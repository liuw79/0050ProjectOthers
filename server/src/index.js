require('dotenv').config();
const express = require('express');
const cors = require('cors');
const AIClient = require('./ai-client');
const LarkClient = require('./lark-client');

const app = express();
const PORT = process.env.PORT || 3000;
const aiClient = new AIClient();
const larkClient = new LarkClient();

// 多维表格配置（临时，实际需要从飞书获取）
const BITABLE_CONFIG = {
  users: {
    app_token: process.env.LARK_USERS_APP_TOKEN || 'placeholder_users_table_token',
    table_id: process.env.LARK_USERS_TABLE_ID || 'placeholder_users_table_id',
  },
  materials: {
    app_token: process.env.LARK_MATERIALS_APP_TOKEN || 'placeholder_materials_table_token',
    table_id: process.env.LARK_MATERIALS_TABLE_ID || 'placeholder_materials_table_id',
  }
};

app.use(cors());
app.use(express.json());

// 健康检查接口
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// ========== 用户数据API ==========

// 获取用户信息
app.get('/api/users/:userId', async (req, res) => {
  try {
    const { userId } = req.params;
    const records = await larkClient.queryBitableRecords(
      BITABLE_CONFIG.users.app_token,
      BITABLE_CONFIG.users.table_id,
      { filter: { conditions: [{ field_name: 'user_id', operator: 'is', value: [userId] }] } }
    );
    if (records.length === 0) {
      return res.status(404).json({ success: false, error: '用户不存在' });
    }
    res.json({ success: true, user: records[0].fields });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// 创建用户
app.post('/api/users', async (req, res) => {
  try {
    const { userId, name, role } = req.body;
    const result = await larkClient.addBitableRecord(
      BITABLE_CONFIG.users.app_token,
      BITABLE_CONFIG.users.table_id,
      {
        user_id: userId,
        name: name,
        role: role || 'user',
        created_at: new Date().toISOString(),
      }
    );
    res.json({ success: true, user: result.fields });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// ========== 素材库API ==========

// 添加素材
app.post('/api/materials', async (req, res) => {
  try {
    const { userId, title, content, tags, category } = req.body;
    if (!userId || !title || !content) {
      return res.status(400).json({ success: false, error: '缺少必填字段: userId, title, content' });
    }
    const result = await larkClient.addBitableRecord(
      BITABLE_CONFIG.materials.app_token,
      BITABLE_CONFIG.materials.table_id,
      {
        user_id: userId,
        title: title,
        content: content,
        tags: tags || [],
        category: category || 'default',
        created_at: new Date().toISOString(),
      }
    );
    res.json({ success: true, material: result.fields });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// 获取素材列表
app.get('/api/materials', async (req, res) => {
  try {
    const { userId, tag, category } = req.query;
    const filter = { conditions: [] };
    if (userId) {
      filter.conditions.push({
        field_name: 'user_id',
        operator: 'is',
        value: [userId]
      });
    }
    if (tag) {
      filter.conditions.push({
        field_name: 'tags',
        operator: 'contains',
        value: [tag]
      });
    }
    if (category) {
      filter.conditions.push({
        field_name: 'category',
        operator: 'is',
        value: [category]
      });
    }
    const records = await larkClient.queryBitableRecords(
      BITABLE_CONFIG.materials.app_token,
      BITABLE_CONFIG.materials.table_id,
      filter.conditions.length > 0 ? filter : undefined
    );
    res.json({ success: true, materials: records.map(r => r.fields) });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// ========== AI API ==========

// 调用Claude API
app.post('/api/ai/claude', async (req, res) => {
  try {
    const { prompt, model, maxTokens } = req.body;
    const result = await aiClient.callClaude(prompt, { model, maxTokens });
    res.json({ success: true, result, model: model || 'claude-sonnet-4-5' });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// 调用Gemini API
app.post('/api/ai/gemini', async (req, res) => {
  try {
    const { prompt, model, maxTokens } = req.body;
    const result = await aiClient.callGemini(prompt, { model, maxTokens });
    res.json({ success: true, result, model: model || 'gemini-2.0-flash' });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// 调用GLM API
app.post('/api/ai/glm', async (req, res) => {
  try {
    const { prompt, model, maxTokens } = req.body;
    const result = await aiClient.callGLM(prompt, { model, maxTokens });
    res.json({ success: true, result, model: model || 'glm-5' });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// 统一AI调用接口 - 根据任务类型自动选择模型
app.post('/api/ai/generate', async (req, res) => {
  try {
    const { taskType, prompt, model, maxTokens } = req.body;
    const result = await aiClient.callModel(taskType, prompt, { model, maxTokens });
    const usedModel = model || aiClient.selectModelByTask(taskType);
    res.json({ success: true, result, model: usedModel, taskType });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  console.log(`Available endpoints:`);
  console.log(`  GET  /health`);
  console.log(`  GET  /api/users/:userId`);
  console.log(`  POST /api/users`);
  console.log(`  GET  /api/materials`);
  console.log(`  POST /api/materials`);
  console.log(`  POST /api/ai/claude`);
  console.log(`  POST /api/ai/gemini`);
  console.log(`  POST /api/ai/glm`);
  console.log(`  POST /api/ai/generate`);
});
