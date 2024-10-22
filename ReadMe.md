# Midjourney 第三方自动化脚本

## 简介

本项目是一个用于自动化生成 Midjourney 图像的脚本。它通过调用第三方站点的 MJ-Chat 接口，逐步执行 `prompts.json` 中的提示词，并在生成图像后将其下载到本地。生成的图像会被切割成四块，并保存在 `output` 文件夹中。

## 技术栈

本项目使用 Python 开发。请确保您的系统中已安装 Python 环境（建议3.12.4），以便顺利运行本项目。

## 支持的站点

本项目支持 Twoapi 和 [gptgod.online](https://gptgod.online/#/register?invite_code=ddw3yl4ve3ofueqz2jwwnpeyp) 等站点（默认模型为: mj-chat），同时也支持其他能够将 Midjourney 请求转换为一次性 SSE 对话的 API 站点。

使用本人链接注册，可以寻找本人提供有限技术支持 :D

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
#### 使用 PowerShell, 管理员权限，允许Script
- PowerShell 下执行
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned
```

#### 安装 pyenv-win
- PowerShell 下执行
```bash
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
```

#### 安装Git 
下载了一直点下一步安装完成
```bash
https://github.com/git-for-windows/git/releases/download/v2.46.0.windows.1/Git-2.46.0-64-bit.exe
```

#### 获取本项目代码
- PowerShell 下执行，注意你最好先cd到你的执行目录再执行这个，否则会在当前目录创建mj文件夹并保存文件。
```bash
git clone https://github.com/520hacker/mj-chat-autorun.git mj
cd mj
```

#### 安装python
- PowerShell 下执行
```bash
pyenv install  3.12.0
pyenv global 3.12.0
```

#### 安装依赖
- PowerShell 下，找到git文件clone的目录，执行
```bash
.\install.bat
```

请自行设置 .env 文件（格式参看 .env.example ）

#### 开始运行项目
- PowerShell 下，找到git文件clone的目录，执行
```bash
.\run.bat
```

## 在 macOS 上使用 MJ-CHAT-AUTORUN

为了在 macOS 上管理多个 Python 版本，你可以使用 `pyenv`，这是一款流行的工具。以下是如何在你的 Mac 上安装和设置 `pyenv` 的步骤：

### 步骤 1：安装依赖项

在安装 `pyenv` 之前，你需要安装一些依赖项。可以通过终端完成此操作：

1. **打开终端**。

2. **安装命令行工具**：如果你还没有安装 Xcode 命令行工具，请运行：

   ```bash
   xcode-select --install
   ```

3. **安装 Homebrew**：如果你还没有安装 Homebrew，可以通过运行以下命令进行安装：

   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

4. **安装所需软件包**：使用 Homebrew 安装所需的软件包：

   ```bash
   brew install openssl readline sqlite3 xz zlib
   ```

5. **验证安装**：安装完成后，可以通过运行以下命令验证 Git 是否已安装：

   ```bash
   git --version
   ```

### 步骤 2：安装 pyenv

1. **安装 pyenv**：你可以使用 Homebrew 安装 `pyenv`：

   ```bash
   brew install pyenv
   ```

2. **将 pyenv 添加到你的 shell**：你需要将 `pyenv` 添加到你的 shell 启动文件。根据你使用的 shell，可能需要编辑以下文件之一：

   - 对于 **bash**（`~/.bash_profile` 或 `~/.bashrc`）：

     ```bash
     echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bash_profile
     echo 'eval "$(pyenv init --path)"' >> ~/.bash_profile
     echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
     ```

3. **应用更改**：编辑完文件后，通过重启终端或运行以下命令来应用更改：

   ```bash
   source ~/.bash_profile
   ```

### 步骤 3：安装 Python 版本

1. **列出可用的 Python 版本**：你可以通过运行以下命令查看可安装的 Python 版本：

   ```bash
   pyenv install --list
   ```

2. **安装特定的 Python 版本**：要安装特定版本，请使用：

   ```bash
   pyenv install <version>
   ```

   例如，要安装 Python 3.12.0：

   ```bash
   pyenv install 3.12.0
   ```

3. **设置全局 Python 版本**：安装完成后，可以设置全局 Python 版本：

   ```bash
   pyenv global 3.12.0
   ```

4. **验证安装**：检查当前使用的 Python 版本是否正确：

   ```bash
   python --version
   ```

### 步骤 4：安装 Python 依赖项

1. **进入项目文件夹**：

   ```bash
   cd mj
   ```

2. **运行安装命令**：

   ```bash
   pip install requests sseclient-py python-dotenv pillow openpyxl
   ```

3. **创建 .env 文件，并将配置放入其中**：

   ```ini
   API_KEY={你的密钥}
   API_HOST=https://api.gptgod.online
   MIDJOURNEY_MODEL=flux
   MODEL=gpt-4o-mini
   ```

4. **测试应用**：

   ```bash
   python app.py
   ```

## 纯文字对话

- 请更新 text-data.xlsx  ， text-prompts.json 会依据 xlsx 进行生成， 结果会输出到 output 目录。
- install.bat 
- text-run.bat 启动程序

## 贡献

欢迎对本项目提出建议或贡献代码！如有任何问题或建议，请在 GitHub 上提交 issue。

## 许可证

本项目遵循 [MIT 许可证](LICENSE)。
