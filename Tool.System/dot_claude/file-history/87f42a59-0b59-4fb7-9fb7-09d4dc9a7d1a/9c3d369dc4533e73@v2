# Tencent-SSH: 添加 SSH Key 到腾讯工蜂

帮助用户将本地 SSH 公钥添加到腾讯工蜂 (git.code.tencent.com)。

## 触发方式

- `/tencent-ssh`
- 用户说 "添加 SSH key"、"配置腾讯工蜂 SSH" 等

## 处理流程

### 步骤1: 检查现有 SSH Key

```bash
ls -la ~/.ssh/*.pub 2>/dev/null || echo "未找到现有 SSH 公钥"
```

列出用户现有的公钥，让用户选择使用哪个，或生成新的。

### 步骤2: 选择或生成 Key

**使用现有 Key:**
- 显示公钥内容供用户复制
- 默认推荐使用 `id_rsa_gw.pub`（高维通用 Key）

**生成新 Key:**
```bash
ssh-keygen -t rsa -b 4096 -C "用户邮箱" -f ~/.ssh/id_rsa_tencent_new
```

### 步骤3: 打开腾讯工蜂并复制公钥

```bash
# 打开添加页面
open "https://git.code.tencent.com/profile/keys/new"

# 复制公钥到剪贴板
cat ~/.ssh/id_rsa_gw.pub | pbcopy
```

### 步骤4: 引导用户填写

在打开的页面中：
1. **Title** - 建议格式: `设备名-日期`（如 `WEIMacBook-20240228`）
2. **Key** - 已复制到剪贴板，直接 `⌘V` 粘贴
3. **Expires at** - 可选设置过期时间
4. 点击 **Add key** 按钮

### 步骤5: 测试连接

```bash
ssh -T git@git.code.tencent.com 2>&1
```

成功标志: `Authenticated to git.code.tencent.com using "publickey"`

### 步骤6: 配置 SSH Config

确保 `~/.ssh/config` 包含腾讯工蜂配置：

```
Host git.code.tencent.com
    HostKeyAlgorithms +ssh-rsa
    PubkeyAcceptedAlgorithms +ssh-rsa
    IdentityFile ~/.ssh/id_rsa_gw
```

## 常见问题

**Q: 提示 "shell request failed on channel 0"**
A: 这是正常的，Git 服务器不支持交互式 shell，只要看到 authenticated 即表示成功。

**Q: 权限被拒绝 (Permission denied)**
A: 检查：
1. 公钥是否正确添加到腾讯工蜂
2. SSH config 中的 IdentityFile 路径是否正确
3. 私钥文件权限是否为 600

## 相关文件

- SSH 配置: `~/.ssh/config`
- 默认公钥: `~/.ssh/id_rsa_gw.pub`
- 腾讯工蜂 SSH 页面: https://git.code.tencent.com/profile/keys

$ARGUMENTS
