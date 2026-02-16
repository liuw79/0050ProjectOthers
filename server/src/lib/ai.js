// server/src/lib/ai.js
export class AIClient {
  constructor() {
    this.geminiKey = process.env.GEMINI_API_KEY;
    this.geminiUrl = 'https://generativelanguage.googleapis.com/v1beta/models';
  }

  async generate(prompt, options = {}) {
    const model = options.model || 'gemini-2.0-flash';
    const maxTokens = options.maxTokens || 8192;

    const res = await fetch(
      `${this.geminiUrl}/${model}:generateContent?key=${this.geminiKey}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: [{ parts: [{ text: prompt }] }],
          generationConfig: { maxOutputTokens: maxTokens },
        }),
      }
    );

    const data = await res.json();
    return data.candidates?.[0]?.content?.parts?.[0]?.text || '';
  }

  async generateJSON(prompt, options = {}) {
    const text = await this.generate(
      prompt + '\n\n只输出 JSON，不要其他内容。',
      options
    );
    const match = text.match(/\{[\s\S]*\}/);
    return match ? JSON.parse(match[0]) : null;
  }
}

export const ai = new AIClient();
