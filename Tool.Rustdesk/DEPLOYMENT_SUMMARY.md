# Rustdesk 中继服务器部署总结

## 项目概述
本项目为在服务器 `op.gaowei.com` 上部署 Rustdesk 中继服务器，避免与现有端口 5000, 80, 5001 冲突。

## 文件说明

| 文件名 | 用途 | 说明 |
|--------|------|------|
| `quick_deploy.sh` | 一键部署脚本 | 推荐使用，包含完整的错误检查和自动配置 |
| `deploy_rustdesk.sh` | 基础部署脚本 | 简单的部署脚本 |
| `manage_rustdesk.sh` | 服务管理脚本 | 用于日常维护和监控 |
| `upload_and_deploy.bat` | Windows上传工具 | 自动上传脚本到服务器 |
| `client_config_guide.md` | 客户端配置指南 | 详细的客户端配置说明 |
| `README.md` | 详细部署文档 | 完整的部署和配置说明 |

## 快速部署步骤

### 方法一：使用 Windows 批处理（推荐）
1. 双击运行 `upload_and_deploy.bat`
2. 脚本会自动上传部署文件到服务器
3. 按提示手动连接SSH执行部署

### 方法二：手动部署
1. 上传脚本到服务器：
   ```bash
   scp quick_deploy.sh root@op.gaowei.com:/tmp/
   ```

2. 连接服务器：
   ```bash
   ssh root@op.gaowei.com
   ```

3. 执行部署：
   ```bash
   chmod +x /tmp/quick_deploy.sh
   /tmp/quick_deploy.sh
   ```

## 端口分配

| 服务 | 端口 | 协议 | 用途 |
|------|------|------|------|
| hbbs | 21115 | TCP | 信令服务器 |
| hbbs | 21116 | TCP/UDP | NAT类型测试 |
| hbbr | 21117 | TCP | 中继服务器 |
| hbbr | 21119 | TCP | 中继服务器 |

## 部署后验证

1. **检查服务状态**：
   ```bash
   cd /opt/rustdesk
   docker-compose ps
   ```

2. **检查端口监听**：
   ```bash
   netstat -tlnp | grep -E ':(21115|21116|21117|21119)'
   ```

3. **获取公钥**：
   ```bash
   cat /opt/rustdesk/data/id_ed25519.pub
   ```

## 客户端配置

配置参数：
- **ID服务器**: `op.gaowei.com:21115`
- **中继服务器**: `op.gaowei.com:21117`
- **公钥**: 从服务器获取的公钥内容

详细配置步骤请参考 `client_config_guide.md`

## 日常管理

上传管理脚本到服务器：
```bash
scp manage_rustdesk.sh root@op.gaowei.com:/usr/local/bin/
ssh root@op.gaowei.com "chmod +x /usr/local/bin/manage_rustdesk.sh"
```

常用管理命令：
```bash
# 查看状态
manage_rustdesk.sh status

# 查看日志
manage_rustdesk.sh logs

# 重启服务
manage_rustdesk.sh restart

# 更新服务
manage_rustdesk.sh update

# 备份配置
manage_rustdesk.sh backup

# 监控服务
manage_rustdesk.sh monitor
```

## 防火墙配置

如果服务器启用了防火墙，需要开放以下端口：

**UFW**：
```bash
sudo ufw allow 21115
sudo ufw allow 21116
sudo ufw allow 21117
sudo ufw allow 21119
```

**iptables**：
```bash
iptables -A INPUT -p tcp --dport 21115 -j ACCEPT
iptables -A INPUT -p tcp --dport 21116 -j ACCEPT
iptables -A INPUT -p udp --dport 21116 -j ACCEPT
iptables -A INPUT -p tcp --dport 21117 -j ACCEPT
iptables -A INPUT -p tcp --dport 21119 -j ACCEPT
```

## 故障排除

### 常见问题

1. **端口冲突**：
   - 检查端口占用：`netstat -tlnp | grep :端口号`
   - 修改 docker-compose.yml 中的端口映射

2. **服务无法启动**：
   - 查看日志：`docker-compose logs`
   - 检查 Docker 服务状态
   - 确认镜像拉取成功

3. **客户端无法连接**：
   - 检查防火墙设置
   - 验证公钥配置
   - 确认服务器地址和端口

### 日志位置
- Docker 容器日志：`docker-compose logs`
- 管理脚本日志：`/var/log/rustdesk_manage.log`

## 安全建议

1. **定期更新**：定期更新 Rustdesk 镜像
2. **备份密钥**：定期备份 `/opt/rustdesk/data` 目录
3. **监控日志**：定期检查服务日志
4. **网络安全**：配置适当的防火墙规则
5. **访问控制**：限制管理端口的访问来源

## 性能优化

1. **资源限制**：在 docker-compose.yml 中添加资源限制
2. **日志轮转**：配置日志轮转避免磁盘空间不足
3. **监控告警**：设置服务监控和告警

## 联系信息

- Rustdesk 官网：https://rustdesk.com/
- GitHub 项目：https://github.com/rustdesk/rustdesk
- 文档：https://rustdesk.com/docs/

## 部署检查清单

- [ ] 服务器连接正常
- [ ] Docker 环境可用
- [ ] 端口无冲突
- [ ] 脚本上传成功
- [ ] 部署脚本执行成功
- [ ] 服务状态正常
- [ ] 端口监听正常
- [ ] 公钥生成成功
- [ ] 防火墙配置完成
- [ ] 客户端配置测试
- [ ] 管理脚本部署
- [ ] 备份策略制定

---

**注意**：请保存好服务器生成的公钥，这是客户端连接必需的。建议将公钥和服务器信息记录在安全的地方。