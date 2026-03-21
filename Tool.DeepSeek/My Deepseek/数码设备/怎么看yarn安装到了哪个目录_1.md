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

要确定 Yarn 的安装目录，可以按照以下步骤操作，具体方法取决于你的操作系统和安装方式：

### 方法 1：使用 which 或 where 命令

这些命令可以直接定位 Yarn 的可执行文件路径。

- Linux/macOS（终端）：bash复制下载which yarn如果结果是符号链接（例如 /usr/local/bin/yarn），可以进一步查看真实路径：bash复制下载readlink -f $(which yarn)

Linux/macOS（终端）：

如果结果是符号链接（例如 /usr/local/bin/yarn），可以进一步查看真实路径：

- Windows（CMD 或 PowerShell）：cmd复制下载where yarn

Windows（CMD 或 PowerShell）：

### 方法 2：检查 npm 的全局安装路径

如果 Yarn 是通过 npm 全局安装的（如 npm install -g yarn），可以找到 npm 的全局包目录：

这会返回类似 /usr/local（Linux/macOS）或 C:\Users\YourName\AppData\Roaming\npm（Windows）的路径。Yarn 的可执行文件通常位于此路径的 bin 子目录中。

### 方法 3：检查系统包管理器路径

- Ubuntu/Debian（通过 apt 安装）：bash复制下载dpkg -L yarn

Ubuntu/Debian（通过 apt 安装）：

- macOS（通过 Homebrew 安装）：bash复制下载brew list yarn

macOS（通过 Homebrew 安装）：

### 方法 4：直接检查 Yarn 的版本信息

运行以下命令，观察输出中的 bin 路径：

### 总结路径示例

- npm 全局安装：Linux/macOS: /usr/local/bin/yarnWindows: %APPDATA%\npm\yarn.CMD

npm 全局安装：

- Linux/macOS: /usr/local/bin/yarn

Linux/macOS: /usr/local/bin/yarn

- Windows: %APPDATA%\npm\yarn.CMD

Windows: %APPDATA%\npm\yarn.CMD

- 系统包管理器安装：Ubuntu: /usr/bin/yarnHomebrew: /usr/local/bin/yarn

系统包管理器安装：

- Ubuntu: /usr/bin/yarn

Ubuntu: /usr/bin/yarn

- Homebrew: /usr/local/bin/yarn

Homebrew: /usr/local/bin/yarn

通过以上方法，你可以快速定位 Yarn 的安装目录。