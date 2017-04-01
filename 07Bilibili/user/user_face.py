# -*- coding: utf-8 -*-
"""
@description: 
@author:XuMing
"""
from __future__ import print_function  # 兼容python3的print写法
from __future__ import unicode_literals  # 兼容python3的编码处理

import re
import urllib

f = open("bilibili_user_info.txt")
line = f.readline()
for i in range(1, 6):
    print(line, )
    if re.match('http://static.*', line):
        line = f.readline()
        print('noface:' + str(i))
    else:
        filename = 'face/' + str(i) + ".jpg"
        urllib.urlretrieve(url=line.strip(), filename=filename)
        line = f.readline()
        print('succeed:' + str(i))

f.close()
