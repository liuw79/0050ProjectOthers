// server/src/routes/write.js
import express from 'express';
import { lark } from '../lib/lark.js';
import { ai } from '../lib/ai.js';

const router = express.Router();

// 延迟获取配置
const getTables = () => ({
  materials: {
    appToken: process.env.LARK_MATERIALS_APP_TOKEN,
    tableId: process.env.LARK_MATERIALS_TABLE_ID,
  },
  courses: {
    appToken: process.env.LARK_COURSES_APP_TOKEN,
    tableId: process.env.LARK_COURSES_TABLE_ID,
  },
});

// 获取选中的素材（同时处理课程和其他素材）
async function getSelectedMaterials(materialIds) {
  const TABLES = getTables();
  const result = {
    courses: [],
    profiles: [],
    brands: [],
    references: [],
  };

  // 区分课程 ID（以 rec 开头）和默认素材 ID（以 default- 开头）
  const courseIds = materialIds.filter(id => id.startsWith('rec') && id.length > 10);
  const defaultIds = materialIds.filter(id => id.startsWith('default-'));
  const otherIds = materialIds.filter(id => !id.startsWith('rec') && !id.startsWith('default-') && id.length > 5);

  // 1. 获取课程内容
  if (courseIds.length > 0) {
    const courseRecords = await lark.getRecords(TABLES.courses.appToken, TABLES.courses.tableId);
    result.courses = courseRecords
      .filter(r => courseIds.includes(r.record_id))
      .map(r => ({
        title: r.fields.course_name,
        content: r.fields.content?.slice(0, 10000),
        teacher: r.fields.teacher,
      }));
  }

  // 2. 获取其他素材（从素材表）
  if (otherIds.length > 0) {
    const materialRecords = await lark.getRecords(TABLES.materials.appToken, TABLES.materials.tableId);
    const materials = materialRecords
      .filter(r => otherIds.includes(r.record_id))
      .map(r => ({ category: r.fields.category, title: r.fields.title, content: r.fields.content }));

    result.profiles = materials.filter(m => m.category === '用户画像');
    result.brands = materials.filter(m => m.category === '高维品牌');
    result.references = materials.filter(m => m.category === '参考标题');
  }

  // 3. 处理默认素材
  const DEFAULT_MATERIALS = {
    'default-profile-1': {
      category: '用户画像',
      title: '目标读者画像',
      content: `【目标读者】
- 1-10 亿规模的创业公司创始人
- 正在经历增长瓶颈或战略迷茫期
- 关注组织效率、人才管理、战略落地
- 希望通过系统学习提升决策质量
- 习惯碎片化阅读，偏好实战性内容`,
    },
    'default-brand-1': {
      category: '高维品牌',
      title: '高维学堂品牌调性',
      content: `【品牌调性】
- 科学：基于方法论和框架，不是鸡汤
- 实战：案例来自真实企业，可落地
- 同行：站在创始人立场，用"我们"而非"你"
- 专业但不装：口语化表达，避免学术腔
- 正能量但有痛点：直面问题，给出解决方案`,
    },
    'default-ref-1': {
      category: '参考标题',
      title: '参考标题风格',
      content: `【标题风格】
- 数字化：《90%的创业公司都忽略了这个战略问题》
- 反常识：《为什么你的战略执行总是变形？》
- 痛点型：《老板的战术勤奋，正在杀死这家公司》
- 方法型：《3个步骤，帮你找到第二增长曲线》
- 案例型：《从9亿到120亿：这家公司做对了什么？》`,
    },
  };

  for (const id of defaultIds) {
    const material = DEFAULT_MATERIALS[id];
    if (material) {
      if (material.category === '用户画像') result.profiles.push(material);
      else if (material.category === '高维品牌') result.brands.push(material);
      else if (material.category === '参考标题') result.references.push(material);
    }
  }

  return result;
}

// 根据选题和素材生成文章
router.post('/generate', async (req, res) => {
  try {
    const { title, materialIds } = req.body;

    // 获取选中的素材
    const selected = await getSelectedMaterials(materialIds);

    const prompt = `【写作任务】
文章标题: ${title}

【目标读者】
${selected.profiles.map(p => p.content).join('\n')}

【品牌调性】
${selected.brands.map(b => b.content).join('\n')}

【参考标题风格】
${selected.references.map(r => r.title).join('\n')}

【课程素材】
${selected.courses.map(m => `【${m.title}】${m.teacher ? `（主讲：${m.teacher}）` : ''}\n${m.content}`).join('\n\n')}

【写作要求】
1. 基于课程素材写作，可以引用案例、数据、金句
2. 口语化表达，像和创始人朋友聊天
3. 站在创始人立场，用"我们"而不是"你"
4. 避免"综上所述"、"值得注意的是"等 AI 味
5. 句子 15-25 字为主，段落 3-5 行
6. 用 Markdown 格式
7. 字数控制在 3000 字左右

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

    // 获取选中的素材
    const selected = await getSelectedMaterials(materialIds);

    const prompt = `【写作任务】
文章标题: ${title}

【目标读者】
${selected.profiles.map(p => p.content).join('\n')}

【品牌调性】
${selected.brands.map(b => b.content).join('\n')}

【参考标题风格】
${selected.references.map(r => r.title).join('\n')}

【课程素材】
${selected.courses.map(m => `【${m.title}】${m.teacher ? `（主讲：${m.teacher}）` : ''}\n${m.content}`).join('\n\n')}

【写作要求】
1. 基于课程素材写作，可以引用案例、数据、金句
2. 口语化表达，像和创始人朋友聊天
3. 站在创始人立场，用"我们"而不是"你"
4. 避免"综上所述"、"值得注意的是"等 AI 味
5. 句子 15-25 字为主，段落 3-5 行
6. 用 Markdown 格式
7. 字数控制在 3000 字左右

直接输出文章内容。`;

    res.json({ success: true, prompt });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

export default router;
