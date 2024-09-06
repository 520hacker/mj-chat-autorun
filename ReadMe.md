# Midjourney 第三方自动化脚本

## 简介

本项目是一个用于自动化生成 Midjourney 图像的脚本。它通过调用第三方站点的 MJ-Chat 接口，逐步执行 `prompts.json` 中的提示词，并在生成图像后将其下载到本地。生成的图像会被切割成四块，并保存在 `output` 文件夹中。

## 技术栈

本项目使用 Python 开发。请确保您的系统中已安装 Python 环境（建议3.12.4），以便顺利运行本项目。

## 支持的站点

本项目支持 Twoapi 和 [gptgod.online](https://gptgod.online/#/register?invite_code=ddw3yl4ve3ofueqz2jwwnpeyp) 等站点（默认模型为: mj-chat），同时也支持其他能够将 Midjourney 请求转换为一次性 SSE 对话的 API 站点。

使用本人传销链接注册，可以寻找本人提供有限技术支持 :D

```
https://gptgod.online/#/register?invite_code=ddw3yl4ve3ofueqz2jwwnpeyp
```



## 完成配置

在根目录创建文件 .env
```env
API_KEY={your key}
API_HOST=https://api.gptgod.online
MIDJOURNEY_MODEL=mj-chat
```

如果您使用的是dalle-3 模型，在 gptgod 中，它的自定义名称是  gpt-4-dalle
如果您使用的是midjourney 模型， 在 gptgod 中，它的自定义 mj-chat

## 安装依赖

在项目目录下，执行以下命令以安装所需的依赖：

```bash
pip install requests sseclient-py python-dotenv pillow 
```


## 使用方法

1. 设置好提示词，格式如下：

```json
[
    "提示词1",
    "提示词2"
]
```

2. 执行以下命令以开始自动化任务：

```bash
python app.py
```

针对 midjourney 会生成4张图片拼合在一起的情况，这里提供一个单独的功能，用于把downloads目录中的大图直接切成4张小图，存放到 output 文件夹。

```
python split.py
```


## WIN下零基础安装 
使用 PowerShell, 管理员权限，允许Script
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned
```

安装 pyenv-win
```bash
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
```

安装Git
```bash
https://github.com/git-for-windows/git/releases/download/v2.46.0.windows.1/Git-2.46.0-64-bit.exe
```

获取本项目代码
```bash
git clone https://github.com/520hacker/mj-chat-autorun.git mj
cd mj
```

安装python
```bash
pyenv install  3.12.0
pyenv global 3.12.0
```

安装依赖
```bash
.\install.bat
```

请自行设置 .env 文件（格式参看 .env.example ）


开始运行项目
```bash
.\run.bat
```


## 贡献

欢迎对本项目提出建议或贡献代码！如有任何问题或建议，请在 GitHub 上提交 issue。

## 许可证

本项目遵循 [MIT 许可证](LICENSE)。
