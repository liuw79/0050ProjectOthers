# DeepSeek 对话导出工具设计文档

## 概述

批量导出 Deepseek 所有历史对话记录为 Markdown 文件的命令行工具。

## 需求

- 用户有几百条对话需要导出
- Deepseek API 无状态，不提供历史对话接口
- 网页版有手动导出功能，但需要逐个点击
- 需要自动化解决方案

## 设计决策

| 项目 | 决定 |
|------|------|
| 数据获取 | Playwright 浏览器自动化（登录用户配合） |
| 输出结构 | 扁平目录，所有 MD 放一起 |
| 文件命名 | 对话标题（处理非法字符） |
| 分类/标签 | 暂不实现，后续可扩展 |

## 技术栈

- Python 3.10+
- Playwright（浏览器自动化）
- asyncio（异步处理）
- rich（进度显示，可选）

## 核心流程

```
1. Playwright 打开 Deepseek 网页
2. 等待用户手动登录（检测登录成功状态）
3. 获取对话列表
4. 遍历每个对话：
   - 点击进入对话
   - 抓取对话内容
   - 保存为 MD 文件
5. 完成后提示统计信息
```

## 输出格式

**目录结构：**
```
exports/
├── 对话标题1.md
├── 对话标题2.md
└── ...
```

**MD 文件格式（待运行时确认）：**
```markdown
# 对话标题

> 创建时间: YYYY-MM-DD HH:MM
> 消息数: N

## User
对话内容...

## Assistant
回复内容...

## User
...
```

## 项目结构

```
Tool.DeepSeek/
├── src/
│   └── deepseek_export/
│       ├── __init__.py
│       ├── main.py          # 入口
│       ├── browser.py       # Playwright 操作
│       ├── parser.py        # 内容解析
│       └── exporter.py      # MD 导出
├── exports/                  # 导出输出目录
├── docs/
│   └── plans/
├── pyproject.toml
├── requirements.txt
└── README.md
```

## 待确认事项

- [ ] Deepseek 网页版对话列表的 DOM 结构
- [ ] 对话内容的 HTML 结构
- [ ] 是否有分页/懒加载
- [ ] 登录状态检测方式

## 后续扩展

- 按日期/标签分类
- 并行导出加速
- 增量导出（只导出新对话）
- 导出为其他格式（PDF、HTML）
