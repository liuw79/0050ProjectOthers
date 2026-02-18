// server/src/routes/segments.js
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

/**
 * 获取段落列表
 * GET /api/segments
 * Query params:
 * - course_id: 课程ID（可选，筛选指定课程的段落）
 * - page: 页码（默认1）
 * - pageSize: 每页数量（默认20）
 */
router.get('/', async (req, res) => {
  try {
    const TABLES = getTables();
    const { course_id, page = 1, pageSize = 20 } = req.query;

    // 构建过滤条件
    let filter = null;
    if (course_id) {
      filter = {
        conjunction: 'and',
        conditions: [
          {
            field_name: 'course',
            operator: 'is',
            value: [course_id]
          }
        ]
      };
    }

    // 获取记录
    let records;
    if (filter) {
      records = await lark.searchRecords(
        TABLES.segments.appToken,
        TABLES.segments.tableId,
        filter
      );
    } else {
      records = await lark.getRecords(
        TABLES.segments.appToken,
        TABLES.segments.tableId
      );
    }

    // 转换并排序
    const allSegments = records
      .map(r => ({
        id: r.record_id,
        courseId: r.fields.course,
        index: r.fields.segment_index,
        title: r.fields.title,
        summary: r.fields.summary,
        charCount: r.fields.char_count,
        keywords: r.fields.keywords || [],
      }))
      .sort((a, b) => (a.index || 0) - (b.index || 0));

    // 分页
    const start = (page - 1) * pageSize;
    const segments = allSegments.slice(start, start + parseInt(pageSize));

    res.json({
      success: true,
      segments,
      total: allSegments.length,
      page: parseInt(page),
      pageSize: parseInt(pageSize),
    });
  } catch (err) {
    console.error('获取段落列表失败:', err);
    res.status(500).json({ success: false, error: err.message });
  }
});

/**
 * 获取段落详情（包含完整内容）
 * GET /api/segments/:id
 */
router.get('/:id', async (req, res) => {
  try {
    const TABLES = getTables();
    const records = await lark.getRecords(
      TABLES.segments.appToken,
      TABLES.segments.tableId
    );

    const segment = records.find(r => r.record_id === req.params.id);

    if (!segment) {
      return res.status(404).json({ success: false, error: '段落不存在' });
    }

    res.json({
      success: true,
      segment: {
        id: segment.record_id,
        courseId: segment.fields.course,
        index: segment.fields.segment_index,
        title: segment.fields.title,
        summary: segment.fields.summary,
        content: segment.fields.content,
        charCount: segment.fields.char_count,
        keywords: segment.fields.keywords || [],
      },
    });
  } catch (err) {
    console.error('获取段落详情失败:', err);
    res.status(500).json({ success: false, error: err.message });
  }
});

/**
 * 批量获取段落内容
 * POST /api/segments/batch
 * Body: { segmentIds: string[] }
 */
router.post('/batch', async (req, res) => {
  try {
    const TABLES = getTables();
    const { segmentIds } = req.body;

    if (!Array.isArray(segmentIds) || segmentIds.length === 0) {
      return res.status(400).json({ success: false, error: '请提供段落ID列表' });
    }

    const records = await lark.getRecords(
      TABLES.segments.appToken,
      TABLES.segments.tableId
    );

    const segments = segmentIds
      .map(id => records.find(r => r.record_id === id))
      .filter(Boolean)
      .map(r => ({
        id: r.record_id,
        courseId: r.fields.course,
        index: r.fields.segment_index,
        title: r.fields.title,
        summary: r.fields.summary,
        content: r.fields.content,
        charCount: r.fields.char_count,
        keywords: r.fields.keywords || [],
      }));

    res.json({
      success: true,
      segments,
      requested: segmentIds.length,
      found: segments.length,
    });
  } catch (err) {
    console.error('批量获取段落失败:', err);
    res.status(500).json({ success: false, error: err.message });
  }
});

/**
 * 根据课程ID获取段落索引（轻量版，不含内容）
 * GET /api/segments/index/:courseId
 */
router.get('/index/:courseId', async (req, res) => {
  try {
    const TABLES = getTables();
    const { courseId } = req.params;

    const filter = {
      conjunction: 'and',
      conditions: [
        {
          field_name: 'course',
          operator: 'is',
          value: [courseId]
        }
      ]
    };

    const records = await lark.searchRecords(
      TABLES.segments.appToken,
      TABLES.segments.tableId,
      filter
    );

    // 转换并排序（不包含content字段，减少数据量）
    const segments = records
      .map(r => ({
        id: r.record_id,
        index: r.fields.segment_index,
        title: r.fields.title,
        summary: r.fields.summary,
        charCount: r.fields.char_count,
        keywords: r.fields.keywords || [],
      }))
      .sort((a, b) => (a.index || 0) - (b.index || 0));

    res.json({
      success: true,
      courseId,
      segments,
      total: segments.length,
    });
  } catch (err) {
    console.error('获取段落索引失败:', err);
    res.status(500).json({ success: false, error: err.message });
  }
});

export default router;
