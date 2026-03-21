# VPN —— Clash 使用与故障排查指南

> 本文记录了使用 Clash（含 ClashX、Clash Verge、Clash Meta 等衍生版本）时遇到 “Google 无法打开” 的典型问题及解决方案 —— **未启用虚拟网卡（TUN/TAP）模式**。
>
> 若后续遇到新的 VPN/代理相关问题，请在本文件继续补充。

---

## 1️⃣ 现象描述

1. 系统基础网络连通正常：`ping 8.8.8.8` 通畅。
2. DNS 解析正常：`dig www.google.com` 能返回 IP（多为污染地址）。
3. 直接访问 `http://www.google.com` 或 `https://www.google.com` 浏览器/`curl` 均超时。
4. 代理软件（Clash）已运行，节点延迟正常，但**仍无法访问谷歌及其他被墙站点**。

### 关键线索
- 日志显示请求已被规则匹配到代理，但无返回数据。
- `scutil --proxy` 看到系统 HTTP/HTTPS 代理已被设置。
- Clash 日志偶尔提示：`[Warning] TUN is not enabled, fallback to system proxy`。

---

## 2️⃣ 问题根因

Clash **仅开启系统代理（HTTP/HTTPS 端口 7890）** 时，浏览器只会将普通 HTTP/HTTPS 请求通过代理；而某些程序（尤其是 *DoH/DoT DNS*、QUIC、非 HTTP 流量）会直接走系统直连。

当 “虚拟网卡模式” (*TUN / TAP / VPN 模式*) 未开启时：
- IP 包级转发未生效 → SNI/RST 干扰仍会阻断 TLS 握手 → Google 无法打开。
- macOS 12+ 默认优先使用 DoH，导致 DNS 走直连，被污染。

---

## 3️⃣ 解决方案：启用虚拟网卡模式

### ClashX / ClashX Pro
1. 右键菜单 → `配置` → 勾选 **启用 TUN 模式**。
2. 首次会提示安装驱动（`clash-nat` 或 `tunhelper`），按提示输入管理员密码。
3. 重启 ClashX，确认状态栏图标显示 `TUN` 字样。

### Clash Verge / Clash Verge Rev
1. `Settings` → `System` → 开启 **Clash TUN** 开关。
2. Protocol 选择 `mixed`，TUN Driver 选择 `clash-tun`（或 `meta-tun`）。
3. 保存后重启应用。

### 通用验证步骤
```bash
# 查看虚拟网卡是否加载成功
ifconfig | grep utun
# utun10: flags=8051<UP,POINTOPOINT,RUNNING,MULTICAST> mtu 1380

# 测试 443 端口连通
curl -Iv https://www.google.com --proxy socks5h://127.0.0.1:7891 --connect-timeout 5
```
出现 `HTTP/2 200` 即表示恢复正常。

---

## 4️⃣ 常用排查命令

```bash
# 基础网络
ping -c 4 8.8.8.8

# DNS
scutil --dns | grep nameserver -A2

# 代理端口占用
lsof -i :7890
lsof -i :7891

# 测试走代理
curl -I https://www.google.com --proxy http://127.0.0.1:7890 --connect-timeout 5

# 查看 TUN 进程 & 日志
ps aux | grep clash
log stream --predicate 'process == "ClashX"' --style syslog --info
```

---

## 5️⃣ 国内镜像下载 Clash

| 平台 | 推荐镜像 |
|-------|-----------|
| macOS (ClashX) | https://ghproxy.com/https://github.com/yichengchen/clashX/releases |
| Windows (Clash for Windows) | https://mirror.ghproxy.com/https://github.com/Fndroid/clash_for_windows_pkg/releases |
| Linux (Clash Meta) | https://mirrors.tuna.tsinghua.edu.cn/github-release/MetaCubeX/Clash.Meta |

镜像下载完成后，仍建议对文件进行 SHA256 校验，确保完整性。

---

## 6️⃣ 参考链接
- [Clash Wiki](https://lancellc.gitbook.io/clash/)（可通过代理访问）
- [Clash Meta 文档](https://github.com/MetaCubeX/Clash.Meta/wiki)
- [Clash 常见问题](https://ghproxy.com/https://github.com/Dreamacro/clash/issues)

---

*最后更新：2025-09-25*