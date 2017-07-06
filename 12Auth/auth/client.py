#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: XuMing <shibing624@126.com>
@description:
"""

import requests


class ZhihuClient:
    def __init__(self,client_id = None,secret = None):
        self._session = requests.session()
