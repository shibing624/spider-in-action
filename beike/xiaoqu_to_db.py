#!/usr/bin/env python
# coding=utf-8
# read data from csv, write to database
# database includes: csv
import sys

sys.path.append("../")
import os

from beike.config import SPIDER_NAME
from beike.place.city import cities, get_chinese_city
from beike.util.date import get_date_string
from beike.util.path import DATA_PATH


def create_prompt_text():
    city_info = list()
    num = 0
    for en_name, ch_name in cities.items():
        num += 1
        city_info.append(en_name)
        city_info.append(": ")
        city_info.append(ch_name)
        if num % 4 == 0:
            city_info.append("\n")
        else:
            city_info.append(", ")
    return 'Which city data do you want to save ?\n' + ''.join(city_info)


if __name__ == '__main__':
    # 设置目标数据库
    database = "csv"
    db = None
    collection = None
    workbook = None
    csv_file = None
    datas = list()
    # save all data to one file
    # 集合文件
    all_name = "all"
    csv_all_path = "{0}/{1}/xiaoqu/{2}.csv".format(DATA_PATH, SPIDER_NAME, all_name)
    f_all = open(csv_all_path, 'w', encoding='utf-8')
    line = "{0};{1};{2};{3};{4};{5};{6}\n".format('city_ch', 'date', 'district', 'area', 'xiaoqu', 'price', 'sale')
    f_all.write(line)
    f_all_count = 0

    # city = get_city()
    for city in cities:
        # city = 'wh'
        xiaoqu_city_path = "{0}/{1}/xiaoqu".format(DATA_PATH, SPIDER_NAME)
        csv_file = open(xiaoqu_city_path + "/{0}.csv".format(city), "w", encoding='utf-8')
        line = "{0};{1};{2};{3};{4};{5};{6}\n".format('city_ch', 'date', 'district', 'area', 'xiaoqu', 'price', 'sale')
        csv_file.write(line)
        # 准备日期信息，爬到的数据存放到日期相关文件夹下
        date = get_date_string()
        # 获得 csv 文件路径
        # date = "20180331"   # 指定采集数据的日期
        # city = "sh"         # 指定采集数据的城市
        city_ch = get_chinese_city(city)
        csv_dir = "{0}/{1}/xiaoqu/{2}/{3}".format(DATA_PATH, SPIDER_NAME, city, date)

        files = list()
        if not os.path.exists(csv_dir):
            print("{0} does not exist.".format(csv_dir))
            print("Please run 'python xiaoqu.py' firstly.")
            print("Bye.")
            continue
        else:
            print('OK, start to process ' + get_chinese_city(city))
        for csv in os.listdir(csv_dir):
            data_csv = csv_dir + "/" + csv
            # print(data_csv)
            files.append(data_csv)

        # 清理数据
        count = 0
        row = 0
        col = 0
        for csv in files:
            with open(csv, 'r', encoding='utf-8') as f:
                for line in f:
                    count += 1
                    text = line.strip()
                    try:
                        # 如果小区名里面没有逗号，那么总共是6项
                        if text.count(',') == 5:
                            date, district, area, xiaoqu, price, sale = text.split(',')
                        elif text.count(',') < 5:
                            continue
                        else:
                            fields = text.split(',')
                            date = fields[0]
                            district = fields[1]
                            area = fields[2]
                            xiaoqu = ','.join(fields[3:-2])
                            price = fields[-2]
                            sale = fields[-1]
                    except Exception as e:
                        print(text)
                        print(e)
                        continue
                    sale = sale.replace(r'套在售二手房', '')
                    price = price.replace(r'暂无', '0')
                    price = price.replace(r'元/m2', '')
                    price = int(price)
                    sale = int(sale)
                    line = "{0};{1};{2};{3};{4};{5};{6}\n".format(city_ch, date, district, area, xiaoqu, price, sale)
                    csv_file.write(line)
                    f_all.write(line)
                    f_all_count += 1

        # 写入，并且关闭句柄
        csv_file.close()
        print("Total write {0} items to csv.".format(count))
    f_all.close()
    print("ALL: Total write {0} items to csv.".format(f_all_count))



