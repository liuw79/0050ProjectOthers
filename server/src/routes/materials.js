// server/src/routes/materials.js
import express from 'express';
import { lark } from '../lib/lark.js';

const router = express.Router();

const TABLES = {
  materials: {
    appToken: process.env.LARK_MATERIALS_APP_TOKEN,
    tableId: process.env.LARK_MATERIALS_TABLE_ID,
  },
};

// 获取素材列表
router.get('/', async (req, res) => {
  try {
    const { type, course, tags } = req.query;
    const conditions = [];

    if (type) {
      conditions.push({ field_name: 'type', operator: 'is', value: [type] });
    }
    if (course) {
      conditions.push({ field_name: 'course', operator: 'is', value: [course] });
    }

    const records = conditions.length > 0
      ? await lark.searchRecords(TABLES.materials.appToken, TABLES.materials.tableId, {
          conjunction: 'and',
          conditions,
        })
      : await lark.getRecords(TABLES.materials.appToken, TABLES.materials.tableId);

    const materials = records.map(r => ({
      id: r.record_id,
      ...r.fields,
    }));

    res.json({ success: true, materials });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// 获取单个素材
router.get('/:id', async (req, res) => {
  try {
    const records = await lark.getRecords(TABLES.materials.appToken, TABLES.materials.tableId);
    const material = records.find(r => r.record_id === req.params.id);

    if (!material) {
      return res.status(404).json({ success: false, error: '素材不存在' });
    }

    res.json({ success: true, material: { id: material.record_id, ...material.fields } });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

export default router;
