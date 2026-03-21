# SSH 密钥

用于访问腾讯工蜂 git.code.tencent.com

## 文件说明

| 文件 | 用途 | 权限 |
|------|------|------|
| id_rsa_gw | 私钥（保密） | 600 |
| id_rsa_gw.pub | 公钥 | 644 |

## 在新电脑上使用

```bash
# 1. 复制文件到 ~/.ssh/
cp id_rsa_gw id_rsa_gw.pub ~/.ssh/

# 2. 设置权限
chmod 600 ~/.ssh/id_rsa_gw
chmod 644 ~/.ssh/id_rsa_gw.pub

# 3. 添加 SSH 配置（如果 ~/.ssh/config 不存在则创建）
cat >> ~/.ssh/config << 'EOF'
Host git.code.tencent.com
    HostKeyAlgorithms +ssh-rsa
    PubkeyAcceptedAlgorithms +ssh-rsa
    IdentityFile ~/.ssh/id_rsa_gw
EOF

# 4. 测试连接
ssh -T git@git.code.tencent.com
```

## 安全提醒

- 私钥文件不要分享给不信任的人
- 不要上传到公开仓库
