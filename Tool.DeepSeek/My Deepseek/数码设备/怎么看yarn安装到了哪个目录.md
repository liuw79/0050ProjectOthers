---
title: 怎么看yarn安装到了哪个目录
category: 数码设备
tags: [数码设备, 教程, 推荐]
source: DeepSeek
messages: 2
processed: 2026-02-20
---
## User

怎么看yarn安装到了哪个目录？

## Assistant

要查看 Yarn 的安装目录，可以通过以下方法分步骤操作：

### 一、查看 Yarn 可执行文件的路径

#### 1. 使用 which 或 where 命令（根据操作系统）

- Linux/macOS：bash复制下载which yarn

Linux/macOS：

- Windows（在命令提示符或 PowerShell 中）：bash复制下载where yarn这会返回 Yarn 可执行文件的绝对路径（例如 /usr/local/bin/yarn 或 C:\Program Files\nodejs\yarn.cmd）。

Windows（在命令提示符或 PowerShell 中）：

这会返回 Yarn 可执行文件的绝对路径（例如 /usr/local/bin/yarn 或 C:\Program Files\nodejs\yarn.cmd）。

### 二、查看 Yarn 全局安装包的目录

#### 2. 通过 Yarn 命令查看全局存储位置

这会显示全局依赖包的安装目录（例如 ~/.config/yarn/global）。

#### 3. 查看全局命令的 bin 目录

这会返回全局命令的 bin 路径（例如 ~/.yarn/bin）。

### 三、通过 npm 查看全局安装路径（如果通过 npm 安装）

#### 4. 查看 npm 全局安装目录

这会显示类似 /usr/local/lib/node_modules/yarn 的路径。

### 四、本地项目中的 Yarn 路径

#### 5. 查看当前项目的 node_modules 目录

如果项目本地安装了 Yarn，路径通常是：

可通过以下命令直接查看：

### 五、操作系统包管理器的安装路径（如 Homebrew）

- Homebrew (macOS)：bash复制下载brew list yarn路径通常为 /usr/local/Cellar/yarn/版本号。

Homebrew (macOS)：

路径通常为 /usr/local/Cellar/yarn/版本号。

- APT (Debian/Ubuntu)：默认安装到 /usr/bin/yarn。

APT (Debian/Ubuntu)：默认安装到 /usr/bin/yarn。

### 总结结果示例

- 可执行文件路径：/usr/local/bin/yarn

可执行文件路径：/usr/local/bin/yarn

- 全局包目录：~/.config/yarn/global

全局包目录：~/.config/yarn/global

- npm 全局路径：/usr/local/lib/node_modules/yarn

npm 全局路径：/usr/local/lib/node_modules/yarn

根据你的安装方式（全局/本地、npm/Yarn 安装）选择对应方法。