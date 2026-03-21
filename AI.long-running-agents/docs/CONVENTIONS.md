# 项目命名规范

## 目录结构

所有项目存放在 `~/SynologyDrive/0050Project/` 目录下。

## 命名格式

```
前缀.项目名
```

- 使用点号 `.` 分隔前缀和项目名
- 项目名使用 PascalCase（首字母大写）

## 前缀分类

| 前缀 | 用途 | 示例 |
|------|------|------|
| `AI.` | AI/机器学习相关项目 | AI.long-running-agents |
| `GW.` | 高维业务相关项目 | GW.KnowledgeBase, GW.Trackr |
| `LW.` | 品牌合作项目 | LW.Reading, LW.wxWaterMark |
| `Tool.` | 工具类项目 | Tool.System, Tool.Docs |
| `Game.` | 游戏项目 | Game.Brick, Game.NockCar |
| `Learn.` | 学习/教学相关 | Learn.Html |
| `Ceo.` | CEO 相关项目 | Ceo.Ceo |
| `GitHub.` | GitHub 克隆/研究项目 | GitHub.interactive-feedback-mcp |
| `Dream.` | 创意/实验项目 | Dream.Boom |
| `Lesson.` | 课程相关 | Lesson.Holacracy |

## 项目名命名原则

1. **简洁有力** - 1-2 个单词
2. **描述功能** - 能从名字看出项目用途
3. **英文为主** - 使用英文，避免中文和拼音
4. **避免数字** - 除非有特殊含义

## 示例

```
博客系统     → GW.Blog 或 Tool.Blog
用户管理 API → GW.UserAPI
数据分析工具 → GW.DataAnalysis
学习地图     → GW.LearnMap
知识库       → GW.KnowledgeBase
```

## 创建新项目时

系统会根据项目描述自动生成 3-4 个命名建议，用户可以：
1. 选择其中一个建议
2. 输入自定义名称
3. 使用默认建议
