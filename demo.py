"""
-*- coding: utf-8 -*-
@Author: Young
@Time: 2024/9/14 16:14
@File: demo.py
@Contact: yangyuan0421@gmail.com
@Note:

"""

from http import HTTPStatus
from dashscope import Application
import os
api_key = os.getenv('QWEN_API_KEY')


def call_with_stream():
    responses = Application.call(app_id='6f91dae8baaa4bc18d4845eac1bb01cb',
                                 api_key=api_key,
                                 prompt='如何做炒西红柿鸡蛋？',
                                 stream=True,
                                 incremental_output=True
                                 )

    for response in responses:
        if response.status_code != HTTPStatus.OK:
            print('request_id=%s, code=%s, message=%s\n' % (
                response.request_id, response.status_code, response.message))
        else:
            print('output=%s, usage=%s\n' % (response.output, response.usage))


if __name__ == '__main__':
    call_with_stream()

