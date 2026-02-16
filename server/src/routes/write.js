// server/src/routes/write.js
import express from 'express';
import { lark } from '../lib/lark.js';
import { ai } from '../lib/ai.js';

const router = express.Router();

const TABLES = {
  materials: {
    appToken: process.env.LARK_MATERIALS_APP_TOKEN,
    tableId: process.env.LARK_MATERIALS_TABLE_ID,
  },
};

// 根据选题和素材生成文章
router.post('/generate', async (req, res) => {
  try {
    const { title, materialIds } = req.body;

    // 获取选中的素材
    const records = await lark.getRecords(TABLES.materials.appToken, TABLES.materials.tableId);
    const materials = records
      .filter(r => materialIds.includes(r.record_id))
      .map(r => ({ type: r.fields.type, title: r.fields.title, content: r.fields.content }));

    // 分类素材
    const courseMaterials = materials.filter(m => m.type === '课程素材');
    const profiles = materials.filter(m => m.type === '用户画像');
    const brands = materials.filter(m => m.type === '高维品牌');
    const references = materials.filter(m => m.type === '参考标题');

    const prompt = `【写作任务】
文章标题: ${title}

【目标读者】
${profiles.map(p => p.content).join('\n')}

【品牌调性】
${brands.map(b => b.content).join('\n')}

【参考标题风格】
${references.map(r => r.title).join('\n')}

【课程素材】
${courseMaterials.map(m => `【${m.title}】\n${m.content}`).join('\n\n')}

【写作要求】
1. 基于课程素材写作，可以引用案例、数据、金句
2. 口语化表达，像和创始人朋友聊天
3. 站在创始人立场，用"我们"而不是"你"
4. 避免"综上所述"、"值得注意的是"等 AI 味
5. 句子 15-25 字为主，段落 3-5 行
6. 用 Markdown 格式

直接输出文章内容。`;

    const content = await ai.generate(prompt, { maxTokens: 8192 });
    res.json({ success: true, content, prompt });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// 预览 Prompt（不生成内容）
router.post('/preview', async (req, res) => {
  try {
    const { title, materialIds } = req.body;

    const records = await lark.getRecords(TABLES.materials.appToken, TABLES.materials.tableId);
    const materials = records
      .filter(r => materialIds.includes(r.record_id))
      .map(r => ({ type: r.fields.type, title: r.fields.title, content: r.fields.content }));

    const courseMaterials = materials.filter(m => m.type === '课程素材');
    const profiles = materials.filter(m => m.type === '用户画像');
    const brands = materials.filter(m => m.type === '高维品牌');
    const references = materials.filter(m => m.type === '参考标题');

    const prompt = `【写作任务】
文章标题: ${title}

【目标读者】
${profiles.map(p => p.content).join('\n')}

【品牌调性】
${brands.map(b => b.content).join('\n')}

【参考标题风格】
${references.map(r => r.title).join('\n')}

【课程素材】
${courseMaterials.map(m => `【${m.title}】\n${m.content}`).join('\n\n')}

【写作要求】
1. 基于课程素材写作，可以引用案例、数据、金句
2. 口语化表达，像和创始人朋友聊天
3. 站在创始人立场，用"我们"而不是"你"
4. 避免"综上所述"、"值得注意的是"等 AI 味
5. 句子 15-25 字为主，段落 3-5 行
6. 用 Markdown 格式

直接输出文章内容。`;

    res.json({ success: true, prompt });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

export default router;
