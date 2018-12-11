#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# @Time: 18-12-10 19:58
# @Author: Badiu Chief Play Officer
# @About: spider to scrapy movie subject_id from douban
# @Copyright (c) 2018 - BCPO <noneenon@protonmail.com>

import requests
from requests.cookies import RequestsCookieJar
import json
import random
import time
import progressbar
import threading

# movie data
subject_id = []

header = {
    "User_Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36"
}

# API1
url_get_api1 = "https://movie.douban.com/j/new_search_subjects"
params_api1 = {
        "sort": "A",
        "range": "0,1",
        "tags": "电影",
        "start": 0
}

range_list = ["0,1","1,2","2,3","3,4","4,5","5,6","6,6.4","6.4,6.7","6.7,7","7,7.4","7.4,8","8,9","9,10"]

# API2
url_get2 = "https://movie.douban.com/j/search_subjects"
params_api2 = {
        "type": "movie",
        "tag": "热门",
        "sort": "time",
        "page_limit": 10000,
        "page_start": 0
}
tag_list = ["热门", "最新", "经典", "可播放", "豆瓣高分", "冷门佳片", "华语", "欧美", "韩国", "日本", "动作", "喜剧", "爱情", "科幻", "悬疑", "恐怖", "成长"]

def main():
    # Spider API1 Scrapy by remark score
    def spider_api1():
        cookie_jar_api1 = RequestsCookieJar()
        for range_item in range_list:
            p = progressbar.ProgressBar()
            score_length = 0
            params_api1["range"] = range_item
            # more than 9979 for 0 score
            for i in p(range(501)):
                sleep_time = random.random() / 2
                time.sleep(sleep_time)
                response = requests.get(url_get_api1, headers=header, cookies=cookie_jar_api1, params=params_api1)
                if response.status_code == 200:
                    data1_pjson = json.loads(response.text)
                    data1_list = data1_pjson["data"]
                    score_length = score_length + len(data1_list)
                    if len(data1_list) == 0:
                        break
                    for data_item in data1_list:
                        subject_id.append(data_item["id"])
                    params_api1["start"] = params_api1["start"] + 20
                    cookie_jar_api1 = response.cookies
                else:
                    exit(print("Request Error" + response.status_code)+" i: "+str(i))
            params_api1["start"] = 0
            p.finish()
            print("Item: " + range_item + " Length: " + str(score_length))
        print("Thread_api1 Done.")

    # Spider API2 Scrapy by tags(tag is not enough)
    def spider_api2():
        cookie_jar_api2 = RequestsCookieJar()
        for tag in tag_list:
            sleep_time = random.random() / 2
            time.sleep(sleep_time)
            params_api2["tag"] = tag
            response = requests.get(url_get2, headers=header, cookies=cookie_jar_api2, params=params_api2)
            if response.status_code == 200:
                data2_pjson = json.loads(response.text)
                data2_list = data2_pjson["subjects"]
                for item in data2_list:
                    subject_id.append(item["id"])
                cookie_jar_api2 = response.cookies
            else:
                exit(print("ERROR CODE" + response.status_code + " Tag: " + tag))
        print("Thread_api2 Done.")
    # create & start thread api1
    thr_api1 = threading.Thread(target=spider_api1())
    thr_api1.start()

    # create & start thread api2
    thr_api2 = threading.Thread(target=spider_api2())
    thr_api2.start()

    # wait thread_api1 & thread_api2 end
    thr_api1.join()
    thr_api2.join()

    # remove repeat item
    subjectid = list(set(subject_id))
    print("Subject_id No-Repeat Total: " + str(len(subjectid)))
    # write to file
    f = open("subjectid.txt", "w")
    f.write(subjectid[0])
    for id in subjectid[1:]:
        f.write("\n" + str(id).strip("\""))
    f.close()

if __name__ == "__main__":
    main()
