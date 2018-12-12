#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# @Time: 18-12-12 22:01
# @Author: Badiu Chief Play Officer
# @About: spider to scrapy movie data from douban
# @Copyright (c) 2018 - BCPO <noneenon@protonmail.com>

import requests
from requests.cookies import RequestsCookieJar
import random
import time
from pymongo import MongoClient
import progressbar

# MongoDB Connection Client
conn = MongoClient("mongodb://localhost:27017")

# requests get
subjectid = []
headers = {
        "User_Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36"
}
api = "http://api.douban.com/v2/movie/subject/"

# progress bar
p = progressbar.ProgressBar()


def main():
    cookie_jar = RequestsCookieJar()
    for line in open("subjectid.txt", "r"):
        subjectid.append(line.strip("\n"))
    total = len(subjectid)
    print("Total subjectid number: "+str(total))

    try:
        db = conn.douban
        for j in p(range(194,total)):
            url = api + str(subjectid[j])
            sleep_time = random.random()
            time.sleep(sleep_time)
            response = requests.get(url,headers=headers,cookies=cookie_jar)
            if response.status_code == 200:
                db.movies.insert_one(response.json())
                cookie_jar = response.cookies
            else:
                exit(print("REQUEST ERROR "+str(response.status_code)+" J: "+str(j)))
    except Exception:
        exit(print("CREATE DB ERROR."))
    else:
        # for movie in db.movies.find():
        #     print(movie)
        exit(print("Done."))


if __name__ == "__main__":
    main()
