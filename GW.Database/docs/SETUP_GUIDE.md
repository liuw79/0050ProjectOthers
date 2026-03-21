# GW.Database - 环境搭建指南

本指南详细说明了在 macOS 系统上搭建 GW.Database 项目所需的环境配置步骤，特别是针对 SQL Server ODBC 驱动的安装和配置。

## 1. 安装 Homebrew (如果尚未安装)

Homebrew 是 macOS 上优秀的包管理器，我们将使用它来安装 FreeTDS。

打开终端，执行以下命令：

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

按照提示完成安装。

## 2. 配置 Homebrew 国内镜像源 (推荐)

为了加快 Homebrew 的下载速度，特别是安装大型软件包时，建议配置清华大学的镜像源。

打开终端，执行以下命令来修改 Homebrew 的环境变量配置。这些配置将被写入您的 `~/.zshrc` 文件中，并立即生效。

```bash
# 将以下内容完整复制并粘贴到您的终端中执行
echo '\n# Homebrew mirror configuration' >> ~/.zshrc && \
echo 'export HOMEBREW_BREW_GIT_REMOTE="https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/brew.git"' >> ~/.zshrc && \
echo 'export HOMEBREW_CORE_GIT_REMOTE="https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/homebrew-core.git"' >> ~/.zshrc && \
echo 'export HOMEBREW_BOTTLE_DOMAIN="https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles"' >> ~/.zshrc && \
source ~/.zshrc
```

执行完成后，运行 `brew update` 来验证镜像源是否生效：

```bash
brew update
```

如果更新速度明显加快，则说明配置成功。

## 3. 安装 FreeTDS ODBC 驱动

GW.Database 使用 FreeTDS 作为连接 SQL Server 的 ODBC 驱动。

打开终端，执行以下命令进行安装：

```bash
brew install freetds
```

## 4. 配置 `odbcinst.ini` 文件

`pyodbc` 需要 `odbcinst.ini` 文件来定位 FreeTDS 驱动。我们将把 FreeTDS 的配置添加到 `/usr/local/etc/odbcinst.ini` 文件中。

首先，获取 FreeTDS 的安装路径：

```bash
basename $(brew --prefix freetds)/lib/libtdsodbc.so
```

假设 FreeTDS 的版本是 `1.5.4`，那么驱动路径通常是 `/usr/local/Cellar/freetds/1.5.4/lib/libtdsodbc.so`。

**请将以下内容完整复制并粘贴到您的终端中执行，并在提示时输入您的系统密码：**

```bash
echo '[FreeTDS]
Description=FreeTDS Driver for SQL Server
Driver=/usr/local/Cellar/freetds/1.5.4/lib/libtdsodbc.so
Setup=/usr/local/Cellar/freetds/1.5.4/lib/libtdsodbc.so
FileUsage=1
UsageCount=1

[SQL Server]
Description=FreeTDS Driver for SQL Server
Driver=/usr/local/Cellar/freetds/1.5.4/lib/libtdsodbc.so
Setup=/usr/local/Cellar/freetds/1.5.4/lib/libtdsodbc.so
FileUsage=1
UsageCount=1' | sudo tee /usr/local/etc/odbcinst.ini > /dev/null
```

**重要提示**: 请确保 `Driver` 和 `Setup` 路径中的版本号 (`1.5.4`) 与您实际安装的 FreeTDS 版本一致。您可以通过 `ls /usr/local/Cellar/freetds/` 来查看实际的版本目录。

## 5. 创建并激活 Python 虚拟环境

在项目根目录下执行：

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 6. 安装 Python 依赖

```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple fastapi uvicorn sqlalchemy pyodbc
```

## 7. 配置数据库连接信息

编辑 `main.py` 文件，更新数据库连接参数。请参考 `DATABASE_CONFIG.md` 获取详细信息。

## 8. 启动服务

```bash
source .venv/bin/activate
python main.py
```

服务将在 `http://127.0.0.1:8001` 启动。
