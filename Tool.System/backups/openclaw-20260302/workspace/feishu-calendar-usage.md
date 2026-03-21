# 飞书日历功能使用说明

## 当前状态

OpenClaw 已配置飞书日历技能，可以创建和管理日历事件。

## 可用日历

### 共享日历：刘伟(openclaw)
- **日历ID**: `feishu.cn_XPhMNlWBS0qz08CnYIrb0g@group.calendar.feishu.cn`
- **用途**: OpenClaw 帮用户管理的日程
- **权限**: 用户有写入权限

## 使用方法

### 创建日程

```
node ~/.openclaw/workspace/skills/feishu-calendar/create.js \
  --summary "事件标题" \
  --start "2026-02-23T10:00:00" \
  --end "2026-02-23T12:00:00" \
  --desc "事件描述" \
  --calendar "feishu.cn_XPhMNlWBS0qz08CnYIrb0g@group.calendar.feishu.cn"
```

### 查看日程

```
node ~/.openclaw/workspace/skills/feishu-calendar/check.js
```

### 搜索日历

```
node ~/.openclaw/workspace/skills/feishu-calendar/search_cal.js
```

## 示例对话

用户说：
- "明天10点去顺德参观"
- "帮我创建一个日程，后天下午3点开会"
- "查看我下周的日程"

## 注意事项

1. **时间格式**: 使用 ISO 格式 `YYYY-MM-DDTHH:mm:ss`，例如 `2026-02-23T10:00:00`
2. **时区**: 默认使用 `Asia/Shanghai`
3. **日历ID**: 默认使用共享日历，如需指定可加 `--calendar` 参数

## 技术说明

### 配置文件位置
- 飞书凭证: `~/.openclaw/workspace/.env`
- 技能目录: `~/.openclaw/workspace/skills/feishu-calendar/`

### 凭证内容
```
FEISHU_APP_ID=cli_a913c55ee839dcd2
FEISHU_APP_SECRET=oO0CB8flBudXU5SEz2zBOe8GLiY4gdOo
```

### 已开通的飞书权限
- `calendar:calendar` - 日历基础权限
- `calendar:event:read` - 读取日历事件
- `calendar:event:write` - 写入日历事件
- `contact:contact.base:readonly` - 获取通讯录基本信息
- `cardkit:card:write` - 创建和更新卡片

## 限制

由于飞书 API 限制，Bot 无法直接访问用户的**个人日历**，只能：
1. 在 Bot 创建的共享日历中创建事件
2. 用户需要在飞书中订阅该共享日历才能在个人日历视图看到

如需访问用户个人日历，需要实现 OAuth 授权流程获取 `user_access_token`。
