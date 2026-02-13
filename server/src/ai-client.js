// AI调用层 - 支持多模型

class AIClient {
  constructor() {
    this.models = {
      claude: {
        apiKey: process.env.ANTHROPIC_API_KEY,
        baseUrl: 'https://api.anthropic.com/v1/messages',
      },
      gemini: {
        apiKey: process.env.GOOGLE_AI_API_KEY,
        baseUrl: 'https://generativelanguage.googleapis.com/v1beta/models/',
      },
      glm: {
        apiKey: process.env.ZHIPUAI_API_KEY,
        baseUrl: 'https://open.bigmodel.cn/api/paas/v4/chat/completions',
      }
    };
  }

  // 调用Claude API
  async callClaude(prompt, options = {}) {
    const { model = 'claude-sonnet-4-5', maxTokens = 4096 } = options;
    const modelMapping = {
      'claude-sonnet-4-5': 'claude-sonnet-4-5-20250929',
      'claude-opus-4-5': 'claude-opus-4-5-20250929',
      'haiku-4': 'claude-haiku-4-20250514',
    };
    const modelName = modelMapping[model] || model;

    try {
      const response = await fetch(this.models.claude.baseUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': this.models.claude.apiKey,
          'anthropic-version': '2023-06-01',
          'anthropic-dangerous-direct-browser-access': 'true',
        },
        body: JSON.stringify({
          model: modelName,
          max_tokens: maxTokens,
          messages: [
            {
              role: 'user',
              content: prompt,
            }
          ],
        }),
      });

      const data = await response.json();
      return data.content[0].text;
    } catch (error) {
      console.error('Claude API error:', error.message);
      throw new Error(`Claude API调用失败: ${error.message}`);
    }
  }

  // 调用Gemini API
  async callGemini(prompt, options = {}) {
    const { model = 'gemini-2.0-flash', maxTokens = 4096 } = options;
    const modelName = model.startsWith('gemini') ? model : 'gemini-2.0-flash';

    try {
      const response = await fetch(`${this.models.gemini.baseUrl}${modelName}:generateContent`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          contents: [
            {
              parts: [
                {
                  text: prompt,
                },
              ],
            },
          ],
          generationConfig: {
            maxOutputTokens: maxTokens,
          },
        }),
      });

      const data = await response.json();
      return data.candidates[0].content.parts[0].text;
    } catch (error) {
      console.error('Gemini API error:', error.message);
      throw new Error(`Gemini API调用失败: ${error.message}`);
    }
  }

  // 调用GLM-5 API
  async callGLM(prompt, options = {}) {
    const { model = 'glm-5', maxTokens = 4096 } = options;

    try {
      const response = await fetch(this.models.glm.baseUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.models.glm.apiKey}`,
        },
        body: JSON.stringify({
          model: model,
          messages: [
            {
              role: 'user',
              content: prompt,
            },
          ],
          max_tokens: maxTokens,
        }),
      });

      const data = await response.json();
      return data.choices[0].message.content;
    } catch (error) {
      console.error('GLM API error:', error.message);
      throw new Error(`GLM API调用失败: ${error.message}`);
    }
  }

  // 统一调用接口 - 根据任务类型自动选择模型
  async callModel(taskType, prompt, options = {}) {
    const model = options.model || this.selectModelByTask(taskType);
    console.log(`调用模型: ${model}, 任务类型: ${taskType}`);

    switch (true) {
      case model.startsWith('claude'):
        return this.callClaude(prompt, options);
      case model.startsWith('gemini'):
        return this.callGemini(prompt, options);
      case model.startsWith('glm'):
        return this.callGLM(prompt, options);
      default:
        return this.callModel(taskType, prompt, { ...options, model: this.selectModelByTask(taskType) });
    }
  }

  // 根据任务类型选择默认模型
  selectModelByTask(taskType) {
    const modelMap = {
      'knowledge_extraction': 'gemini-2.0-flash',
      'content_generation': 'glm-5',
      'content_evaluation': 'claude-sonnet-4-5',
      'skill_iteration': 'claude-opus-4-5',
      'default': 'claude-sonnet-4-5',
    };
    return modelMap[taskType] || modelMap['default'];
  }
}

module.exports = AIClient;
