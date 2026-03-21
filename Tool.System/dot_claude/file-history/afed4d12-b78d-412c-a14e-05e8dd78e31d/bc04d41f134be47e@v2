// server/src/routes/courses.js
import express from 'express';
import { lark } from '../lib/lark.js';

const router = express.Router();

// 延迟获取配置
const getTables = () => ({
  courses: {
    appToken: process.env.LARK_COURSES_APP_TOKEN,
    tableId: process.env.LARK_COURSES_TABLE_ID,
  },
  segments: {
    appToken: process.env.LARK_SEGMENTS_APP_TOKEN,
    tableId: process.env.LARK_SEGMENTS_TABLE_ID,
  },
});

// 获取课程列表（只返回名称，不返回内容）
router.get('/', async (req, res) => {
  try {
    const TABLES = getTables();
    const records = await lark.getRecords(TABLES.courses.appToken, TABLES.courses.tableId);
    const courses = records.map(r => ({
      id: r.record_id,
      name: r.fields.course_name,
      teacher: r.fields.teacher,
      processStatus: r.fields.process_status || '待处理',
    }));
    res.json({ success: true, courses });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

/**
 * 获取课程详情（包含概述和段落索引）
 * GET /api/courses/:id
 */
router.get('/:id', async (req, res) => {
  try {
    const TABLES = getTables();
    const records = await lark.getRecords(TABLES.courses.appToken, TABLES.courses.tableId);
    const course = records.find(r => r.record_id === req.params.id);

    if (!course) {
      return res.status(404).json({ success: false, error: '课程不存在' });
    }

    // 解析 segment_index JSON
    let segmentIndex = null;
    if (course.fields.segment_index) {
      try {
        segmentIndex = JSON.parse(course.fields.segment_index);
      } catch (e) {
        console.error('解析 segment_index 失败:', e.message);
      }
    }

    res.json({
      success: true,
      course: {
        id: course.record_id,
        name: course.fields.course_name,
        teacher: course.fields.teacher,
        overview: course.fields.overview || '',
        segmentIndex: segmentIndex,
        processStatus: course.fields.process_status || '待处理',
      },
    });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// 获取课程内容（用于 AI 分析）
router.get('/:id/content', async (req, res) => {
  try {
    const TABLES = getTables();
    const records = await lark.getRecords(TABLES.courses.appToken, TABLES.courses.tableId);
    const course = records.find(r => r.record_id === req.params.id);

    if (!course) {
      return res.status(404).json({ success: false, error: '课程不存在' });
    }

    res.json({
      success: true,
      course: {
        id: course.record_id,
        name: course.fields.course_name,
        teacher: course.fields.teacher,
        content: course.fields.content,
      },
    });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

export default router;
