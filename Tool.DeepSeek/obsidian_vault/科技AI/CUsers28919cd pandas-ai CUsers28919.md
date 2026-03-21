---
title: CUsers28919cd pandas-ai CUsers28919
category: 科技AI
tags: [科技AI, 教程, 问题]
source: DeepSeek
messages: 12
processed: 2026-02-20
---
## User

C:\Users\28919>cd pandas-ai

C:\Users\28919\pandas-ai>docker-compose build
error during connect: Head "http://%2F%2F.%2Fpipe%2FdockerDesktopLinuxEngine/_ping": open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified.

## Assistant

The error you're encountering is related to Docker Desktop not running or not being properly configured on your Windows system. Let's go through the steps to resolve this:

### 1. Start Docker Desktop

- Ensure Docker Desktop is installed and running.

Ensure Docker Desktop is installed and running.

- Look for the Docker whale icon in your system tray (bottom-right corner).

Look for the Docker whale icon in your system tray (bottom-right corner).

- If it's not running, start it from the Start Menu.

If it's not running, start it from the Start Menu.

### 2. Switch to Linux Containers

- Right-click the Docker Desktop icon in the system tray.

Right-click the Docker Desktop icon in the system tray.

- Select "Switch to Linux Containers" (if you see "Switch to Windows Containers", it means you're already in Linux mode).

Select "Switch to Linux Containers" (if you see "Switch to Windows Containers", it means you're already in Linux mode).

### 3. Check Docker Service

- Open PowerShell or Command Prompt.

Open PowerShell or Command Prompt.

- Run:bash复制下载docker version

Run:

- If you get a similar error, Docker Desktop is not communicating properly.

If you get a similar error, Docker Desktop is not communicating properly.

### 4. Restart Docker Desktop

- Fully exit Docker Desktop via the system tray (right-click → Quit).

Fully exit Docker Desktop via the system tray (right-click → Quit).

- Reopen Docker Desktop from the Start Menu.

Reopen Docker Desktop from the Start Menu.

- Wait 1–2 minutes for it to initialize.

Wait 1–2 minutes for it to initialize.

### 5. Run as Administrator

- Right-click your Command Prompt/PowerShell and select "Run as Administrator".

Right-click your Command Prompt/PowerShell and select "Run as Administrator".

- Try the docker-compose build command again.

Try the docker-compose build command again.

### 6. Reset Docker Desktop

- Open Docker Desktop settings (gear icon in the top-right).

Open Docker Desktop settings (gear icon in the top-right).

- Go to Troubleshoot → Reset to factory defaults.

Go to Troubleshoot → Reset to factory defaults.

- Restart your computer afterward.

Restart your computer afterward.

### 7. Reinstall Docker Desktop

If issues persist:

- Uninstall Docker Desktop via Windows Settings → Apps.

Uninstall Docker Desktop via Windows Settings → Apps.

- Download the latest version from Docker Hub.

Download the latest version from Docker Hub.

- Install it and reboot your system.

Install it and reboot your system.

### 8. Verify WSL2 Integration

- Docker Desktop on Windows uses WSL2. Ensure:WSL2 is enabled (see Microsoft's guide).In Docker Desktop settings → General, check "Use the WSL 2 based engine".

Docker Desktop on Windows uses WSL2. Ensure:

- WSL2 is enabled (see Microsoft's guide).

WSL2 is enabled (see Microsoft's guide).

- In Docker Desktop settings → General, check "Use the WSL 2 based engine".

In Docker Desktop settings → General, check "Use the WSL 2 based engine".

After completing these steps, run:

again in your project directory. Let me know if you still face issues!

## User

中文谢谢

## Assistant

不用客气！如果还有其他问题或需要进一步的帮助，随时告诉我。祝你使用Docker和PandasAI顺利！ 😊

## User

中文

## Assistant

以下是解决该问题的详细中文步骤指南：

### 问题原因

你遇到的错误通常是因为 Docker Desktop 未运行 或 Docker 服务未正确启动，导致命令行无法连接到 Docker 引擎。

### 解决方法

#### 1. 启动 Docker Desktop

- 双击桌面图标或从开始菜单打开 Docker Desktop。

双击桌面图标或从开始菜单打开 Docker Desktop。

- 等待 1-2 分钟，直到右下角系统托盘出现白鲸图标（🐳），且图标静止（非闪烁状态）。

等待 1-2 分钟，直到右下角系统托盘出现白鲸图标（🐳），且图标静止（非闪烁状态）。

https://i.imgur.com/2dHmzKk.png

#### 2. 切换为 Linux 容器模式

- 右键点击 Docker 托盘图标。

右键点击 Docker 托盘图标。

- 如果菜单显示 "Switch to Windows Containers"，说明当前已是 Linux 模式，无需操作。

如果菜单显示 "Switch to Windows Containers"，说明当前已是 Linux 模式，无需操作。

- 如果显示 "Switch to Linux Containers"，点击切换并等待完成。

如果显示 "Switch to Linux Containers"，点击切换并等待完成。

#### 3. 验证 Docker 是否正常运行

- 以 管理员身份 打开 PowerShell 或命令提示符。

以 管理员身份 打开 PowerShell 或命令提示符。

- 输入以下命令：bash复制下载docker version

输入以下命令：

- 正常情况：会显示 Client 和 Server 版本信息。

正常情况：会显示 Client 和 Server 版本信息。

- 异常情况：如果提示 error during connect，继续下一步。

异常情况：如果提示 error during connect，继续下一步。

#### 4. 重启 Docker 服务

- 完全退出 Docker Desktop：右键托盘图标 → Quit Docker Desktop。

完全退出 Docker Desktop：

- 右键托盘图标 → Quit Docker Desktop。

右键托盘图标 → Quit Docker Desktop。

- 重新打开 Docker Desktop，等待初始化完成（白鲸图标静止）。

重新打开 Docker Desktop，等待初始化完成（白鲸图标静止）。

#### 5. 检查 WSL2 集成

- 按下 Win + S，搜索并打开 “启用或关闭 Windows 功能”。

按下 Win + S，搜索并打开 “启用或关闭 Windows 功能”。

- 确保勾选：Hyper-VWindows Subsystem for LinuxVirtual Machine Platform

确保勾选：

- Hyper-V

Hyper-V

- Windows Subsystem for Linux

Windows Subsystem for Linux

- Virtual Machine Platform

Virtual Machine Platform

- 保存后重启电脑。

保存后重启电脑。

#### 6. 以管理员身份运行命令

- 右键点击命令提示符/PowerShell → 以管理员身份运行。

右键点击命令提示符/PowerShell → 以管理员身份运行。

- 进入你的项目目录：bash复制下载cd C:\Users\28919\pandas-ai

进入你的项目目录：

- 再次尝试构建：bash复制下载docker-compose build

再次尝试构建：

#### 7. 重置 Docker Desktop

- 如果仍失败，尝试重置 Docker：打开 Docker Desktop。点击右上角齿轮图标 → Troubleshoot → Reset to factory defaults。重启电脑后重试。

如果仍失败，尝试重置 Docker：

- 打开 Docker Desktop。

打开 Docker Desktop。

- 点击右上角齿轮图标 → Troubleshoot → Reset to factory defaults。

点击右上角齿轮图标 → Troubleshoot → Reset to factory defaults。

- 重启电脑后重试。

重启电脑后重试。

### 常见问题补充

- 错误 WSL2 not found需手动安装 WSL2：bash复制下载wsl --install完成后重启系统。

错误 WSL2 not found

- 需手动安装 WSL2：bash复制下载wsl --install

需手动安装 WSL2：

- 完成后重启系统。

完成后重启系统。

- Hyper-V 未启用按下 Win + R，输入 optionalfeatures，勾选 Hyper-V 并重启。

Hyper-V 未启用

- 按下 Win + R，输入 optionalfeatures，勾选 Hyper-V 并重启。

按下 Win + R，输入 optionalfeatures，勾选 Hyper-V 并重启。

完成以上步骤后，再次运行 docker-compose build 应该可以成功。如果仍有问题，请提供完整错误截图或日志，我会进一步帮你分析！ 🚀

## User

等待 1-2 分钟，直到右下角系统托盘出现白鲸图标（🐳），且图标静止（非闪烁状态）
等了好久，它一直闪烁

## Assistant

服务器繁忙，请稍后再试。

## User

An unexpected error occurred while executing a WSL command.

Either shut down WSL down with wsl --shutdown, and/or reboot your machine. You can also try reinstalling WSL and/or Docker Desktop. If the issue persists, collect diagnostics and submit an issue ⁠.

## Assistant

以下是分步解决方案，帮助您解决与 WSL 相关的 Docker 错误：

### 1. 强制关闭 WSL 并重启

### 2. 验证 WSL 2 安装状态

- 若版本为 "1"：升级到 WSL 2：bash复制下载wsl --set-version <发行版名称> 2

若版本为 "1"：升级到 WSL 2：

### 3. 启用必要的 Windows 功能

- 按下 Win + R，输入 optionalfeatures 打开以下窗口：勾选：Hyper-VWindows Subsystem for LinuxVirtual Machine Platform点击 确定 并重启电脑。

按下 Win + R，输入 optionalfeatures 打开以下窗口：

- 勾选：Hyper-VWindows Subsystem for LinuxVirtual Machine Platform

勾选：

- Hyper-V

Hyper-V

- Windows Subsystem for Linux

Windows Subsystem for Linux

- Virtual Machine Platform

Virtual Machine Platform

- 点击 确定 并重启电脑。

点击 确定 并重启电脑。

### 4. 重设 WSL 默认版本

### 5. 检查 Docker Desktop 的 WSL 集成

- 打开 Docker Desktop

打开 Docker Desktop

- 进入设置 → Resources → WSL Integration

进入设置 → Resources → WSL Integration

- 确保：✅ Enable integration with my default WSL distro✅ 勾选你使用的 WSL 发行版（如 Ubuntu-22.04）

确保：

- ✅ Enable integration with my default WSL distro

✅ Enable integration with my default WSL distro

- ✅ 勾选你使用的 WSL 发行版（如 Ubuntu-22.04）

✅ 勾选你使用的 WSL 发行版（如 Ubuntu-22.04）

https://i.imgur.com/5XzJk9L.png

### 6. 完全重置 Docker Desktop

- 退出 Docker Desktop

退出 Docker Desktop

- 执行以下命令清理残留：bash复制下载docker-compose down
docker system prune -a --volumes

执行以下命令清理残留：

- 重新打开 Docker Desktop → 设置 → Troubleshoot → Reset to factory defaults

重新打开 Docker Desktop → 设置 → Troubleshoot → Reset to factory defaults

### 7. 重新安装 WSL 和 Docker

如果问题仍存在：

- 卸载 WSL：bash复制下载wsl --unregister <发行版名称>

卸载 WSL：

- 重新安装 WSL：bash复制下载wsl --install -d Ubuntu-22.04

重新安装 WSL：

- 卸载并重新安装 Docker Desktop：从 官网 下载最新版本安装时勾选 Use WSL 2 instead of Hyper-V

卸载并重新安装 Docker Desktop：

- 从 官网 下载最新版本

从 官网 下载最新版本

- 安装时勾选 Use WSL 2 instead of Hyper-V

安装时勾选 Use WSL 2 instead of Hyper-V

### 8. 提交诊断信息（最后手段）

将日志提交至：

- Docker 社区论坛：https://forums.docker.com/

Docker 社区论坛：https://forums.docker.com/

- WSL GitHub 仓库：https://github.com/microsoft/WSL/issues

WSL GitHub 仓库：https://github.com/microsoft/WSL/issues

### 补充说明

- 硬件要求：确保系统支持虚拟化（BIOS 中启用 Intel VT-x/AMD-V）

硬件要求：确保系统支持虚拟化（BIOS 中启用 Intel VT-x/AMD-V）

- Windows 版本：必须为 Windows 10 2004+ 或 Windows 11

Windows 版本：必须为 Windows 10 2004+ 或 Windows 11

完成上述步骤后，再次尝试运行 docker-compose build。如果仍有问题，请提供完整错误日志，我会进一步协助！ 🛠️

## User

PS C:\Users\28919> wsl -l -v
适用于 Linux 的 Windows 子系统没有已安装的分发。
可通过安装包含以下说明的分发来解决此问题：

使用“wsl.exe --list --online' ”列出可用的分发
和 “wsl.exe --install <Distro>” 进行安装。
PS C:\Users\28919>

## Assistant

以下是分步解决方案，帮助您安装 WSL 并修复 Docker 依赖环境：

### 1. 安装默认 WSL 发行版（Ubuntu）

- 安装过程会自动启用所需功能并下载系统（约 1GB，确保网络畅通）

安装过程会自动启用所需功能并下载系统（约 1GB，确保网络畅通）

- 安装完成后会自动进入 Ubuntu 初始化（需设置 UNIX 用户名和密码）

安装完成后会自动进入 Ubuntu 初始化（需设置 UNIX 用户名和密码）

### 2. 手动启用 Windows 功能（如果自动启用失败）

- 按下 Win + R，输入 optionalfeatures

按下 Win + R，输入 optionalfeatures

- 勾选以下选项：[✅] Hyper-V[✅] Windows Subsystem for Linux[✅] Virtual Machine Platform

勾选以下选项：

- [✅] Hyper-V

[✅] Hyper-V

- [✅] Windows Subsystem for Linux

[✅] Windows Subsystem for Linux

- [✅] Virtual Machine Platform

[✅] Virtual Machine Platform

- 点击 确定 → 立即重新启动

点击 确定 → 立即重新启动

### 3. 验证 WSL 安装

### 4. 设置默认 WSL 版本

### 5. 配置 Docker Desktop 的 WSL 集成

- 打开 Docker Desktop

打开 Docker Desktop

- 进入设置 → Resources → WSL Integration

进入设置 → Resources → WSL Integration

- 启用选项：✅ Enable integration with my default WSL distro✅ 勾选刚安装的 Ubuntu-22.04

启用选项：

- ✅ Enable integration with my default WSL distro

✅ Enable integration with my default WSL distro

- ✅ 勾选刚安装的 Ubuntu-22.04

✅ 勾选刚安装的 Ubuntu-22.04

https://i.imgur.com/5XzJk9L.png

### 6. 测试 Docker 与 WSL 的协作

如果看到以下输出，表示成功：

### 常见问题处理

#### 问题 1：安装时卡在 Downloading...

- 解决方案：手动下载 WSL 内核更新包访问 微软官方文档，下载并安装 WSL2 Linux 内核更新包

解决方案：手动下载 WSL 内核更新包访问 微软官方文档，下载并安装 WSL2 Linux 内核更新包

#### 问题 2：错误 WslRegisterDistribution failed

#### 问题 3：BIOS 未开启虚拟化

- 重启电脑，进入 BIOS（按键通常是 F2、Delete 或 F10）

重启电脑，进入 BIOS（按键通常是 F2、Delete 或 F10）

- 找到选项：Intel CPU：启用 Intel Virtualization Technology (VT-x)AMD CPU：启用 SVM Mode

找到选项：

- Intel CPU：启用 Intel Virtualization Technology (VT-x)

Intel CPU：启用 Intel Virtualization Technology (VT-x)

- AMD CPU：启用 SVM Mode

AMD CPU：启用 SVM Mode

- 保存并退出

保存并退出

完成以上步骤后，返回您的项目目录再次尝试：

如果仍有问题，请提供完整错误截图或日志，我会进一步分析！ 🚀