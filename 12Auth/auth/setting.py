#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: XuMing <shibing624@126.com>
@description:
"""


import requests.adapters

ADAPTER_WITH_RETRY = requests.adapters.HTTPAdapter(
    max_retries=requests.adapters.Retry(
        total=10,
        status_forcelist=[403,408,500,502],
    )
)

DEFAULT_CAPTCHA_FILENAME = 'captcha.gif'
"""
验证码文件，放置在当前目录下的captcha.gif。
"""