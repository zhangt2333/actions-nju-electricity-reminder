# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Copyright 2022 zhangt2333. All Rights Reserved.
# Author-Github: github.com/zhangt2333
import base64
import random

import ddddocr
from Cryptodome.Cipher import AES


def encrypt_password(text: str, key: str):
    r"""encrypt the password
    the code is translated from encrypt.js
    """
    _rds = lambda length: ''.join(
        [random.choice('ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678') for _ in range(length)])
    pad = lambda s: s + (len(key) - len(s) % len(key)) * chr(len(key) - len(s) % len(key))
    text = pad(_rds(64) + text).encode("utf-8")
    aes = AES.new(str.encode(key), AES.MODE_CBC, str.encode(_rds(16)))
    return str(base64.b64encode(aes.encrypt(text)), 'utf-8')


def predict_captcha(image: bytes) -> str:
    return ddddocr.DdddOcr(show_ad=0).classification(image)
