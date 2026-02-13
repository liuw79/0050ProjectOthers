require('dotenv').config();
const express = require('express');
const cors = require('cors');
const AIClient = require('./ai-client');

const app = express();
const PORT = process.env.PORT || 3000;
const aiClient = new AIClient();

app.use(cors());
app.use(express.json());

// 健康检查接口
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

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
  console.log(`  POST /api/ai/claude`);
  console.log(`  POST /api/ai/gemini`);
  console.log(`  POST /api/ai/glm`);
  console.log(`  POST /api/ai/generate`);
});
