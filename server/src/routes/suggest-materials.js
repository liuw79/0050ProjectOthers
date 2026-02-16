// server/src/routes/suggest-materials.js
import express from 'express';
import { lark } from '../lib/lark.js';
import { ai } from '../lib/ai.js';

const router = express.Router();

const TABLES = {
  materials: {
    appToken: process.env.LARK_MATERIALS_APP_TOKEN,
    tableId: process.env.LARK_MATERIALS_TABLE_ID,
  },
  courses: {
    appToken: process.env.LARK_COURSES_APP_TOKEN,
    tableId: process.env.LARK_COURSES_TABLE_ID,
  },
};

// 根据选题推荐素材
router.post('/', async (req, res) => {
  try {
    const { title, courseIds } = req.body;

    // 获取所有素材
    const records = await lark.getRecords(TABLES.materials.appToken, TABLES.materials.tableId);
    const allMaterials = records.map(r => ({
      id: r.record_id,
      title: r.fields.title,
      content: r.fields.content,
      type: r.fields.type,
      course: r.fields.course,
    }));

    // 按类型分组
    const grouped = {
      course: allMaterials.filter(m => m.type === '课程素材' && (!courseIds || courseIds.includes(m.course))),
      profile: allMaterials.filter(m => m.type === '用户画像'),
      brand: allMaterials.filter(m => m.type === '高维品牌'),
      reference: allMaterials.filter(m => m.type === '参考标题'),
    };

    // 让 AI 选择相关素材
    const courseMaterialList = grouped.course.map(m => ({ id: m.id, title: m.title, preview: m.content?.slice(0, 200) }));

    const prompt = `用户要写的文章标题: ${title}

可选的课程素材:
${JSON.stringify(courseMaterialList, null, 2)}

【任务】选择与这个标题最相关的课程素材 ID。

【输出格式】JSON:
{
  "selectedIds": ["id1", "id2", ...]
}`;

    const result = await ai.generateJSON(prompt);
    const selectedIds = result?.selectedIds || [];

    // 组装返回数据
    const response = {
      course: grouped.course.filter(m => selectedIds.includes(m.id)),
      profile: grouped.profile,
      brand: grouped.brand,
      reference: grouped.reference,
    };

    res.json({ success: true, materials: response });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

export default router;
