---
title: windows 11 hosts 文件在哪
category: 科技AI
tags: [科技AI, 教程, 推荐, 问题]
source: DeepSeek
messages: 4
processed: 2026-02-20
---
## User

windows 11 hosts 文件在哪

## Assistant

Windows 11 的 hosts 文件标准路径是：C:\Windows\System32\drivers\etc\hosts-2-3-4。

### 🔍 查找与编辑关键提示

找到该文件后，要顺利查看和编辑它，有几个关键点需要注意：

- 文件显示：该目录下的 hosts 文件没有扩展名（如 .txt）。如果你在文件夹中只看到名为 hosts 的文件，而没有更具体的类型描述，那它就是你要找的文件-3-4。

文件显示：该目录下的 hosts 文件没有扩展名（如 .txt）。如果你在文件夹中只看到名为 hosts 的文件，而没有更具体的类型描述，那它就是你要找的文件-3-4。

- 以管理员身份编辑：直接双击打开可能无法保存修改。正确的方法是：先在开始菜单搜索“记事本”，然后右键选择“以管理员身份运行”。在记事本中，通过“文件”->“打开”导航到上述路径，并选择打开 hosts 文件-7。

以管理员身份编辑：直接双击打开可能无法保存修改。正确的方法是：先在开始菜单搜索“记事本”，然后右键选择“以管理员身份运行”。在记事本中，通过“文件”->“打开”导航到上述路径，并选择打开 hosts 文件-7。

- 修改格式与保存：在文件末尾添加新规则时，格式为 IP地址 + 空格/制表符 + 域名（例如：127.0.0.1 example.com）。保存时，务必保持文件名为 hosts，且没有后缀，不要另存为 .txt 文件-7。

修改格式与保存：在文件末尾添加新规则时，格式为 IP地址 + 空格/制表符 + 域名（例如：127.0.0.1 example.com）。保存时，务必保持文件名为 hosts，且没有后缀，不要另存为 .txt 文件-7。

### 💡 额外建议：快速打开方法

如果你觉得手动导航路径麻烦，这里有一个更快捷的方法：按下 Win + R 键打开“运行”对话框，然后直接输入上述完整路径 C:\Windows\System32\drivers\etc 并回车，就能直接进入目标文件夹-1。

如果你打算修改 hosts 文件来实现特定的网络功能（如屏蔽某些网站或进行本地开发测试），我可以为你提供更具体的操作示例和注意事项。

## User

# Copyright (c) 1993-2009 Microsoft Corp.
#
# This is a sample HOSTS file used by Microsoft TCP/IP for Windows.
#
# This file contains the mappings of IP addresses to host names. Each
# entry should be kept on an individual line. The IP address should
# be placed in the first column followed by the corresponding host name.
# The IP address and the host name should be separated by at least one
# space.
#
# Additionally, comments (such as these) may be inserted on individual
# lines or following the machine name denoted by a '#' symbol.
#
# For example:
#
#      102.54.94.97     rhino.acme.com          # source server
#       38.25.63.10     x.acme.com              # x client host

# localhost name resolution is handled within DNS itself.
#	127.0.0.1       localhost
#	::1             localhost
# Added by Docker Desktop
127.0.0.1 *.douyin.com
127.0.0.1 www.douyin.com
192.168.1.2 host.docker.internal
192.168.1.2 gateway.docker.internal
# To allow the same kube context to work on the host and the container:
127.0.0.1 kubernetes.docker.internal
# End of section
为什么这样没有阻止抖音网站打开播放视频？

## Assistant

根据你提供的 hosts 文件内容，添加了 *.douyin.com 等规则后，抖音网页仍然能打开，这是非常常见的情况。主要原因和解决方法如下：

### 🔍 主要原因分析

- DNS缓存：系统或浏览器可能缓存了抖音域名之前解析到的真实IP地址。你修改 hosts 文件后，这个“旧结果”还在被使用。

DNS缓存：系统或浏览器可能缓存了抖音域名之前解析到的真实IP地址。你修改 hosts 文件后，这个“旧结果”还在被使用。

- CDN与多域名：像抖音这样的大型网站，视频、图片、API接口等资源通常由多个不同的子域名提供（例如 p3.douyin.com, s0.douyin.com 等）。你屏蔽的 *.douyin.com 规则可能无法覆盖所有实际使用的域名，特别是当你访问的是 www.douyin.com 时，页面会加载大量其他域名的资源。

CDN与多域名：像抖音这样的大型网站，视频、图片、API接口等资源通常由多个不同的子域名提供（例如 p3.douyin.com, s0.douyin.com 等）。你屏蔽的 *.douyin.com 规则可能无法覆盖所有实际使用的域名，特别是当你访问的是 www.douyin.com 时，页面会加载大量其他域名的资源。

- IP直连与HSTS：部分网站或应用（尤其是手机App）可能会绕开域名解析，直接连接IP地址，或者通过HTTPS的HSTS机制强制使用安全连接，这使得 hosts 文件在本地重定向IP的方法失效。

IP直连与HSTS：部分网站或应用（尤其是手机App）可能会绕开域名解析，直接连接IP地址，或者通过HTTPS的HSTS机制强制使用安全连接，这使得 hosts 文件在本地重定向IP的方法失效。

- 规则格式：*.douyin.com 这个通配符写法在某些系统或软件的 hosts 文件解析中可能不被支持。标准写法是列举具体子域名。

规则格式：*.douyin.com 这个通配符写法在某些系统或软件的 hosts 文件解析中可能不被支持。标准写法是列举具体子域名。

### 🛠️ 解决步骤（从易到难）

你可以按照以下步骤排查和增强屏蔽效果：

#### 第一步：清除DNS缓存（立即生效）

这是最应该先尝试的方法。以管理员身份运行“命令提示符”或“Windows PowerShell”，输入以下命令后回车：

完成后，完全关闭浏览器再重新打开，然后测试访问。

#### 第二步：补充更多抖音相关域名

如果清除缓存无效，问题很可能在于抖音使用了其他你未屏蔽的域名。你需要找出这些域名并添加到 hosts 文件中。

- 基础添加：在你现有规则下方，可以先手动补充一些常见的抖音域名：text复制下载127.0.0.1 douyin.com
127.0.0.1 www.douyin.com
127.0.0.1 v.douyin.com
127.0.0.1 p3.douyin.com
127.0.0.1 s0.douyin.com
127.0.0.1 s3.douyin.com
127.0.0.1 toutiao.com

基础添加：在你现有规则下方，可以先手动补充一些常见的抖音域名：

- 高级查找（推荐）：要更彻底地屏蔽，需要找出所有相关域名。打开浏览器（以Chrome为例）的开发者工具 (F12)。切换到 Network（网络）标签页。在地址栏访问抖音网站，观察“Network”面板中加载的所有资源请求。在列表上方的筛选栏输入 douyin，就能看到所有包含该关键词的域名。将它们全部记录下来，并逐个添加到 hosts 文件中，指向 127.0.0.1。

高级查找（推荐）：要更彻底地屏蔽，需要找出所有相关域名。

- 打开浏览器（以Chrome为例）的开发者工具 (F12)。

打开浏览器（以Chrome为例）的开发者工具 (F12)。

- 切换到 Network（网络）标签页。

切换到 Network（网络）标签页。

- 在地址栏访问抖音网站，观察“Network”面板中加载的所有资源请求。

在地址栏访问抖音网站，观察“Network”面板中加载的所有资源请求。

- 在列表上方的筛选栏输入 douyin，就能看到所有包含该关键词的域名。将它们全部记录下来，并逐个添加到 hosts 文件中，指向 127.0.0.1。

在列表上方的筛选栏输入 douyin，就能看到所有包含该关键词的域名。将它们全部记录下来，并逐个添加到 hosts 文件中，指向 127.0.0.1。

#### 第三步：检查浏览器特性

- HTTPS问题：现代浏览器对HTTPS网站非常严格。如果你访问的是 https://www.douyin.com，即使 hosts 将其指向了 127.0.0.1，浏览器也会因为IP地址与抖音SSL证书不匹配而报错并可能仍然显示旧页面。你可以尝试访问 http://www.douyin.com（HTTP协议）来验证。

HTTPS问题：现代浏览器对HTTPS网站非常严格。如果你访问的是 https://www.douyin.com，即使 hosts 将其指向了 127.0.0.1，浏览器也会因为IP地址与抖音SSL证书不匹配而报错并可能仍然显示旧页面。你可以尝试访问 http://www.douyin.com（HTTP协议）来验证。

- 使用隐私/无痕模式：在浏览器的隐私（或无痕）窗口中测试，这个模式下通常没有缓存，能更真实地反映 hosts 文件的效果。

使用隐私/无痕模式：在浏览器的隐私（或无痕）窗口中测试，这个模式下通常没有缓存，能更真实地反映 hosts 文件的效果。

#### 第四步：考虑使用专业工具

如果以上方法都无法满足需求（例如想屏蔽手机App内的抖音），那么 hosts 文件可能力有未逮。你可以考虑：

- 使用防火墙：在Windows防火墙或第三方防火墙中，直接阻止抖音相关域名的出站连接。

使用防火墙：在Windows防火墙或第三方防火墙中，直接阻止抖音相关域名的出站连接。

- 使用广告屏蔽插件：在浏览器中安装如 uBlock Origin 等插件，通过自定义规则来屏蔽抖音网站及其元素。

使用广告屏蔽插件：在浏览器中安装如 uBlock Origin 等插件，通过自定义规则来屏蔽抖音网站及其元素。

- 修改路由器设置：在家庭路由器的家长控制或黑名单功能中，直接屏蔽 douyin.com 等域名，这样所有连接该Wi-Fi的设备都无法访问。

修改路由器设置：在家庭路由器的家长控制或黑名单功能中，直接屏蔽 douyin.com 等域名，这样所有连接该Wi-Fi的设备都无法访问。

### 💎 总结建议

- 立即执行：以管理员身份运行 ipconfig /flushdns，然后重启浏览器测试。

立即执行：以管理员身份运行 ipconfig /flushdns，然后重启浏览器测试。

- 如果无效：使用浏览器的开发者工具，找出抖音页面加载的所有子域名，将它们全部添加到 hosts 文件中。

如果无效：使用浏览器的开发者工具，找出抖音页面加载的所有子域名，将它们全部添加到 hosts 文件中。

- 注意局限性：理解 hosts 文件对HTTPS网站和直接IP连接的屏蔽效果有限。对于深度屏蔽，需结合防火墙等工具。

注意局限性：理解 hosts 文件对HTTPS网站和直接IP连接的屏蔽效果有限。对于深度屏蔽，需结合防火墙等工具。

如果需要更详细的某一步骤（例如如何使用开发者工具抓取域名），我可以为你提供更具体的操作指引。