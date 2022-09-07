# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Copyright 2021 zhangt2333. All Rights Reserved.
# Author-Github: github.com/zhangt2333
# spider.py 2021/9/11 13:01
import re
import requests

from . import utils

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Linux; Android 11; Redmi K30 Pro Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/90.0.4430.210 Mobile Safari/537.36 cpdaily/9.0.15 wisedu/9.0.15",
})


def login(username: str, password: str, to_url: str) -> requests.sessions.Session:
    r"""登录并返回Session

    :param username: your student id
    :param password: your password
    :param to_url: callback url, like "https://ehall.nju.edu.cn:443/login?service=https://ehall.nju.edu.cn/ywtb-portal/official/index.html"
    :return: requests.sessions.Session
    """
    url = f"https://authserver.nju.edu.cn/authserver/login?service={to_url}&login_type=mobileLogin"
    lt, dllt, execution, _eventId, rmShown, pwdDefaultEncryptSalt = getLoginCasData(url)
    data = dict(
        username=username,
        password=utils.encrypt_password(password, pwdDefaultEncryptSalt),
        lt=lt,
        dllt=dllt,
        execution=execution,
        _eventId=_eventId,
        rmShown=rmShown,
    )
    # 可能验证码错误, 登录会重试3次
    for _ in range(3):
        try:
            data["captchaResponse"] = getCaptcha(username)
            session.post(url=url, data=data)
            if session.cookies.get("MOD_AUTH_CAS") or session.cookies.get("JSESSIONID"):
                return session
        except Exception: pass
    raise Exception("login error")


def getLoginCasData(url: str):
    r"""返回CAS数据和初始JSESSIONID

    :param url: the full url
    :return: lt, dllt, execution, _eventId, rmShown, pwdDefaultEncryptSalt
    """
    try:
        response = session.get(url)
        if response.status_code == 200:
            # 获取 html 中 hidden 的表单 input
            lt = re.search(r'<input type="hidden" name="lt" value="(.*?)"/>', response.text).group(1)
            dllt = re.search(r'<input type="hidden" name="dllt" value="(.*?)"/>', response.text).group(1)
            execution = re.search(r'<input type="hidden" name="execution" value="(.*?)"/>', response.text).group(1)
            _eventId = re.search(r'<input type="hidden" name="_eventId" value="(.*?)"/>', response.text).group(1)
            rmShown = re.search(r'<input type="hidden" name="rmShown" value="(.*?)"', response.text).group(1)
            pwdDefaultEncryptSalt = re.search(r'var pwdDefaultEncryptSalt = "(.*?)"', response.text).group(1)
            return lt, dllt, execution, _eventId, rmShown, pwdDefaultEncryptSalt
    except Exception as e:
        raise e


def getCaptcha(username: str) -> str:
    r"""获取登录需要的验证码

    :return: the captcha text
    """
    if isNeedCaptcha(username):
        try:
            captcha_image = session.get("https://authserver.nju.edu.cn/authserver/captcha.html")
            if captcha_image.status_code == 200:
                return utils.predict_captcha(captcha_image.content)
            raise Exception("get captcha error")
        except Exception as e:
            raise e
    return ""


def isNeedCaptcha(username: str) -> bool:
    r"""返回该用户登录是否需要验证码

    :param username: your student id
    :return: True if need captcha for logining
    """
    try:
        response = session.get(
            url="https://authserver.nju.edu.cn/authserver/needCaptcha.html",
            params=dict(username=username)
        )
        return "true" in response.text
    except Exception as e:
        raise e
