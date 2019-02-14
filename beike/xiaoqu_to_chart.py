#!/usr/bin/env python
# coding=utf-8
# 1. 杀死之前启动的http服务器
# 2. 启动一个新的http服务器
# 3. 用浏览器打开生成的数据html文件
import sys

sys.path.append("../")

import pandas as pd
from pyecharts import Bar, Map, Page

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
            # ct = 'wh'
            # 注意，已经将分割符号转换成分号，因为有的小区名中有逗号
            df = pd.read_csv(xiaoqu_city_path + "/{0}.csv".format(ct), encoding="utf-8", sep=";")
            dist = [i + "区" if not i.endswith("区") else i for i in df["district"].tolist()]
            df.insert(0, "district_full", dist)
            # 打印总行数
            print("before: row number is {0}".format(len(df)))
            # 过滤房价为0的无效数据
            df = df[df.price > 0]
            print("trim zero: row number is {0}".format(len(df)))

            ####################################################
            # 最贵的小区排名
            ####################################################
            df.sort_values("price", ascending=False, inplace=True)
            num = -1
            print(df.head(10))
            city = cities[ct]
            xqs = df["xiaoqu"][0:num]
            prices = df["price"][0:num]
            page = Page()
            xiaoqu_bar = Bar("{0}小区均价".format(city), width=1200)
            xiaoqu_bar.add("小区均价排名", xqs, prices,
                           is_label_show=True,
                           is_more_utils=True,
                           xaxis_interval=0,
                           xaxis_rotate=30,
                           is_datazoom_show=True,
                           datazoom_type="both",
                           datazoom_range=[10, 10.3],
                           )
            xiaoqu_bar.render(path="html/{0}_xiaoqu_bar.html".format(ct))

            ####################################################
            # 区县均价排名
            ####################################################
            district_df = df.groupby('district_full').mean()
            district_df = district_df.round(0)
            district_df.sort_values("price", ascending=False, inplace=True)
            print(district_df)
            districts = district_df.index
            prices = district_df["price"]
            district_bar = Bar("{0}区县均价".format(city), width=1200)
            district_bar.add("区县均价排名", districts, prices,
                             is_stack=False,
                             xaxis_interval=0,
                             xaxis_rotate=30,
                             mark_line=["average"],
                             is_label_show=True,
                             is_more_utils=True
                             )
            district_bar.render(path="html/{0}_district_bar.html".format(ct))

            ####################################################
            # 区县均价排名-地图
            ####################################################
            district_map = Map("{0}区县均价分布".format(city), width=1200, height=600)
            price_min, price_max = min(prices.tolist()), max(prices.tolist())
            district_map.add("", districts, prices,
                             maptype=city,
                             is_visualmap=True,
                             visual_text_color="#000",
                             visual_range=[price_min, price_max],
                             is_label_show=True,
                             is_more_utils=True)
            district_map.render(path="html/{0}_district_map.html".format(ct))

            page.add(district_map)
            page.add(district_bar)
            page.add(xiaoqu_bar)
            page.render(path="html/{0}.html".format(ct))
            # break
        except Exception as e:
            print("error with df: ", e)
            continue
