#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# @Time: 18-12-12 22:01
# @Author: Badiu Chief Play Officer
# @About: spider to scrapy movie data from douban
# @Copyright (c) 2018 - BCPO <noneenon@protonmail.com>

import requests
from pymongo import MongoClient

# MongoDB Connection Client
conn = MongoClient("mongodb://localhost:27017")

# requests get
subjectid = []
headers = {
        "User_Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        "Content-Type": "json"
}
api = "http://api.douban.com/v2/movie/subject/"

# scylla server
scylla_proxies = "http://39.105.38.48:8081"


def main():
    for line in open("subjectid.txt", "r"):
        subjectid.append(line.strip("\n"))
    total = len(subjectid)
    print("Total subjectid number: "+str(total))

    try:
        db = conn.douban
        j = 0
        while j < total:
            print("J is: " + str(j))
            url = api + str(subjectid[j])
            try:
                response = requests.get(url,headers=headers,proxies={'http': scylla_proxies})
            except Exception:
                print("Proxy Error.")

            try:
                print(response.json())
                if 'title' in response.json():
                    j = j + 1
                    # db.movies.insert_one(response.json())
                else:
                    print("Limit")
            except Exception:
                j = j + 1
                print("Response json Error.")
    except Exception:
        exit(print("CREATE DB ERROR."))
    else:
        # for movie in db.movies.find():
        #     print(movie)
        exit(print("Done."))


if __name__ == "__main__":
    main()
