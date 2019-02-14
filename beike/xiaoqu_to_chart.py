#!/usr/bin/env python
# coding=utf-8
# 1. 杀死之前启动的http服务器
# 2. 启动一个新的http服务器
# 3. 用浏览器打开生成的数据html文件
import sys

sys.path.append("../")

import pandas as pd
from pyecharts import Bar, Grid

from beike.config import SPIDER_NAME
from beike.place.city import cities
from beike.util.path import DATA_PATH

if __name__ == '__main__':
    # try:
    #     os.system("ps aux | grep python | grep http.server | grep -v grep | awk '{print $2}' | xargs kill")
    #     os.system("python3.6 -m http.server 8080 & > /dev/null 2>&1 ")
    # except Exception as e:
    #     print(e)

    xiaoqu_city_path = "{0}/{1}/xiaoqu".format(DATA_PATH, SPIDER_NAME)
    for ct in cities:
        try:
            # 注意，已经将分割符号转换成分号，因为有的小区名中有逗号
            df = pd.read_csv(xiaoqu_city_path + "/{0}.csv".format(ct), encoding="utf-8", sep=";")

            # 打印总行数
            print("row number is {0}".format(len(df.index)))

            # 过滤房价为0的无效数据
            df = df[df.price > 0]
            if not len(df):
                continue

            print("row number is {0}".format(len(df.index)))

            ####################################################
            # 最贵的小区排名
            ####################################################
            df.sort_values("price", ascending=False, inplace=True)
            num = -1
            print(df.head(10))

            city = df["city_ch"][0]
            xqs = df["xiaoqu"][0:num]
            prices = df["price"][0:num]
            bar = Bar("{0}小区均价排名".format(city))
            bar.add("小区均价排名", xqs, prices, is_label_show=True, is_more_utils=True,
                    xaxis_interval=0,
                    xaxis_rotate=30,
                    mark_line=["average"], mark_point=["max", "min"],
                    is_datazoom_show=True,
                    datazoom_type="both",
                    datazoom_range=[10, 10.3],
                    )

            ####################################################
            # 区县均价排名
            ####################################################
            district_df = df.groupby('district').mean()
            district_df = district_df.round(0)
            district_df.sort_values("price", ascending=False, inplace=True)
            print(district_df)
            districts = district_df.index
            prices = district_df["price"]
            district_bar = Bar("{0}区县均价".format(city), title_top="50%")
            district_bar.add("区县均价排名", districts, prices, is_stack=False,
                             xaxis_interval=0,
                             xaxis_rotate=30,
                             mark_line=["average"], mark_point=["max", "min"],
                             is_label_show=True, is_more_utils=True, legend_top="50%")
            grid = Grid(height=720)
            grid.add(bar, grid_bottom="60%")
            grid.add(district_bar, grid_top="60%")
            grid.render(path="html/{0}.html".format(ct))
            # url = "http://localhost:8080/{0}.html".format(ct)
            # web.open(url, new=0, autoraise=True)
            # print(url)
        except Exception as e:
            print("error with df: " + e)
            continue
