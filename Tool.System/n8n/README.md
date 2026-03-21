# N8N 本地部署指南

N8N 是一个强大的工作流自动化工具，可以连接各种服务和API，实现自动化任务。

## 📋 目录

- [快速开始](#快速开始)
- [安装方式](#安装方式)
- [配置说明](#配置说明)
- [使用说明](#使用说明)
- [常见问题](#常见问题)
- [进阶配置](#进阶配置)

## 🚀 快速开始

### 方式一：Docker 方式（推荐）

#### 前置要求
- 安装 [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop)

#### 启动步骤

1. **双击运行启动脚本**
   ```
   双击 "启动N8N.command"
   ```

2. **或使用命令行**
   ```bash
   cd /Users/comdir/SynologyDrive/0050Project/Tool.System/n8n
   docker-compose up -d
   ```

3. **访问 N8N**
   - 地址: http://localhost:5678
   - 默认用户名: `admin`
   - 默认密码: `admin123`

### 方式二：npm 方式

```bash
# 全局安装
npm install -g n8n

# 启动
n8n start

# 自定义端口启动
n8n start --port 5678
```

## ⚙️ 配置说明

### 环境变量 (.env)

```env
# 基本认证
N8N_BASIC_AUTH_USER=admin              # 登录用户名
N8N_BASIC_AUTH_PASSWORD=admin123       # 登录密码

# 主机配置
N8N_HOST=localhost                     # 主机地址
WEBHOOK_URL=http://localhost:5678/     # Webhook地址

# 时区
TIMEZONE=Asia/Shanghai                 # 时区设置
```

### 重要配置项

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `N8N_PORT` | 服务端口 | 5678 |
| `N8N_BASIC_AUTH_ACTIVE` | 启用基本认证 | true |
| `EXECUTIONS_DATA_PRUNE` | 自动清理执行数据 | true |
| `EXECUTIONS_DATA_MAX_AGE` | 数据保留天数 | 168 (7天) |

## 📖 使用说明

### 启动服务

```bash
# 使用启动脚本
双击 "启动N8N.command"

# 或使用命令行
docker-compose up -d
```

### 停止服务

```bash
# 使用停止脚本
双击 "停止N8N.command"

# 或使用命令行
docker-compose down
```

### 查看日志

```bash
# 使用日志脚本
双击 "查看日志.command"

# 或使用命令行
docker-compose logs -f n8n
```

### 重启服务

```bash
docker-compose restart
```

### 更新 N8N

```bash
# 拉取最新镜像
docker-compose pull

# 重启服务
docker-compose up -d
```

## 🎯 常见用途

### 1. 自动化工作流
- 定时任务执行
- 数据同步
- API集成

### 2. Webhook 触发
- 接收外部事件
- 处理HTTP请求
- 触发自动化流程

### 3. 数据处理
- 数据转换
- 数据聚合
- 数据分发

## 📁 目录结构

```
n8n/
├── docker-compose.yml      # Docker编排配置
├── .env                    # 环境变量配置
├── .env.example            # 环境变量示例
├── .gitignore             # Git忽略文件
├── n8n_data/              # N8N数据目录（自动创建）
├── local_files/           # 本地文件目录（自动创建）
├── 启动N8N.command        # 启动脚本
├── 停止N8N.command        # 停止脚本
├── 查看日志.command       # 日志查看脚本
└── README.md              # 本文件
```

## ❓ 常见问题

### 1. 无法访问 http://localhost:5678

**原因**: 
- Docker 未启动
- 端口被占用
- 服务启动失败

**解决方案**:
```bash
# 检查 Docker 状态
docker ps

# 检查端口占用
lsof -i :5678

# 查看日志
docker-compose logs n8n
```

### 2. 忘记密码

**解决方案**:
1. 停止服务: `docker-compose down`
2. 修改 `.env` 文件中的密码
3. 重新启动: `docker-compose up -d`

### 3. 数据持久化

数据存储在 `n8n_data/` 目录，包括:
- 工作流定义
- 凭证信息
- 执行历史

**备份数据**:
```bash
# 备份整个数据目录
cp -r n8n_data/ n8n_data_backup_$(date +%Y%m%d)

# 或使用 Docker 卷备份
docker run --rm -v n8n_n8n_data:/data -v $(pwd):/backup alpine tar czf /backup/n8n_backup.tar.gz /data
```

### 4. 性能优化

**增加资源限制** (修改 docker-compose.yml):
```yaml
services:
  n8n:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
```

## 🔧 进阶配置

### 使用 PostgreSQL 数据库

1. 取消 `docker-compose.yml` 中 PostgreSQL 部分的注释
2. 在 `.env` 中启用数据库配置
3. 重启服务

### 配置 HTTPS

使用反向代理（如 Nginx）配置 HTTPS:

```nginx
server {
    listen 443 ssl;
    server_name n8n.example.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:5678;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 外网访问

1. 修改 `.env`:
   ```env
   N8N_HOST=your-domain.com
   WEBHOOK_URL=https://your-domain.com/
   ```

2. 配置防火墙开放 5678 端口

3. 使用反向代理配置域名和 HTTPS

## 📚 相关资源

- [N8N 官方文档](https://docs.n8n.io/)
- [N8N 工作流社区](https://n8n.io/workflows)
- [N8N GitHub](https://github.com/n8n-io/n8n)
- [N8N 中文教程](https://docs.n8n.io/getting-started/)

## 🆘 获取帮助

- [官方社区论坛](https://community.n8n.io/)
- [GitHub Issues](https://github.com/n8n-io/n8n/issues)
- [Discord 社区](https://discord.gg/n8n)

## 📝 注意事项

1. **安全性**
   - 修改默认密码
   - 不要暴露到公网（除非配置了 HTTPS）
   - 定期更新 N8N 版本

2. **数据备份**
   - 定期备份 `n8n_data/` 目录
   - 重要工作流导出保存

3. **资源使用**
   - 监控 Docker 容器资源使用
   - 定期清理执行历史数据

## 📄 许可证

N8N 使用 Apache 2.0 许可证开源


