# Claude Code 全局配置共享

通过 Synology Drive 在多台电脑间共享 Claude Code 的全局配置。

## 目录结构

```
~/.claude → Tool.System/dot_claude/
├── CLAUDE.md          ← 全局配置（项目缩写、SSH、技能等）
├── commands/          ← 全局 Skills
├── skills/            ← 自定义技能
└── settings.json      ← Claude Code 设置
```

## 首次在新电脑上配置

### 步骤 1：创建软链接

```bash
# 如果已有 .claude 目录，先备份
mv ~/.claude ~/.claude.backup

# 创建软链接（假设 SynologyDrive 挂载在 /Users/你的用户名/SynologyDrive）
ln -s /Users/$(whoami)/SynologyDrive/0050Project/Tool.System/dot_claude ~/.claude
```

### 步骤 2：合并配置（首次使用）

如果你之前在另一台电脑有自己的 `CLAUDE.md`，需要手动合并：

1. 打开备份的旧配置：`~/.claude.backup/CLAUDE.md`
2. 打开共享配置：`~/.claude/CLAUDE.md`
3. 把旧配置中独有的内容合并到共享配置中
4. 删除备份：`rm -rf ~/.claude.backup`

### 步骤 3：配置 SSH（如需访问腾讯工蜂）

```bash
# 复制密钥
cp /Users/$(whoami)/SynologyDrive/0050Project/Tool.System/ssh_keys/id_rsa_gw* ~/.ssh/

# 设置权限
chmod 600 ~/.ssh/id_rsa_gw
chmod 644 ~/.ssh/id_rsa_gw.pub

# 添加 SSH 配置
cat >> ~/.ssh/config << 'EOF'
Host git.code.tencent.com
    HostKeyAlgorithms +ssh-rsa
    PubkeyAcceptedAlgorithms +ssh-rsa
    IdentityFile ~/.ssh/id_rsa_gw
EOF
```

## 注意事项

- **不要同时编辑**：两台电脑同时修改配置会产生冲突
- **定期同步**：确保 Synology Drive 正常同步后再编辑
- **冲突处理**：如果 Synology Drive 报告冲突，手动合并两个版本

## 共享内容包括

- 项目缩写映射（gkb、gc、ts 等）
- SSH 配置信息
- 全局 Skills（/tencent-ssh、/meeting 等）
- Claude Code 设置
