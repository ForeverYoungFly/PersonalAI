"""
-*- coding: utf-8 -*-
@Author: Young
@Time: 2024/8/29 17:05
@File: KnowledgeDB.py
@Contact: yangyuan0421@gmail.com
@Note:

"""
import os
import datetime


# 定义处理文件夹的函数
def process_directory(directory, output_file):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                with open(output_file, 'a', encoding='utf-8') as f:
                    f.write(content + '!!!!\n\n\n')


# 定义知识库文件位置
base_filepath = 'C:/Users/Young/Documents/Obsidian Vault'

# 定义知识库文件夹名
file_list = ['01 文献阅读', '02 知识库', '05 论文写作', '06 名人堂', '07 科研', '08 哲学', '发现美好']

# 获取当前日期
now = datetime.datetime.now()

# 创建一个新的文件夹，命名为KnowledgeDB+当前日期
output_folder = 'KnowledgeDB' + now.strftime('%Y%m%d')

# 创建一个空白txt文件，命名为KnowledgeDB.txt
output_file = output_folder + '.txt'
with open(output_file, 'w', encoding='utf-8') as file:
    # 在文件夹第一行写入：“知识库更新日期：datetime”
    file.write('知识库更新日期：'+now.strftime('%Y%m%d\n'))
    pass  # 创建空文件

# 轮询知识库文件夹，拼接字符串
for folder in file_list:
    folder_path = os.path.join(base_filepath, folder)
    print('当前文件夹路径为：', folder_path)
    if os.path.isdir(folder_path):
        process_directory(folder_path, output_file)


# 统计KnowledgeDB.txt文件中的字符数
with open(output_file, 'r', encoding='utf-8') as f:
    content = f.read()
    print('本次知识数据转换后，KnowledgeDB.txt文件中的字符数为：', len(content))

print('知识库文件已经写入KnowledgeDB.txt文件中')


