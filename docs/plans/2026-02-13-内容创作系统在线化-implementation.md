# 内容创作系统在线化 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 将现有的本地文件系统内容创作系统改造为在线系统，支持4-10人团队独立使用，统一管理内容和素材

**Architecture:** 采用飞书应用方案，使用飞书多维表格和飞书文档作为数据存储，Node.js作为后端服务，调用多AI模型（Claude、Gemini、GLM-5）

**Tech Stack:** Vue3、Node.js/Express、飞书开放平台API、飞书多维表格、飞书文档、Anthropic API、Google AI API、智谱AI API

---

## Initializer Agent - 首次环境设置

### Task 1: 创建项目基础结构

**Files:**
- Create: `server/package.json`
- Create: `server/.env.example`
- Create: `server/src/index.js`

**Step 1: Write the failing test**

```bash
# Test: 检查server目录是否存在
if [ ! -d "server" ]; then
  echo "FAIL: server目录不存在"
  exit 1
fi
echo "PASS: server目录存在"
```

**Step 2: Run test to verify it fails**

Run: `bash -c 'if [ ! -d "server" ]; then echo "FAIL"; else echo "UNEXPECTED PASS"; fi'`
Expected: FAIL

**Step 3: Create server directory and package.json**

```bash
mkdir -p server/src
cat > server/package.json << 'EOF'
{
  "name": "lark-content-system",
  "version": "1.0.0",
  "description": "内容创作系统后端服务",
  "main": "src/index.js",
  "scripts": {
    "start": "node src/index.js",
    "dev": "nodemon src/index.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "cors": "^2.8.5",
    "dotenv": "^16.3.1",
    "axios": "^1.6.7"
  },
  "devDependencies": {
    "nodemon": "^3.0.2"
  }
}
EOF
```

**Step 4: Run test to verify it passes**

Run: `bash -c 'if [ -d "server" ]; then echo "PASS"; else echo "FAIL"; fi'`
Expected: PASS

**Step 5: Create .env.example**

```bash
cat > server/.env.example << 'EOF'
# 飞书应用配置
LARK_APP_ID=
LARK_APP_SECRET=
LARK_VERIFICATION_TOKEN=
LARK_ENCRYPT_KEY=

# AI API配置
ANTHROPIC_API_KEY=
GOOGLE_AI_API_KEY=
ZHIPUAI_API_KEY=

# 服务器配置
PORT=3000
EOF
```

**Step 6: Create basic server file**

```javascript
cat > server/src/index.js << 'EOF'
require('dotenv').config();
const express = require('express');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
EOF
```

**Step 7: Commit**

```bash
git add server/ && git commit -m "feat: create server project structure"
```

---

### Task 2: 创建feature_list.json

**Files:**
- Create: `feature_list.json`

**Step 1: Write feature_list.json**

```json
cat > feature_list.json << 'EOF'
[
  {
    "id": "1",
    "category": "auth",
    "description": "用户可以通过飞书认证登录系统",
    "steps": [
      "点击飞书登录按钮",
      "用户被重定向到飞书授权页面",
      "用户同意授权",
      "系统获取用户信息",
      "验证用户可以访问主页"
    ],
    "passes": false
  },
  {
    "id": "2",
    "category": "data",
    "description": "飞书多维表格存储用户数据",
    "steps": [
      "用户登录后，多维表格新增用户记录",
      "用户信息包括user_id、name、role",
      "验证用户数据正确写入多维表格"
    ],
    "passes": false
  },
  {
    "id": "3",
    "category": "content",
    "description": "用户可以查看个人素材库",
    "steps": [
      "用户登录后进入系统",
      "点击'我的素材'菜单",
      "查看素材列表",
      "验证只显示当前用户的素材"
    ],
    "passes": false
  },
  {
    "id": "4",
    "category": "content",
    "description": "用户可以添加个人素材",
    "steps": [
      "点击'添加素材'按钮",
      "填写标题、内容、标签、分类",
      "提交保存",
      "验证素材出现在列表中"
    ],
    "passes": false
  },
  {
    "id": "5",
    "category": "content",
    "description": "用户可以选择内容类型开始创作",
    "steps": [
      "用户登录后进入主页",
      "查看内容类型选项（公众号、主持词、朋友圈等）",
      "选择'公众号'",
      "进入公众号创作流程"
    ],
    "passes": false
  },
  {
    "id": "6",
    "category": "workflow",
    "description": "系统展示创作流程进度条",
    "steps": [
      "用户选择内容类型",
      "显示进度条：步骤1/9→步骤2/9...",
      "当前步骤高亮显示",
      "验证进度正确展示"
    ],
    "passes": false
  },
  {
    "id": "7",
    "category": "ai",
    "description": "AI调用层支持多模型",
    "steps": [
      "调用Claude API",
      "调用Gemini API",
      "调用GLM-5 API",
      "验证各模型接口正常"
    ],
    "passes": false
  },
  {
    "id": "8",
    "category": "knowledge",
    "description": "飞书文档存储课程全文（仅管理员可见）",
    "steps": [
      "管理员上传课程文档",
      "文档存储在飞书文档",
      "设置权限为仅管理员可见",
      "验证普通用户无法访问"
    ],
    "passes": false
  },
  {
    "id": "9",
    "category": "knowledge",
    "description": "飞书多维表格存储知识点",
    "steps": [
      "在多维表格创建knowledge_points表",
      "包含标题、内容、标签、关联字段",
      "API可以读取和写入知识点"
    ],
    "passes": false
  },
  {
    "id": "10",
    "category": "skill",
    "description": "Skills数据存储和版本管理",
    "steps": [
      "多维表格创建skills表",
      "包含版本号、父版本、状态字段",
      "支持版本历史查询"
    ],
    "passes": false
  }
]
EOF
```

**Step 2: Commit**

```bash
git add feature_list.json && git commit -m "feat: add feature_list.json for tracking progress"
```

---

### Task 3: 创建claude-progress.txt

**Files:**
- Create: `claude-progress.txt`

**Step 1: Create progress tracking file**

```bash
cat > claude-progress.txt << 'EOF'
# 内容创作系统在线化 - 开发进度追踪

## 已完成任务

### 2026-02-13
- ✅ 创建项目基础结构
- ✅ 创建feature_list.json

## 当前任务

待选择下一个功能开始实现...

## 已知问题

暂无

## 待确认事项

1. 飞书应用的具体类型（小程序/网页应用/移动应用）
2. AI调用预算和限额设置
3. 飞书应用服务器部署的具体云服务商
4. 内容备份和灾备方案
EOF
```

**Step 2: Commit**

```bash
git add claude-progress.txt && git commit -m "feat: add progress tracking file"
```

---

### Task 4: 创建init.sh脚本

**Files:**
- Create: `init.sh`

**Step 1: Create init.sh**

```bash
cat > init.sh << 'EOF'
#!/bin/bash

# 内容创作系统 - 开发环境初始化脚本

echo "🚀 初始化开发环境..."

# 1. 检查环境
if [ ! -f "server/.env" ]; then
  echo "⚠️  警告: .env文件不存在，请复制.env.example并配置"
  if [ -f "server/.env.example" ]; then
    echo "运行: cp server/.env.example server/.env"
  fi
  exit 1
fi

# 2. 安装依赖
echo "📦 安装依赖..."
cd server
npm install
cd ..

# 3. 启动开发服务器
echo "🔧 启动开发服务器..."
cd server
npm run dev &
cd ..

echo "✅ 开发环境初始化完成！"
echo ""
echo "📝 开发服务器运行在: http://localhost:3000"
echo "📊 进度追踪文件: claude-progress.txt"
echo "📋 功能列表: feature_list.json"
echo ""
echo "💡 提示: Ctrl+C 停止服务器"
EOF

chmod +x init.sh
```

**Step 2: Commit**

```bash
git add init.sh && git commit -m "feat: add init.sh for development environment"
```

---

### Task 5: 创建前端项目结构

**Files:**
- Create: `frontend/package.json`
- Create: `frontend/vite.config.js`
- Create: `frontend/index.html`
- Create: `frontend/src/main.js`

**Step 1: Create frontend package.json**

```json
cat > frontend/package.json << 'EOF'
{
  "name": "lark-content-system-frontend",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "vue": "^3.4.0",
    "@larksuiteoapi/sdk": "^1.0.0",
    "axios": "^1.6.7"
  },
  "devDependencies": {
    "vite": "^5.0.0"
  }
}
EOF
```

**Step 2: Create vite.config.js**

```javascript
cat > frontend/vite.config.js << 'EOF'
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:3000',
        changeOrigin: true
      }
    }
  }
});
EOF
```

**Step 3: Create basic frontend files**

```html
cat > frontend/index.html << 'EOF'
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>内容创作系统</title>
</head>
<body>
  <div id="app"></div>
  <script type="module" src="/src/main.js"></script>
</body>
</html>
EOF
```

```javascript
cat > frontend/src/main.js << 'EOF'
import { createApp } from 'vue';

createApp({
  data() {
    return {
      message: '内容创作系统'
    };
  },
  template: `
    <div class="app">
      <h1>{{ message }}</h1>
      <p>开发中...</p>
    </div>
  `
}).mount('#app');
EOF
```

**Step 4: Commit**

```bash
git add frontend/ && git commit -m "feat: create frontend project structure"
```

---

## Coding Agent - 每次Session实现一个Feature

### Session启动流程

每次Coding Agent session开始时，执行以下步骤：

1. **运行pwd确认工作目录**
   ```bash
   pwd
   ```

2. **读取git logs和progress文件了解进展**
   ```bash
   git log --oneline -10
   cat claude-progress.txt
   ```

3. **读取feature_list.json选择一个未完成的feature**
   - 选择最高优先级的passes=false的feature
   - 确认理解该feature的需求

4. **运行init.sh启动开发服务器**
   ```bash
   ./init.sh
   ```

5. **测试基本功能**
   - 访问http://localhost:3000/health
   - 验证服务器正常运行

6. **实现选定的feature**

7. **测试feature端到端**
   - 按照feature_list.json中的steps测试
   - 只有通过所有步骤才标记为完成

8. **提交代码并更新进度**
   ```bash
   git add .
   git commit -m "feat: [feature description]"
   # 更新feature_list.json中对应feature的passes为true
   # 更新claude-progress.txt添加完成记录
   git add feature_list.json claude-progress.txt
   git commit -m "chore: update progress and feature status"
   ```

---

## 待实施的Features

以下features按照优先级排序，Coding Agent每次选择一个实现：

### 优先级1: 基础设施

| ID | Feature | 状态 |
|-----|----------|--------|
| 7 | AI调用层支持多模型 | ❌ |
| 2 | 飞书多维表格存储用户数据 | ❌ |

### 优先级2: 认证

| ID | Feature | 状态 |
|-----|----------|--------|
| 1 | 用户可以通过飞书认证登录系统 | ❌ |

### 优先级3: 内容管理

| ID | Feature | 状态 |
|-----|----------|--------|
| 3 | 用户可以查看个人素材库 | ❌ |
| 4 | 用户可以添加个人素材 | ❌ |
| 5 | 用户可以选择内容类型开始创作 | ❌ |

### 优先级4: 工作流

| ID | Feature | 状态 |
|-----|----------|--------|
| 6 | 系统展示创作流程进度条 | ❌ |

### 优先级5: 知识管理

| ID | Feature | 状态 |
|-----|----------|--------|
| 8 | 飞书文档存储课程全文 | ❌ |
| 9 | 飞书多维表格存储知识点 | ❌ |

### 优先级6: Skill管理

| ID | Feature | 状态 |
|-----|----------|--------|
| 10 | Skills数据存储和版本管理 | ❌ |

---

## Coding Session 示例

当Coding Agent开始一个session时，应该遵循以下模式：

```bash
# Session开始

[Assistant] 我开始了解当前项目状态。

[Tool Use] pwd
[Tool Use] cat claude-progress.txt
[Tool Use] git log --oneline -10

[Assistant] 好的，现在让我查看feature_list.json选择下一个要实现的feature。

[Tool Use] cat feature_list.json

[Assistant] 根据优先级，我选择实现 Feature #7: AI调用层支持多模型。

让我运行init.sh启动开发服务器。

[Tool Use] ./init.sh

[Assistant] 开发服务器已启动。让我测试健康检查接口。

[Tool Use] curl http://localhost:3000/health

[Assistant] 服务器运行正常。现在开始实现Feature #7...

[实现代码...]

[Assistant] 代码实现完成。现在进行端到端测试。

[测试按照steps...]

[Assistant] 所有测试通过。现在提交代码并更新进度。

[Tool Use] git add .
[Tool Use] git commit -m "feat: implement AI client with multi-model support (Claude, Gemini, GLM-5)"
[Tool Use] 更新feature_list.json中feature #7的passes为true
[Tool Use] 更新claude-progress.txt添加完成记录
[Tool Use] git add feature_list.json claude-progress.txt
[Tool Use] git commit -m "chore: update progress - feature #7 completed"

[Assistant] Feature #7 已完成！进度已更新。
```

---

## 关键原则

1. **一次一个Feature** - 每次session只实现一个feature
2. **完整测试** - 按照feature_list.json的steps进行端到端测试
3. **干净状态** - session结束时确保代码可以合并到main分支
4. **Git Commit** - 每个feature完成后必须提交
5. **进度更新** - 更新feature_list.json和claude-progress.txt
6. **只编辑passes字段** - 不允许删除或修改feature_list.json的其他字段

---

## 下一步

选择执行方式：

**1. Subagent-Driven（当前session）** - 我在这个session中逐个执行任务，每个任务后进行代码审查，快速迭代

**2. Parallel Session（独立session）** - 打开新session使用executing-plans技能，批量执行并设置检查点

**选择哪种方式？**
