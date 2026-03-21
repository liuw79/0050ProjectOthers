---
title: android sdk如何安装
category: 数码设备
tags: [数码设备, 教程, 推荐, 问题]
source: DeepSeek
messages: 2
processed: 2026-02-20
---
## User

android sdk如何安装

## Assistant

安装 Android SDK 的步骤如下：

### 1. 下载 Android Studio

Android SDK 通常通过 Android Studio 安装。首先，下载并安装 Android Studio：

- 访问 Android Studio 官网。

访问 Android Studio 官网。

- 下载适合你操作系统的版本（Windows、macOS 或 Linux）。

下载适合你操作系统的版本（Windows、macOS 或 Linux）。

- 运行安装程序并按照提示完成安装。

运行安装程序并按照提示完成安装。

### 2. 安装 Android SDK

安装 Android Studio 时，默认会包含 Android SDK，但你可以手动安装或更新：

- 启动 Android Studio。

启动 Android Studio。

- 打开 SDK Manager：在欢迎界面，点击“Configure” > “SDK Manager”。如果已打开项目，点击“File” > “Settings” > “Appearance & Behavior” > “System Settings” > “Android SDK”。

打开 SDK Manager：

- 在欢迎界面，点击“Configure” > “SDK Manager”。

在欢迎界面，点击“Configure” > “SDK Manager”。

- 如果已打开项目，点击“File” > “Settings” > “Appearance & Behavior” > “System Settings” > “Android SDK”。

如果已打开项目，点击“File” > “Settings” > “Appearance & Behavior” > “System Settings” > “Android SDK”。

- 选择 SDK 版本：在“SDK Platforms”选项卡中，勾选需要的 Android 版本。在“SDK Tools”选项卡中，选择必要的工具（如 Android SDK Build-Tools、Android Emulator 等）。

选择 SDK 版本：

- 在“SDK Platforms”选项卡中，勾选需要的 Android 版本。

在“SDK Platforms”选项卡中，勾选需要的 Android 版本。

- 在“SDK Tools”选项卡中，选择必要的工具（如 Android SDK Build-Tools、Android Emulator 等）。

在“SDK Tools”选项卡中，选择必要的工具（如 Android SDK Build-Tools、Android Emulator 等）。

- 点击“Apply”或“OK”，开始下载并安装所选内容。

点击“Apply”或“OK”，开始下载并安装所选内容。

### 3. 配置环境变量（可选）

为方便命令行使用 SDK 工具，可以配置环境变量：

- 找到 SDK 路径：默认路径：Windows: C:\Users\<用户名>\AppData\Local\Android\SdkmacOS: ~/Library/Android/sdkLinux: ~/Android/Sdk

找到 SDK 路径：

- 默认路径：Windows: C:\Users\<用户名>\AppData\Local\Android\SdkmacOS: ~/Library/Android/sdkLinux: ~/Android/Sdk

默认路径：

- Windows: C:\Users\<用户名>\AppData\Local\Android\Sdk

Windows: C:\Users\<用户名>\AppData\Local\Android\Sdk

- macOS: ~/Library/Android/sdk

macOS: ~/Library/Android/sdk

- Linux: ~/Android/Sdk

Linux: ~/Android/Sdk

- 设置环境变量：Windows：右键“此电脑” > “属性” > “高级系统设置” > “环境变量”。在“系统变量”中找到 Path，点击“编辑”，添加 SDK 的 tools 和 platform-tools 路径。macOS/Linux：打开终端，编辑 ~/.bashrc 或 ~/.zshrc 文件，添加：bash复制下载export ANDROID_HOME=~/Library/Android/sdk
export PATH=$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools:$PATH保存后运行 source ~/.bashrc 或 source ~/.zshrc 使更改生效。

设置环境变量：

- Windows：右键“此电脑” > “属性” > “高级系统设置” > “环境变量”。在“系统变量”中找到 Path，点击“编辑”，添加 SDK 的 tools 和 platform-tools 路径。

Windows：

- 右键“此电脑” > “属性” > “高级系统设置” > “环境变量”。

右键“此电脑” > “属性” > “高级系统设置” > “环境变量”。

- 在“系统变量”中找到 Path，点击“编辑”，添加 SDK 的 tools 和 platform-tools 路径。

在“系统变量”中找到 Path，点击“编辑”，添加 SDK 的 tools 和 platform-tools 路径。

- macOS/Linux：打开终端，编辑 ~/.bashrc 或 ~/.zshrc 文件，添加：bash复制下载export ANDROID_HOME=~/Library/Android/sdk
export PATH=$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools:$PATH保存后运行 source ~/.bashrc 或 source ~/.zshrc 使更改生效。

macOS/Linux：

- 打开终端，编辑 ~/.bashrc 或 ~/.zshrc 文件，添加：bash复制下载export ANDROID_HOME=~/Library/Android/sdk
export PATH=$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools:$PATH

打开终端，编辑 ~/.bashrc 或 ~/.zshrc 文件，添加：

- 保存后运行 source ~/.bashrc 或 source ~/.zshrc 使更改生效。

保存后运行 source ~/.bashrc 或 source ~/.zshrc 使更改生效。

### 4. 验证安装

打开终端或命令提示符，输入以下命令验证安装：

如果显示 ADB 版本信息，说明 SDK 安装成功。

### 5. 更新 SDK

定期更新 SDK 以获取最新功能和修复：

- 打开 Android Studio。

打开 Android Studio。

- 进入“SDK Manager”。

进入“SDK Manager”。

- 在“SDK Platforms”和“SDK Tools”中，勾选需要更新的项目，点击“Apply”或“OK”进行更新。

在“SDK Platforms”和“SDK Tools”中，勾选需要更新的项目，点击“Apply”或“OK”进行更新。

### 总结

通过以上步骤，你可以成功安装并配置 Android SDK。如有问题，可参考官方文档或社区资源。