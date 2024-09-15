"""
-*- coding: utf-8 -*-
@Author: Young
@Time: 2024/9/2 16:24
@File: KnowledgeSpider.py
@Contact: yangyuan0421@gmail.com
@Note: 用于下载并爬取指定网页的内容

"""

import requests
from bs4 import BeautifulSoup
import os
import datetime


# 定义爬虫函数
def spider(url, output_file):
    # 获取网页内容
    response = requests.get(url)
    response.encoding = 'utf-8'
    html = response.text

    # 解析网页内容
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.get_text()

    # 写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)


# 起始函数
def main():
    # 定义爬取网页的URL
    url = input('请输入要爬取的网页URL：')

    # 获取当前日期
    now = datetime.datetime.now()

    # 创建一个新的文件夹，命名为KnowledgeSpider+当前日期
    output_folder = 'KnowledgeSpider' + now.strftime('%Y%m%d')

    # 创建一个空白txt文件，命名为KnowledgeSpider.txt
    output_file = output_folder + '.txt'

    # 调用爬虫函数
    spider(url, output_file)

    print('网页内容已经写入KnowledgeSpider.txt文件中')


if __name__ == '__main__':
    main()

