# GW.Content 2.0

AI 写作工作台 - 素材透明，流程可控

## 功能特点

- **三步写作流程**：确定选题 → 素材准备 → 生成内容
- **素材透明**：预览 AI 将收到的完整 Prompt
- **AI 推荐**：根据课程或关键词自动推荐选题和素材

## 快速开始

### 后端

```bash
cd server
cp .env.example .env
# 编辑 .env 填写配置
npm install
npm run dev
```

### 前端

```bash
cd web
npm install
npm run dev
```

## 环境变量

在 `server/.env` 中配置：

| 变量名 | 说明 |
|--------|------|
| LARK_APP_ID | 飞书应用 ID |
| LARK_APP_SECRET | 飞书应用密钥 |
| LARK_MATERIALS_APP_TOKEN | 素材库多维表格 App Token |
| LARK_MATERIALS_TABLE_ID | 素材库多维表格 Table ID |
| LARK_COURSES_APP_TOKEN | 课程原文多维表格 App Token |
| LARK_COURSES_TABLE_ID | 课程原文多维表格 Table ID |
| GEMINI_API_KEY | Gemini API Key |

## 技术栈

- **前端**：Vue 3 + Vite + Pinia + Tailwind CSS
- **后端**：Node.js + Express
- **数据存储**：飞书多维表格
- **AI**：Google Gemini
