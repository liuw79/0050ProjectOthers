// server/src/routes/suggest-materials.js
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

// 默认素材（当飞书表中没有数据时使用）
const DEFAULT_MATERIALS = {
  profile: [
    {
      id: 'default-profile-1',
      title: '目标读者画像',
      content: `【目标读者】
- 1-10 亿规模的创业公司创始人
- 正在经历增长瓶颈或战略迷茫期
- 关注组织效率、人才管理、战略落地
- 希望通过系统学习提升决策质量
- 习惯碎片化阅读，偏好实战性内容`,
    },
  ],
  brand: [
    {
      id: 'default-brand-1',
      title: '高维学堂品牌调性',
      content: `【品牌调性】
- 科学：基于方法论和框架，不是鸡汤
- 实战：案例来自真实企业，可落地
- 同行：站在创始人立场，用"我们"而非"你"
- 专业但不装：口语化表达，避免学术腔
- 正能量但有痛点：直面问题，给出解决方案`,
    },
  ],
  reference: [
    {
      id: 'default-ref-1',
      title: '参考标题风格',
      content: `【标题风格】
- 数字化：《90%的创业公司都忽略了这个战略问题》
- 反常识：《为什么你的战略执行总是变形？》
- 痛点型：《老板的战术勤奋，正在杀死这家公司》
- 方法型：《3个步骤，帮你找到第二增长曲线》
- 案例型：《从9亿到120亿：这家公司做对了什么？》`,
    },
  ],
};

// 根据选题推荐素材
router.post('/', async (req, res) => {
  try {
    const { title, courseIds } = req.body;
    const TABLES = getTables();

    // 1. 获取用户选择的课程内容作为课程素材
    let courseMaterials = [];
    if (courseIds?.length > 0) {
      const courseRecords = await lark.getRecords(TABLES.courses.appToken, TABLES.courses.tableId);
      const selectedCourses = courseRecords.filter(r => courseIds.includes(r.record_id));
      courseMaterials = selectedCourses.map(c => ({
        id: c.record_id,
        title: c.fields.course_name,
        content: c.fields.content?.slice(0, 10000), // 限制每个课程 10000 字
        teacher: c.fields.teacher,
      }));
    }

    // 2. 获取其他素材（用户画像、品牌、参考标题）
    const materialRecords = await lark.getRecords(TABLES.materials.appToken, TABLES.materials.tableId);
    const allMaterials = materialRecords.map(r => ({
      id: r.record_id,
      title: r.fields.title,
      content: r.fields.content,
      category: r.fields.category,
    }));

    const grouped = {
      profile: allMaterials.filter(m => m.category === '用户画像'),
      brand: allMaterials.filter(m => m.category === '高维品牌'),
      reference: allMaterials.filter(m => m.category === '参考标题'),
    };

    // 3. 组装返回数据
    const response = {
      course: courseMaterials,
      profile: grouped.profile.length > 0 ? grouped.profile : DEFAULT_MATERIALS.profile,
      brand: grouped.brand.length > 0 ? grouped.brand : DEFAULT_MATERIALS.brand,
      reference: grouped.reference.length > 0 ? grouped.reference : DEFAULT_MATERIALS.reference,
    };

    res.json({ success: true, materials: response });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

export default router;
