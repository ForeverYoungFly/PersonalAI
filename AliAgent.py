"""
-*- coding: utf-8 -*-
@Author: Young
@Time: 2024/8/29 18:19
@File: AliAgent.py
@Contact: yangyuan0421@gmail.com
@Note:
    1. 与自己云端设定的Agent进行对话
    2. 目前Prompt在阿里云那边设置，这里不再使用Prompt
    3. 命令行输入：panel serve AliAgent.py --autoreload  启动服务
    4. 如果环境变量设置好后，os.getenv还是返回None，请重启Windows
    5. 程序搭好以后，可以写个bat脚本，启动服务
    6. Panel参考文档https://panel.holoviz.org/

"""

# 导入所需的库
import panel as pn
from http import HTTPStatus
from dashscope import Application
from panel.chat import ChatInterface
import param
import os


pn.extension()  # 加载Panel扩展
# 定义CSS样式
pn.config.raw_css.append("""
div > img {
    border-radius: 50% !important;  /* 使图片变成圆形 */
    width: 50px !important; height: 50px !important;
}
.nav.flex-column{
    height: 100% !important;
}
.sidenav  .bk-panel-models-layout-Column {
    height: 85% !important;
}
.bk-panel-models-reactive_html-ReactiveHTML{
    height: 10% !important;
}
""")

knowledgeDBUpdateTime = '2024年9月9日'  # 设置知识库最新的更新日期
api_key = '{YOUR_API_KEY}'   # 替换为自己的API_KEY
app_id = '{YOUR_APP_ID}'  # 替换为自己的APP_ID
# 定义用户和系统头像的路径
user_avatar = 'assets/user_avatar.JPG'
# 定义模型的价格信息
model_name = 'qwen-Max'
if model_name == 'qwen-Turbo':
    model_price_input = 0.002/1000  # 模型输入价格(每1000个token)
    model_price_output = 0.006/1000  # 模型输出价格（每1000个token）
elif model_name == 'qwen-Max':
    model_price_input = 0.04/1000
    model_price_output = 0.012/1000
# 后续可以添加更多模型的价格信息


# 创建一个ChatCount类，这样就可以参数化，然后调用watch方法，监控参数的变化
class ChatCount(param.Parameterized):
    turns_count = param.Integer(default=0)
    input_tokens = param.List(default=[])
    output_tokens = param.List(default=[])


# 处理信息
def process_message(response):
    # 输出参数表：https://help.aliyun.com/zh/model-studio/developer-reference/call-alibaba-cloud-model-studio-through-sdk?spm=a2c4g.11186623.0.0.20f968c1DoBFl8
    global session_id
    if response.status_code != HTTPStatus.OK:
        return '网络连接错误'
    else:
        session_id = response.output.session_id  # 获取session_id
        print('response:', response.usage)
        chat_count_instance.input_tokens.append(response.usage['models'][0]['input_tokens'])
        chat_count_instance.output_tokens.append(response.usage['models'][0]['output_tokens'])
        chat_count_instance.turns_count += 1
        return response.output.text


# 调用Agent应用
def call_agent_app(messages, user, instance):
    # 首轮对话不需要session_id
    if chat_count_instance == 1:
        response = Application.call(app_id=app_id,
                                    prompt=messages,
                                    api_key=api_key
                                    )
        return process_message(response)

    else:
        response = Application.call(app_id=app_id,
                                    prompt=messages,
                                    api_key=api_key,
                                    session_id=session_id
                                    )
        return process_message(response)


def indicators_update(*events):
    turns_count_indicator.value = chat_count_instance.turns_count
    lastInputTokens.value = chat_count_instance.input_tokens[-1]
    inputTokens.value = sum(chat_count_instance.input_tokens)
    lastOutputTokens.value = chat_count_instance.output_tokens[-1]
    outputTokens.value = sum(chat_count_instance.output_tokens)
    costTokens.value = round(inputTokens.value * model_price_input + outputTokens.value * model_price_output, 2)


# 创建实例
chat_count_instance = ChatCount()
session_id = None


# 监听对话轮次参数(chat_count_instance实例中的turns_count参数)的更新
chat_count_instance.param.watch(indicators_update, 'turns_count')

# 创建ChatInterface实例
chat_interface = ChatInterface(
    callback=call_agent_app,
    callback_exception='verbose',
    widgets=[
        pn.chat.ChatAreaInput(placeholder='Type your message here...', resizable='height')],
    user="Young",
    avatar=user_avatar,
    show_undo=False,
    show_rerun=False)

# 创建Indicators实例
turns_count_indicator = pn.indicators.Number(
    name="Conversation Turns",
    value=0,
    default_color="green",
    title_size='10pt',
    font_size='20pt'
)

lastInputTokens = pn.indicators.Number(name="Last Input Tokens", value=0, title_size='10pt', font_size='20pt')

inputTokens = pn.indicators.Number(name="Total Input Tokens", value=0, title_size='10pt', font_size='20pt')

lastOutputTokens = pn.indicators.Number(name="Last Output Tokens", value=0, title_size='10pt', font_size='20pt')

outputTokens = pn.indicators.Number(name="Total Output Tokens", value=0, title_size='10pt', font_size='20pt')

costTokens = pn.indicators.Number(name="本次消费(￥)", value=0, title_size='10pt', font_size='20pt')

sidebar = pn.FlexBox(
    pn.Column(
        turns_count_indicator,
        lastInputTokens,
        inputTokens,
        lastOutputTokens,
        outputTokens,
        costTokens),
    pn.FlexBox(f"Powered by {model_name} model<br>知识库更新于{knowledgeDBUpdateTime}"))

pn.template.FastListTemplate(title='AIAgent',
                             sidebar=sidebar,
                             main=[chat_interface],
                             ).servable()



