---
name: meeting-project-sync
description: "会议记录与项目管理协同系统。解析会议纪要自动提取决策、待办任务和下次会议建议,并同步到项目管理格式(看板、甘特图)。当用户需要: (1) 导入会议纪要并生成项目任务, (2) 将会议讨论转化为可执行的待办事项, (3) 追踪会议决策的执行情况, (4) 准备下次会议材料, (5) 建立会议与项目的协同推进机制时使用此技能。支持Markdown/Word/PDF格式输入,输出JSON/Markdown看板/甘特图等多种格式。"
---

# 会议-项目同步系统

快速将会议纪要转换为结构化的项目任务,实现会议与项目管理的无缝衔接。

## 核心功能

1. **智能解析会议纪要** - 自动识别决策、任务、建议
2. **项目任务同步** - 转换为项目管理格式(看板/甘特图)
3. **任务智能分类** - 自动分配优先级和标签
4. **进度跟踪** - 建立从会议到执行的完整链路

## 使用方法

### 基础工作流

**步骤1: 解析会议纪要**

```bash
python scripts/parse_meeting.py <会议纪要文件> [json|markdown]
```

输出:
- JSON格式: 结构化的会议数据
- Markdown格式: 人类可读的任务清单

**步骤2: 同步到项目**

```bash
python scripts/sync_project.py <解析JSON> [项目名称] [json|kanban|gantt]
```

输出:
- JSON: 完整的项目数据结构
- Kanban: 项目看板(待办/进行中/完成)
- Gantt: 甘特图时间规划

### 快速开始示例

```bash
# 完整流程演示
python scripts/parse_meeting.py meeting.md json
python scripts/sync_project.py meeting_parsed.json "Q1产品开发" kanban
```

## 会议纪要格式要求

### 推荐结构

会议纪要应包含以下部分以获得最佳解析效果:

```markdown
# 会议标题

**日期**: 2025-01-20
**参会人员**: 张三, 李四, 王五

## 讨论内容

### 主题1
讨论要点...

**决策**: 决定采用方案A

### 主题2
讨论要点...

## 待办任务

- [ ] 任务描述 @负责人 ⏰ 截止日期
- [ ] 任务描述 @负责人 ⏰ 本周五

## 下次会议

建议时间: 下周五
建议议程: ...
```

### 关键词识别

系统自动识别以下关键词:

**决策**: 决定、决策、批准、同意、确定、定为、决议
**任务**: 使用 `- [ ]` 复选框、编号列表、或包含"任务"、"待办"、"负责"等词
**建议**: 建议、提议、下次、后续、跟进、下周、下一步

**详细格式说明**: 查看 `references/meeting_templates.md`

## 输出格式说明

### 1. 解析结果 (JSON)

```json
{
  "meeting_info": {
    "title": "会议标题",
    "date": "2025-01-20",
    "participants": ["张三", "李四"]
  },
  "decisions": [
    {
      "content": "决策内容",
      "priority": "high|medium|normal",
      "category": "strategic|technical|financial|personnel|general"
    }
  ],
  "tasks": [
    {
      "description": "任务描述",
      "assignee": "负责人",
      "deadline": "截止日期",
      "priority": "high|medium|normal"
    }
  ],
  "next_meeting_suggestions": [
    {
      "content": "建议内容",
      "type": "meeting_logistics|preparation|participants|general"
    }
  ]
}
```

### 2. 任务清单 (Markdown)

包含:
- 会议信息汇总
- 决策事项列表(带优先级和分类)
- 待办任务清单(带负责人和截止日期)
- 下次会议建议
- 讨论主题

### 3. 项目看板 (Kanban)

按列组织任务:
- 📋 待办 - 新创建的任务
- 🚀 进行中 - 正在执行的任务
- ✅ 已完成 - 完成的任务
- 🎯 里程碑 - 关键决策点
- 📌 下次会议准备 - 后续行动项

每个任务包含:
- 任务ID (TASK-1000)
- 优先级标记 (🔴P0 🟡P1 🟢P2)
- 负责人 (@名字)
- 截止日期 (⏰ 日期)
- 标签 (development, design, testing等)

### 4. 甘特图 (Mermaid)

时间线格式,可在Markdown中直接渲染或导入项目管理工具。

## 高级功能

### 任务智能分类

系统自动为任务分配标签:
- `development` - 开发相关
- `design` - 设计相关
- `testing` - 测试相关
- `documentation` - 文档相关
- `meeting` - 会议相关
- `research` - 研究调研
- `deployment` - 部署发布
- `bug` - 问题修复

### 优先级判断

自动判断任务优先级:
- **P0 (高)**: 包含"紧急"、"重要"、"优先"、"立即"
- **P1 (中)**: 包含"尽快"、"本周"、"重点"
- **P2 (低)**: 其他任务

### 截止日期标准化

智能解析相对日期:
- "本周" → 本周五
- "下周" → 下周五
- "本月底" → 当月最后一天
- 支持标准日期格式 (YYYY-MM-DD)

### 决策分类

自动分类决策类型:
- `strategic` - 战略方向
- `technical` - 技术方案
- `financial` - 财务预算
- `personnel` - 人员调动
- `general` - 一般决策

## 集成建议

### 与现有工具集成

**Notion/Confluence**: 复制Markdown输出直接粘贴

**Jira/Asana**: 使用JSON数据通过API批量创建任务

**GitHub Projects**: 将任务转换为Issues并添加到Project Board

**Slack/企业微信**: 分享任务清单到团队频道

### 自动化工作流

**Git Hook集成**: 
```bash
# 提交会议纪要时自动解析
.git/hooks/post-commit
```

**定时任务**:
```bash
# 每天自动处理新的会议纪要
crontab: 0 17 * * * /path/to/process_meetings.sh
```

**邮件提醒**: 在脚本中添加邮件功能,自动通知任务负责人

## 示例使用场景

### 场景1: 周会后的任务分配

```bash
# 解析周会纪要
python scripts/parse_meeting.py weekly_meeting.md markdown

# 查看任务清单并分发给团队
cat weekly_meeting_tasks.md

# 生成项目看板
python scripts/sync_project.py weekly_meeting_parsed.json "周度项目" kanban
```

### 场景2: 季度规划会议

```bash
# 解析季度规划会议
python scripts/parse_meeting.py q1_planning.md json

# 生成完整项目结构
python scripts/sync_project.py q1_planning_parsed.json "Q1产品规划" json

# 生成甘特图用于时间规划
python scripts/sync_project.py q1_planning_parsed.json "Q1产品规划" gantt
```

### 场景3: 持续项目跟进

每次会议后重复运行脚本,手动合并新任务到现有项目,或使用版本控制跟踪变化。

## 参考资料

- `references/meeting_templates.md` - 会议纪要模板和格式指南
- `references/workflow_guide.md` - 完整工作流程和故障排除
- `assets/example_meeting.md` - 标准会议纪要示例

## 脚本说明

### parse_meeting.py

解析会议纪要,提取结构化信息。

**参数**:
- `<会议纪要文件>` - 输入文件路径
- `[输出格式]` - json 或 markdown (默认json)

**输出**:
- JSON: `<文件名>_parsed.json`
- Markdown: `<文件名>_tasks.md`

### sync_project.py

将解析结果转换为项目管理格式。

**参数**:
- `<解析JSON>` - parse_meeting.py的JSON输出
- `[项目名称]` - 可选,默认使用会议标题
- `[输出格式]` - json, kanban, 或 gantt (默认json)

**输出**:
- JSON: `<文件名>_project.json`
- Kanban: `<文件名>_kanban.md`
- Gantt: `<文件名>_gantt.md`

## 最佳实践

1. **使用Markdown格式** - 结构清晰,易于解析
2. **明确任务分配** - 使用 @负责人 标记
3. **标准化日期** - 使用YYYY-MM-DD或"本周"、"下周"
4. **清晰的决策记录** - 使用"决定"、"批准"等关键词
5. **结构化组织** - 使用标题、列表分段
6. **及时处理** - 会议结束后尽快解析纪要

## 故障排除

**问题**: 任务未被识别
**解决**: 使用 `- [ ]` 或编号列表,明确标注@负责人

**问题**: 决策未提取
**解决**: 使用"决定"、"批准"等关键词,单独列出决策部分

**问题**: 中文日期解析错误
**解决**: 使用YYYY-MM-DD格式,或明确"本周"、"下周"

更多帮助请查看 `references/workflow_guide.md`
