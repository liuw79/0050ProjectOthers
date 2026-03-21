# Monica AI 代理设置指南

## 问题描述
Monica AI 工具出现 "Error: Client network socket disconnected before secure TLS connection was established" 错误。

## 问题原因
系统代理（127.0.0.1:7897）在处理某些 TLS 连接时存在兼容性问题，导致 Monica 无法正常建立安全连接。

## 解决方案

### 方法一：为 Monica 添加专用代理规则（推荐）

#### 1. 找到 Clash Verge 配置文件
```bash
# 配置文件位置
~/Library/Application Support/io.github.clash-verge-rev.clash-verge-rev/clash-verge.yaml
```

#### 2. 备份配置文件
```bash
cp "/Users/comdir/Library/Application Support/io.github.clash-verge-rev.clash-verge-rev/clash-verge.yaml" \
   "/Users/comdir/Library/Application Support/io.github.clash-verge-rev.clash-verge-rev/clash-verge.yaml.backup"
```

#### 3. 添加 Monica 代理规则
在配置文件的 `rules:` 部分开头添加：
```yaml
- DOMAIN-SUFFIX,monica.im,最萌の云 - CuteCloud
```

#### 4. 使用 sed 命令自动添加规则
```bash
# 找到规则部分行号
grep -n "^rules:" "/Users/comdir/Library/Application Support/io.github.clash-verge-rev.clash-verge-rev/clash-verge.yaml"

# 在规则部分添加 Monica 规则（假设 rules: 在第 664 行）
sed -i '' '665i\
- DOMAIN-SUFFIX,monica.im,最萌の云 - CuteCloud
' "/Users/comdir/Library/Application Support/io.github.clash-verge-rev.clash-verge-rev/clash-verge.yaml"
```

#### 5. 验证规则添加成功
```bash
grep -A 5 -B 5 "monica.im" "/Users/comdir/Library/Application Support/io.github.clash-verge-rev.clash-verge-rev/clash-verge.yaml"
```

#### 6. 测试连接
```bash
curl -v --connect-timeout 10 https://monica.im
```

### 方法二：临时禁用代理（备选方案）
如果方法一不可行，可以临时禁用系统代理：
1. 打开系统偏好设置 → 网络
2. 选择当前网络连接 → 高级 → 代理
3. 取消勾选所有代理选项
4. 测试 Monica 连接

### 方法三：检查代理软件设置
1. 检查代理软件（如 Clash）的 TLS 处理设置
2. 尝试切换不同的代理节点
3. 检查代理软件的兼容性设置

## 诊断命令

### 检查网络连接
```bash
# 基本网络连接
ping -c 3 8.8.8.8

# DNS 解析
nslookup monica.im

# 系统代理设置
scutil --proxy

# 检查代理端口
lsof -i :7897
```

### 测试 TLS 连接
```bash
# 通过代理测试
curl -v --connect-timeout 10 https://monica.im

# 绕过代理测试
curl -v --noproxy "*" --connect-timeout 10 https://monica.im

# 使用 OpenSSL 测试
openssl s_client -connect monica.im:443 -servername monica.im
```

## 成功标志
- DNS 解析到 fake-ip 地址（如 198.18.0.22）
- TLS 握手成功完成
- 连接状态显示 "Connected to monica.im"
- Monica 应用恢复正常使用

## 注意事项
1. **备份配置文件**：修改前务必备份原配置
2. **重启应用**：配置修改后重启 Clash Verge 和 Monica
3. **规则优先级**：新添加的规则会优先匹配
4. **界面延迟**：Clash Verge 界面可能不会立即显示新规则，重启后正常

## 故障排除
- 如果规则不生效，检查代理组名称是否正确
- 如果连接仍有问题，尝试切换其他代理节点
- 如果配置文件损坏，使用备份文件恢复

## 相关文件
- 配置文件：`clash-verge.yaml`
- 备份文件：`clash-verge.yaml.backup`
- 日志文件：`~/Library/Application Support/io.github.clash-verge-rev.clash-verge-rev/logs/`

---
*最后更新：2024年9月24日*
*解决方案验证：✅ 成功*