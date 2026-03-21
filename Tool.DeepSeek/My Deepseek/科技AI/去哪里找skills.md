---
title: 去哪里找skills
category: 科技AI
tags: [科技AI, 推荐, 问题]
source: DeepSeek
messages: 4
processed: 2026-02-20
---
## User

去哪里找skills

## Assistant

你好！“去哪里找skills”这个问题

## User

去哪里找claude code的skills

## Assistant

寻找和获取Claude Code的Skills（技能）主要有以下几种途径，你可以根据自身需求选择。

### 🗂️ 官方技能库

Claude官方提供预置技能包，可以通过插件市场直接安装，非常方便：

- 安装方式：在Claude Code中输入命令 /plugin marketplace add anthropics/skills 添加官方市场，然后安装所需技能包-5。

安装方式：在Claude Code中输入命令 /plugin marketplace add anthropics/skills 添加官方市场，然后安装所需技能包-5。

- 核心包内容：document-skills：包含处理Word文档(docx)、Excel表格(xlsx)、PowerPoint演示文稿(pptx)的技能-5。example-skills：包含网页测试、MCP服务器构建、前端设计、品牌指南应用等十多个示例技能-5。

核心包内容：

- document-skills：包含处理Word文档(docx)、Excel表格(xlsx)、PowerPoint演示文稿(pptx)的技能-5。

document-skills：包含处理Word文档(docx)、Excel表格(xlsx)、PowerPoint演示文稿(pptx)的技能-5。

- example-skills：包含网页测试、MCP服务器构建、前端设计、品牌指南应用等十多个示例技能-5。

example-skills：包含网页测试、MCP服务器构建、前端设计、品牌指南应用等十多个示例技能-5。

### 🔍 社区与开源资源

这是探索技能、获取灵感和直接使用现成方案的主要阵地。

- GitHub官方仓库：在GitHub上搜索 anthropics/skills 可以找到官方开源的技能库-5。

GitHub官方仓库：在GitHub上搜索 anthropics/skills 可以找到官方开源的技能库-5。

- 第三方社区：许多开发者和社区会分享自己编写的技能，通常以SKILL.md文件或项目的形式发布-1-5。你可以将其下载并放置到对应的Skills目录中即可使用-4。

第三方社区：许多开发者和社区会分享自己编写的技能，通常以SKILL.md文件或项目的形式发布-1-5。你可以将其下载并放置到对应的Skills目录中即可使用-4。

### 🛠️ 自行创建与使用技能

如果你有特定的需求，自己创建技能能获得最好的效果。

- 创建技能目录：根据你想要共享的范围，在对应位置创建目录-4。个人技能：~/.claude/skills/your-skill-name/ （仅自己可用）项目技能：.claude/skills/your-skill-name/ （项目成员共享）

创建技能目录：根据你想要共享的范围，在对应位置创建目录-4。

- 个人技能：~/.claude/skills/your-skill-name/ （仅自己可用）

个人技能：~/.claude/skills/your-skill-name/ （仅自己可用）

- 项目技能：.claude/skills/your-skill-name/ （项目成员共享）

项目技能：.claude/skills/your-skill-name/ （项目成员共享）

- 编写核心文件：在目录中创建 SKILL.md 文件。它包含顶部的YAML元数据（如name、description）和下方的具体指令-1-4。description的撰写非常关键，需要清晰描述功能和触发场景，Claude会根据它来自动匹配-4。

编写核心文件：在目录中创建 SKILL.md 文件。它包含顶部的YAML元数据（如name、description）和下方的具体指令-1-4。description的撰写非常关键，需要清晰描述功能和触发场景，Claude会根据它来自动匹配-4。

- 使用技能：创建并重启Claude Code后，直接描述你的任务（如“提取这份PDF中的付款条款”），Claude会自动识别并建议使用匹配的技能，无需手动指定技能名称-5-7。你还可以在一个任务中组合使用多个技能-5。

使用技能：创建并重启Claude Code后，直接描述你的任务（如“提取这份PDF中的付款条款”），Claude会自动识别并建议使用匹配的技能，无需手动指定技能名称-5-7。你还可以在一个任务中组合使用多个技能-5。

### 💡 实用技巧

- 查看已加载技能：在Claude Code中询问 What Skills are available? 可以查看当前所有可用技能列表-4-5。

查看已加载技能：在Claude Code中询问 What Skills are available? 可以查看当前所有可用技能列表-4-5。

- 调试技能：如果技能未按预期触发，可以用 claude --debug 命令启动调试模式，查看详细的加载和激活日志-4-5。

调试技能：如果技能未按预期触发，可以用 claude --debug 命令启动调试模式，查看详细的加载和激活日志-4-5。

总的来说，建议新手先从官方市场安装 document-skills 等核心包开始体验-5，然后在社区中寻找灵感，最终学会创建自己的专属技能来最大化提升效率。

如果你对创建特定用途（比如自动生成API文档或代码审查）的技能感兴趣，我可以为你提供更具体的创建思路和文件结构示例。