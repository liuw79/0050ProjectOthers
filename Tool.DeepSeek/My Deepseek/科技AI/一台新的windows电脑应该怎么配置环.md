---
title: 一台新的windows电脑应该怎么配置环
category: 科技AI
tags: [科技AI, 教程, 推荐, 问题]
source: DeepSeek
messages: 6
processed: 2026-02-20
---
## User

一台新的windows电脑应该怎么配置环境，会让我接下来去玩github上面的开源AI软件更少遇到包依赖及版本问题？

## Assistant

为了在 Windows 系统上高效使用 GitHub 上的开源 AI 项目并减少依赖问题，可以按以下步骤配置环境：

### 一、基础工具安装

- 安装包管理工具Chocolatey（Windows 包管理器）以管理员身份运行 PowerShell，执行：powershell复制下载Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))之后可通过 choco install 快速安装软件（如 Git、Python 等）。

安装包管理工具

- Chocolatey（Windows 包管理器）以管理员身份运行 PowerShell，执行：powershell复制下载Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))之后可通过 choco install 快速安装软件（如 Git、Python 等）。

Chocolatey（Windows 包管理器）以管理员身份运行 PowerShell，执行：

之后可通过 choco install 快速安装软件（如 Git、Python 等）。

- 安装 Gitpowershell复制下载choco install git -y

安装 Git

### 二、Python 环境配置

- 安装 Miniconda（推荐）下载地址：Miniconda Windows选择 Python 3.9 或 3.10（多数 AI 项目兼容的版本），安装时勾选 “Add to PATH”。

安装 Miniconda（推荐）

- 下载地址：Miniconda Windows

下载地址：Miniconda Windows

- 选择 Python 3.9 或 3.10（多数 AI 项目兼容的版本），安装时勾选 “Add to PATH”。

选择 Python 3.9 或 3.10（多数 AI 项目兼容的版本），安装时勾选 “Add to PATH”。

- 配置 Conda 虚拟环境bash复制下载# 创建独立环境（如名为 `ai_env`）
conda create -n ai_env python=3.9
conda activate ai_env优先使用 Conda 安装包：Conda 能自动解决非 Python 依赖（如 NumPy 的 MKL 库）。若包不在 Conda 仓库，再用 pip install。

配置 Conda 虚拟环境

- 优先使用 Conda 安装包：Conda 能自动解决非 Python 依赖（如 NumPy 的 MKL 库）。

优先使用 Conda 安装包：Conda 能自动解决非 Python 依赖（如 NumPy 的 MKL 库）。

- 若包不在 Conda 仓库，再用 pip install。

若包不在 Conda 仓库，再用 pip install。

### 三、GPU 支持（如有 NVIDIA 显卡）

- 安装 CUDA 和 cuDNN查看支持的版本：NVIDIA CUDA 兼容性表通过 Conda 安装（推荐避免手动配置）：bash复制下载conda install cudatoolkit=11.3 cudnn=8.2 -c conda-forge或手动安装：CUDA Toolkit + cuDNN（需注册 NVIDIA 账号）。

安装 CUDA 和 cuDNN

- 查看支持的版本：NVIDIA CUDA 兼容性表

查看支持的版本：NVIDIA CUDA 兼容性表

- 通过 Conda 安装（推荐避免手动配置）：bash复制下载conda install cudatoolkit=11.3 cudnn=8.2 -c conda-forge

通过 Conda 安装（推荐避免手动配置）：

- 或手动安装：CUDA Toolkit + cuDNN（需注册 NVIDIA 账号）。

或手动安装：CUDA Toolkit + cuDNN（需注册 NVIDIA 账号）。

- 验证 GPU 是否可用python复制下载import torch
print(torch.cuda.is_available())  # 应输出 True

验证 GPU 是否可用

### 四、容器化与 Linux 环境

- 启用 WSL2（Windows Subsystem for Linux）powershell复制下载wsl --install -d Ubuntu-22.04在 WSL2 中安装 Python 和 CUDA 可能更少遇到路径问题。

启用 WSL2（Windows Subsystem for Linux）

- 在 WSL2 中安装 Python 和 CUDA 可能更少遇到路径问题。

在 WSL2 中安装 Python 和 CUDA 可能更少遇到路径问题。

- 安装 Docker Desktop下载地址：Docker Desktop for Windows设置中启用 WSL2 后端 和 Kubernetes（可选）。

安装 Docker Desktop

- 下载地址：Docker Desktop for Windows

下载地址：Docker Desktop for Windows

- 设置中启用 WSL2 后端 和 Kubernetes（可选）。

设置中启用 WSL2 后端 和 Kubernetes（可选）。

- 使用 Docker 运行项目bash复制下载docker pull pytorch/pytorch:1.9.0-cuda11.1-cudnn8-runtime
docker run -it --gpus all pytorch/pytorch:1.9.0-cuda11.1-cudnn8-runtime

使用 Docker 运行项目

### 五、IDE 与工具链

- Visual Studio Code 配置安装插件：Python、Jupyter、Docker、Remote - WSL。设置终端为 bash 或 conda。

Visual Studio Code 配置

- 安装插件：Python、Jupyter、Docker、Remote - WSL。

安装插件：Python、Jupyter、Docker、Remote - WSL。

- 设置终端为 bash 或 conda。

设置终端为 bash 或 conda。

- 依赖管理工具pip freeze > requirements.txt 导出环境。复杂项目使用 poetry 或 pipenv：bash复制下载pip install poetry
poetry init  # 生成 pyproject.toml

依赖管理工具

- pip freeze > requirements.txt 导出环境。

pip freeze > requirements.txt 导出环境。

- 复杂项目使用 poetry 或 pipenv：bash复制下载pip install poetry
poetry init  # 生成 pyproject.toml

复杂项目使用 poetry 或 pipenv：

### 六、通用避坑指南

- 路径规范项目路径避免中文、空格和特殊符号（如 C:\Code\ai_project）。

路径规范

- 项目路径避免中文、空格和特殊符号（如 C:\Code\ai_project）。

项目路径避免中文、空格和特殊符号（如 C:\Code\ai_project）。

- 依赖版本锁定使用 conda env export > environment.yml 精确复现环境。

依赖版本锁定

- 使用 conda env export > environment.yml 精确复现环境。

使用 conda env export > environment.yml 精确复现环境。

- 优先使用项目推荐的版本查看项目的 requirements.txt 或 environment.yml。

优先使用项目推荐的版本

- 查看项目的 requirements.txt 或 environment.yml。

查看项目的 requirements.txt 或 environment.yml。

### 七、快速检查清单

- Conda 环境已创建并激活

Conda 环境已创建并激活

- CUDA/cuDNN 版本与深度学习框架匹配（如 TensorFlow/PyTorch 官网文档）

CUDA/cuDNN 版本与深度学习框架匹配（如 TensorFlow/PyTorch 官网文档）

- Docker 和 WSL2 已配置

Docker 和 WSL2 已配置

- 使用 --no-cache-dir 避免 pip 缓存冲突

使用 --no-cache-dir 避免 pip 缓存冲突

通过以上步骤，可显著降低开源 AI 项目的环境配置复杂度。遇到问题时，优先在项目的 GitHub Issues 中搜索错误关键词。

## User

版权所有（C） Microsoft Corporation。保留所有权利。
                        Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))32>
使用“1”个参数调用“DownloadString”时发生异常:“未 能解析此远程名称: 'chocolatey.org'
”
所在位置 行:1 字符: 166
+ ...  -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('ht ...
+                 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (:) [], MethodInvocationException
    + FullyQualifiedErrorId : WebException

## Assistant

你遇到的错误表明系统无法解析 chocolatey.org 的域名，这通常与网络连接或 DNS 配置有关。以下是逐步排查和解决方案：

### 1. 检查网络连接

- 验证能否访问 chocolatey.org在浏览器中访问 https://chocolatey.org：如果无法打开，检查网络是否正常（如代理、防火墙限制）。如果是国内网络，可能被限制，可尝试通过全局代理访问。

验证能否访问 chocolatey.org在浏览器中访问 https://chocolatey.org：

- 如果无法打开，检查网络是否正常（如代理、防火墙限制）。

如果无法打开，检查网络是否正常（如代理、防火墙限制）。

- 如果是国内网络，可能被限制，可尝试通过全局代理访问。

如果是国内网络，可能被限制，可尝试通过全局代理访问。

- 使用 ping 测试域名解析在 PowerShell 中运行：powershell复制下载ping chocolatey.org如果返回 无法访问目标主机，说明 DNS 解析失败。尝试更换 DNS（如 8.8.8.8 或 114.114.114.114）。

使用 ping 测试域名解析在 PowerShell 中运行：

- 如果返回 无法访问目标主机，说明 DNS 解析失败。

如果返回 无法访问目标主机，说明 DNS 解析失败。

- 尝试更换 DNS（如 8.8.8.8 或 114.114.114.114）。

尝试更换 DNS（如 8.8.8.8 或 114.114.114.114）。

### 2. 手动下载安装脚本

如果直接执行命令失败，可手动下载安装脚本：

- 在浏览器中访问以下链接：https://chocolatey.org/install.ps1

在浏览器中访问以下链接：https://chocolatey.org/install.ps1

- 将页面内容保存为 install.ps1，存放在本地（如 C:\install.ps1）。

将页面内容保存为 install.ps1，存放在本地（如 C:\install.ps1）。

- 在 PowerShell 中运行：powershell复制下载Set-ExecutionPolicy Bypass -Scope Process -Force
.\install.ps1

在 PowerShell 中运行：

### 3. 使用国内镜像源（针对国内网络问题）

如果因网络限制无法访问，可尝试替换 Chocolatey 的安装源：

### 4. 检查代理设置

如果使用代理服务器，需在 PowerShell 中配置代理：

### 5. 临时关闭防火墙/安全软件

某些安全软件（如 360、火绒）可能拦截网络请求，尝试暂时关闭它们后重试。

### 6. 使用备用安装方法

如果仍失败，可用 Windows 自带的包管理器 winget 安装 Chocolatey：

### 验证安装

安装完成后，检查 Chocolatey 是否正常工作：

### 总结步骤

- 确保网络畅通，尝试浏览器访问 chocolatey.org。

确保网络畅通，尝试浏览器访问 chocolatey.org。

- 手动下载安装脚本或使用国内镜像源。

手动下载安装脚本或使用国内镜像源。

- 检查代理和防火墙设置。

检查代理和防火墙设置。

- 使用 winget 作为备用方案。

使用 winget 作为备用方案。

如果问题依旧，请提供更详细的网络环境描述（如是否在公司/学校网络、是否使用 VPN）。

## User

Set-ExecutionPolicy Bypass -Scope Process -Force
>> .\C:\Users\28919\Downloads\install.ps1
.\C:\Users\28919\Downloads\install.ps1 : 无法将“.\C:\Users\28919\Downloads\install.ps1”项识别为 cmdlet、函数、脚本文
件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。
所在位置 行:2 字符: 1
+ .\C:\Users\28919\Downloads\install.ps1
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : ObjectNotFound: (.\C:\Users\28919\Downloads\install.ps1:String) [], CommandNotFoundExcep
   tion
    + FullyQualifiedErrorId : CommandNotFoundException

## Assistant

你可以通过以下步骤解决该问题：

### 错误原因分析

错误提示表明 PowerShell 无法找到 install.ps1 脚本文件，可能原因包括：

- 文件路径错误（如拼写错误或文件未保存到指定位置）

文件路径错误（如拼写错误或文件未保存到指定位置）

- 路径中包含特殊字符（如空格未用引号包裹）

路径中包含特殊字符（如空格未用引号包裹）

- 未进入脚本所在目录直接调用绝对路径时语法错误

未进入脚本所在目录直接调用绝对路径时语法错误

### 解决方案

#### 1. 检查文件路径是否正确

- 打开资源管理器，确认 C:\Users\28919\Downloads\ 目录下存在 install.ps1 文件。

打开资源管理器，确认 C:\Users\28919\Downloads\ 目录下存在 install.ps1 文件。

- 重点检查：文件名是否完整（如不是 install.ps1.txt，需显示文件扩展名）。路径是否包含空格（如有，需用英文引号包裹路径）。

重点检查：

- 文件名是否完整（如不是 install.ps1.txt，需显示文件扩展名）。

文件名是否完整（如不是 install.ps1.txt，需显示文件扩展名）。

- 路径是否包含空格（如有，需用英文引号包裹路径）。

路径是否包含空格（如有，需用英文引号包裹路径）。

#### 2. 直接使用完整绝对路径

在 PowerShell 中运行以下命令（注意去掉开头的 .\）：

或：

#### 3. 切换到脚本目录后执行

#### 4. 处理特殊字符（如空格）

如果路径包含空格或特殊符号（如 C:\Users\My Downloads\install.ps1），需用引号包裹路径：

#### 5. 验证文件是否存在

在 PowerShell 中运行以下命令检查文件：

- 若返回 True，文件存在；若返回 False，需重新下载脚本。

若返回 True，文件存在；若返回 False，需重新下载脚本。

### 完整操作示例

### 其他注意事项

- 管理员权限：需以管理员身份运行 PowerShell。

管理员权限：需以管理员身份运行 PowerShell。

- 文件扩展名：如果系统隐藏了扩展名，文件可能实际保存为 install.ps1.txt，需重命名为 install.ps1。

文件扩展名：如果系统隐藏了扩展名，文件可能实际保存为 install.ps1.txt，需重命名为 install.ps1。

- 防病毒软件：临时关闭安全软件，避免拦截脚本执行。

防病毒软件：临时关闭安全软件，避免拦截脚本执行。

如果问题仍未解决，请提供以下信息：

- 文件 install.ps1 的完整路径截图

文件 install.ps1 的完整路径截图

- 执行 Get-ChildItem C:\Users\28919\Downloads\install.ps1 的输出结果

执行 Get-ChildItem C:\Users\28919\Downloads\install.ps1 的输出结果