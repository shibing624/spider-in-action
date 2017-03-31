# -*- coding: utf-8 -*-
"""
@description: 
@author:XuMing
"""
from __future__ import print_function  # 兼容python3的print写法
from __future__ import unicode_literals  # 兼容python3的编码处理

import json

from bs4 import BeautifulSoup as BS

from common import Common

"""
验证码错误返回：{ "r": 1, "errcode": 1991829, "data": {"captcha":"验证码错误"}, "msg": "验证码错误" }
验证码过期：{ "r": 1, "errcode": 1991829, 
"data": {"captcha":"验证码回话无效 :(","name":"ERR_VERIFY_CAPTCHA_SESSION_INVALID"}, "msg": "验证码回话无效 :(" }
登录：{"r":0, "msg": "登录成功"}
"""


def login(username, password):
    common = Common()
    logger = common.create_logger('mylogger', 'zhihu.log')
    homepage = r"https://www.zhihu.com/"
    html = common.opener.open(homepage).read()
    soup = BS(html, "html.parser")
    _xsrf = soup.find("input", {'type': 'hidden'}).get("value")

    # 根据email和手机登陆得到的参数名不一样，email登陆传递的参数是‘email’，手机登陆传递的是‘phone_num’
    # username = raw_input("Please input username: ")
    # password = getpass.getpass("Please input your password: ")
    account_name = None
    if "@" in username:
        account_name = 'email'
    else:
        account_name = 'phone_num'

    logger.info("save captcha to local machine.")
    captchaURL = r"https://www.zhihu.com/captcha.gif?type=login"  # 验证码url
    common.save_captcha(captcha_url=captchaURL, out_path="captcha.jpg")

    post_data = {
        '_xsrf': _xsrf,
        account_name: username,
        'password': password,
        'remember_me': 'true',
        'captcha': raw_input("Please input captcha by captcha.jpg: ")
    }
    header = {
        'Accept': '*/*',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.zhihu.com/',
        'Accept-Language': 'en-GB,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
        'Accept-Encoding': 'gzip, deflate, br',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
        'Host': 'www.zhihu.com'
    }

    url = r"https://www.zhihu.com/login/" + account_name
    common.set_request_data(url, post_data, header)
    resText = common.get_html_text()
    jsonText = json.loads(resText)

    if jsonText["r"] == 0:
        logger.info("Login success!")
    else:
        logger.error("Login Failed!")
        logger.error("Error info ---> " + jsonText["msg"])

    text = common.opener.open(homepage).read()
    common.output(text, "home.html")


if __name__ == '__main__':
    username = 'your username'
    password = 'your password'
    login(username, password)
