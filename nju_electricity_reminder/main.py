# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Copyright 2022 zhangt2333. All Rights Reserved.
# Author-Github: github.com/zhangt2333
import json
import os
import re

import nju_login_spider.spider

if __name__ == '__main__':
    config = json.loads(os.getenv("DATA"))
    session = nju_login_spider.spider.login(config["username"],
                                            config["password"],
                                            "https://wx.nju.edu.cn/njucharge/wap/electric/index")
    response = session.get("https://wx.nju.edu.cn/njucharge/wap/electric/index")
    myRooms = re.search(r'myroom: (\[.*?\]),', response.text).group(1)
    myRooms = myRooms.encode('utf8').decode('unicode_escape')
    myRooms = json.loads(myRooms)
    for room in myRooms:
        name = room["area_name"] + room["build_name"] + room["room_name"]
        electricity = room["dfyl"]
        print(f"当前电量: {electricity}")
        if electricity < config["threshold"]:
            exit(-1)
