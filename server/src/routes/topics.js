// server/src/routes/topics.js
import express from 'express';
import { lark } from '../lib/lark.js';
import { ai } from '../lib/ai.js';

const router = express.Router();

const TABLES = {
  courses: {
    appToken: process.env.LARK_COURSES_APP_TOKEN,
    tableId: process.env.LARK_COURSES_TABLE_ID,
  },
  materials: {
    appToken: process.env.LARK_MATERIALS_APP_TOKEN,
    tableId: process.env.LARK_MATERIALS_TABLE_ID,
  },
};

// 根据课程或关键词推荐选题
router.post('/suggest', async (req, res) => {
  try {
    const { courseIds, keywords } = req.body;

    // 获取课程内容
    let courseContent = '';
    if (courseIds?.length > 0) {
      const records = await lark.getRecords(TABLES.courses.appToken, TABLES.courses.tableId);
      const courses = records.filter(r => courseIds.includes(r.record_id));
      courseContent = courses.map(c => `【${c.fields.course_name}】\n${c.fields.content?.slice(0, 10000)}`).join('\n\n');
    }

    const prompt = `你是一位资深商业媒体编辑。基于以下内容推荐公众号文章选题。

${courseContent ? `【课程内容】\n${courseContent}` : ''}
${keywords ? `【用户关注的关键词】${keywords}` : ''}

【任务】推荐 3-5 个选题。

【输出格式】JSON:
{
  "topics": [
    {
      "title": "文章标题（要有吸引力）",
      "angle": "核心角度（一句话）",
      "reason": "推荐理由"
    }
  ]
}

【要求】
1. 标题要能吸引创始人点击
2. 角度要具体可落地
3. 站在创始人立场`;

    const result = await ai.generateJSON(prompt);
    res.json({ success: true, ...result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

export default router;
