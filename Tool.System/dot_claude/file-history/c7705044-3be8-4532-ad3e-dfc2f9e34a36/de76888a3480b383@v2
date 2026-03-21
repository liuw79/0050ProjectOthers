# Claude Remote - 飞书远程控制 Claude Code

通过飞书手机客户端远程操作电脑上的 Claude Code。

## 快速开始

### 1. 启动服务

```bash
cd /Users/comdir/SynologyDrive/0050Project/Tool.System/claude-remote
./scripts/start.sh
```

启动后会显示：
- 公网地址（用于飞书事件订阅）
- 当前状态

### 2. 配置飞书应用

启动服务后，需要完成以下飞书应用配置：

#### 2.1 启用机器人能力

1. 打开 https://open.feishu.cn/app/cli_a91c59780ff89ced
2. 左侧菜单 → 应用功能 → 机器人
3. 启用机器人
4. 设置机器人名称和描述

#### 2.2 配置权限

左侧菜单 → 权限管理，开通以下权限：

| 权限 | 用途 |
|------|------|
| `im:message` | 获取用户发给机器人的消息 |
| `im:message:send_as_bot` | 以机器人身份发送消息 |

#### 2.3 配置事件订阅

1. 左侧菜单 → 事件订阅
2. 启用事件订阅
3. 请求网址填写：`https://xxxx.trycloudflare.com/webhook`
   （启动服务后会显示具体地址）
4. 添加事件：
   - `im.message.receive_v1` - 接收消息

#### 2.4 发布版本

1. 左侧菜单 → 版本管理与发布
2. 创建版本并发布
3. 在企业内可用

### 3. 使用方式

在飞书中找到机器人，发送消息即可：

```
/status      - 查看当前项目
/projects    - 列出所有项目
/kb          - 切换到知识库
你好 Claude  - 直接发消息给 Claude
```

## 命令列表

| 命令 | 说明 |
|------|------|
| `/status` | 查看当前项目状态 |
| `/projects` | 列出所有可用项目 |
| `/kb` `/gc` `/ts` 等 | 切换到对应项目 |
| `/history [数量]` | 查看历史记录 |
| `/help` | 显示帮助 |
| 直接发送文字 | 发送消息给 Claude |

## 项目缩写

```
kb     → GW.KnowledgeBase (知识库)
gc     → GW.Content (内容)
ts/sys → Tool.System (系统工具)
... 更多见 config/projects.json
```

## 停止服务

```bash
./scripts/stop.sh
```

## 故障排除

### 问题：消息没有响应

1. 检查服务是否运行：访问 `http://localhost:3000/health`
2. 检查 cloudflared 是否运行：`ps aux | grep cloudflared`
3. 检查飞书事件订阅是否配置正确
4. 检查飞书应用权限是否开通

### 问题：cloudflared 无法启动

```bash
# 手动启动测试
cloudflared tunnel --url http://localhost:3000
```

### 问题：飞书 webhook 验证失败

确保 URL 格式正确：`https://xxx.trycloudflare.com/webhook`

## 文件结构

```
claude-remote/
├── src/
│   ├── index.js      # 主服务入口
│   ├── claude.js     # Claude CLI 封装
│   ├── session.js    # 会话管理
│   └── commands.js   # 命令解析
├── config/
│   ├── projects.json # 项目配置
│   └── .env          # 环境变量
├── scripts/
│   ├── start.sh      # 启动脚本
│   └── stop.sh       # 停止脚本
└── README.md
```

## 安全提示

- `.env` 文件包含敏感信息，请勿提交到 git
- 飞书机器人仅响应配置的权限范围内的请求
- 建议定期更换 App Secret
