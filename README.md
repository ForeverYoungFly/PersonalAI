`AliAgent.py` 是一个基于 Panel 框架的 Python 应用程序，用于与云端设定的 Agent 进行对话。该应用程序通过调用阿里云的 API 实现对话功能，并展示对话的统计信息。

## 功能

1. 与云端设定的 Agent 进行对话。
2. 显示对话轮次、输入和输出的 token 数量以及对话的总费用。
3. 自定义用户头像和界面样式。

## 依赖项

- Python 3.x
- `panel`
- `dashscope`
- `param`
- `requests`
- `beautifulsoup4`

## 安装

1. 克隆或下载此项目。
2. 创建并激活虚拟环境（可选）。
3. 安装所需的 Python 包：

    ```bash
    pip install panel dashscope param requests beautifulsoup4
    ```

## 使用方法

1. 确保已设置好阿里云的 API Key，并将其存储在环境变量 `QWEN_API_KEY` 中。
2. 运行以下命令启动服务：

    ```bash
    panel serve AliAgent.py --autoreload
    ```

3. 打开浏览器并访问 `http://localhost:5006/AliAgent` 以使用应用程序。

## 文件说明

- `AliAgent.py`: 主应用程序文件，包含界面定义和对话逻辑。
- `KnowledgeSpider.py`: 用于下载并爬取指定网页内容的脚本。
- `KnowledgeDB.py`: 用于处理知识库文件夹并生成知识库文件的脚本。

## 自定义样式

在 `AliAgent.py` 中，可以通过修改以下 CSS 样式来自定义界面：

```python
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
