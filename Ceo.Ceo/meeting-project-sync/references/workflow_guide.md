# 会议-项目同步工作流

## 完整工作流程

```
会议纪要 → 解析提取 → 项目同步 → 任务跟踪 → 下次会议
```

## 详细步骤

### 步骤1: 准备会议纪要

**输入格式**: Markdown, TXT, DOCX, PDF

**推荐结构**:
1. 会议基本信息(标题、日期、参与者)
2. 讨论内容(分主题)
3. 决策事项(明确标注"决定"、"批准"等)
4. 待办任务(使用复选框或编号)
5. 下次会议建议

### 步骤2: 解析会议纪要

**使用脚本**: `scripts/parse_meeting.py`

**命令**:
```bash
python parse_meeting.py meeting_notes.md json
```

**输出**:
- `meeting_notes_parsed.json` - 结构化数据
- 或 `meeting_notes_tasks.md` - 任务清单

**提取内容**:
- ✅ 决策事项(带分类和优先级)
- ✅ 待办任务(带负责人和截止日期)
- ✅ 下次会议建议
- ✅ 讨论主题

### 步骤3: 同步到项目

**使用脚本**: `scripts/sync_project.py`

**命令**:
```bash
# 生成项目JSON
python sync_project.py meeting_notes_parsed.json "项目名称" json

# 生成看板
python sync_project.py meeting_notes_parsed.json "项目名称" kanban

# 生成甘特图
python sync_project.py meeting_notes_parsed.json "项目名称" gantt
```

**输出**:
- `meeting_notes_project.json` - 项目数据
- `meeting_notes_kanban.md` - 项目看板
- `meeting_notes_gantt.md` - 甘特图

### 步骤4: 任务跟踪

**项目看板包含**:
- 📋 待办任务
- 🚀 进行中任务
- ✅ 已完成任务
- 🎯 项目里程碑
- 📌 下次会议准备

**每个任务包含**:
- 任务ID (TASK-1000, TASK-1001...)
- 标题和描述
- 负责人
- 截止日期
- 优先级 (P0高/P1中/P2低)
- 状态
- 标签

### 步骤5: 准备下次会议

**基于输出的"下次会议准备"部分**:
- 检查任务完成情况
- 准备必要材料
- 确定参与者
- 安排会议时间

## 快速使用指南

### 场景1: 首次使用

```bash
# 1. 解析会议纪要并生成任务清单
python scripts/parse_meeting.py meeting.md markdown

# 2. 查看任务清单
cat meeting_tasks.md

# 3. 同步到项目看板
python scripts/sync_project.py meeting_parsed.json "Q1产品开发" kanban

# 4. 查看项目看板
cat meeting_kanban.md
```

### 场景2: 持续项目更新

```bash
# 每次会议后
python scripts/parse_meeting.py weekly_meeting.md json
python scripts/sync_project.py weekly_meeting_parsed.json "项目名称" kanban

# 更新现有项目(手动合并任务)
```

### 场景3: 导出给团队

```bash
# 生成所有格式
python scripts/parse_meeting.py meeting.md json
python scripts/parse_meeting.py meeting.md markdown
python scripts/sync_project.py meeting_parsed.json "项目" json
python scripts/sync_project.py meeting_parsed.json "项目" kanban
python scripts/sync_project.py meeting_parsed.json "项目" gantt

# 分发文件
- meeting_tasks.md → 发给团队成员
- meeting_kanban.md → 导入项目管理工具
- meeting_gantt.md → 用于时间规划
```

## 集成到现有工具

### 集成到Notion

1. 解析会议纪要生成Markdown
2. 复制Markdown内容到Notion页面
3. Notion会自动渲染复选框和格式

### 集成到Jira/Asana

1. 生成JSON格式项目数据
2. 使用API导入任务
3. 或手动根据看板创建任务

### 集成到GitHub Projects

1. 生成Markdown看板
2. 转换为GitHub Issues
3. 添加到Project Board

### 集成到Slack

1. 解析会议生成任务清单
2. 发送到Slack频道
3. 团队成员可直接查看待办

## 自动化建议

### 使用Cron定期处理

```bash
# 每天下午5点处理当天的会议纪要
0 17 * * * /path/to/process_meetings.sh
```

### 使用Git Hooks

会议纪要提交到Git时自动解析:

```bash
#!/bin/bash
# .git/hooks/post-commit

if git diff-tree --no-commit-id --name-only -r HEAD | grep -q "meetings/"; then
    python scripts/parse_meeting.py meetings/latest.md json
fi
```

## 故障排除

### 问题1: 任务未被识别

**原因**: 任务格式不标准

**解决**:
- 使用 `- [ ]` 或编号列表
- 明确标注 @负责人
- 使用标准日期格式

### 问题2: 决策未提取

**原因**: 缺少决策关键词

**解决**:
- 使用"决定"、"批准"、"确定"等词
- 单独列出决策部分
- 使用加粗或标题突出

### 问题3: 中文日期解析错误

**原因**: 日期格式多样

**解决**:
- 使用标准格式: YYYY-MM-DD
- 或明确标注"本周"、"下周"
- 避免模糊表达"尽快"

## 扩展功能

### 添加邮件通知

在脚本中添加邮件发送功能,自动通知任务负责人。

### 添加周期性提醒

设置Cron任务,在截止日期前提醒负责人。

### 集成AI总结

使用Claude API对会议纪要进行智能总结和风险识别。

### 数据可视化

生成任务完成率、成员工作量等统计图表。
