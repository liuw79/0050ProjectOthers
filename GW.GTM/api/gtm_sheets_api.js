// GTM通用表格系统 API接口
// 支持所有类型的表格的统一API
const express = require('express');
const { Pool } = require('pg');
const cors = require('cors');

const app = express();
const port = 3002; // 使用新端口，避免冲突

// 中间件
app.use(cors());
app.use(express.json());
app.use(express.static('.')); // 服务静态文件

// PostgreSQL连接配置
const pool = new Pool({
    user: 'comdir',
    host: 'localhost',
    database: 'gtm_assistant',
    port: 5432,
});

// 测试数据库连接
pool.query('SELECT NOW()', (err, res) => {
    if (err) {
        console.error('❌ 数据库连接失败:', err);
    } else {
        console.log('✅ 数据库连接成功:', res.rows[0].now);
    }
});

// ============ 表格类型配置相关API ============

// 1. 获取所有表格类型配置
app.get('/api/sheet-types', async (req, res) => {
    try {
        const query = `
            SELECT type_key, display_name, description, columns_config,
                   settings, validation_rules, aggregation_config, theme_config
            FROM gtm_sheet_types
            WHERE is_active = true
            ORDER BY display_name
        `;
        const result = await pool.query(query);
        res.json(result.rows);
    } catch (err) {
        console.error('获取表格类型失败:', err);
        res.status(500).json({ error: '获取表格类型失败' });
    }
});

// 2. 获取特定表格类型配置
app.get('/api/sheet-types/:typeKey', async (req, res) => {
    try {
        const { typeKey } = req.params;
        const query = `
            SELECT type_key, display_name, description, columns_config,
                   settings, validation_rules, aggregation_config, theme_config
            FROM gtm_sheet_types
            WHERE type_key = $1 AND is_active = true
        `;
        const result = await pool.query(query, [typeKey]);

        if (result.rows.length === 0) {
            return res.status(404).json({ error: '表格类型不存在' });
        }

        res.json(result.rows[0]);
    } catch (err) {
        console.error('获取表格类型配置失败:', err);
        res.status(500).json({ error: '获取表格类型配置失败' });
    }
});

// ============ 表格实例相关API ============

// 3. 获取项目的某类型表格列表
app.get('/api/projects/:projectId/sheets/:sheetType', async (req, res) => {
    try {
        const { projectId, sheetType } = req.params;

        const query = `
            SELECT s.*, u.display_name as creator_name,
                   st.display_name as type_display_name,
                   jsonb_array_length(s.data) as item_count
            FROM gtm_sheets s
            LEFT JOIN users u ON s.created_by = u.id
            LEFT JOIN gtm_sheet_types st ON s.sheet_type = st.type_key
            WHERE s.project_id = $1 AND s.sheet_type = $2
            ORDER BY s.created_at DESC
        `;

        const result = await pool.query(query, [projectId, sheetType]);
        res.json(result.rows);
    } catch (err) {
        console.error('获取表格列表失败:', err);
        res.status(500).json({ error: '获取表格列表失败' });
    }
});

// 4. 获取项目的所有表格（所有类型）
app.get('/api/projects/:projectId/sheets', async (req, res) => {
    try {
        const { projectId } = req.params;

        const query = `
            SELECT s.*, u.display_name as creator_name,
                   st.display_name as type_display_name,
                   jsonb_array_length(s.data) as item_count
            FROM gtm_sheets s
            LEFT JOIN users u ON s.created_by = u.id
            LEFT JOIN gtm_sheet_types st ON s.sheet_type = st.type_key
            WHERE s.project_id = $1
            ORDER BY s.sheet_type, s.created_at DESC
        `;

        const result = await pool.query(query, [projectId]);

        // 按表格类型分组
        const groupedSheets = {};
        result.rows.forEach(sheet => {
            if (!groupedSheets[sheet.sheet_type]) {
                groupedSheets[sheet.sheet_type] = {
                    type_key: sheet.sheet_type,
                    type_display_name: sheet.type_display_name,
                    sheets: []
                };
            }
            groupedSheets[sheet.sheet_type].sheets.push(sheet);
        });

        res.json(Object.values(groupedSheets));
    } catch (err) {
        console.error('获取项目表格失败:', err);
        res.status(500).json({ error: '获取项目表格失败' });
    }
});

// 5. 获取特定表格详情
app.get('/api/sheets/:sheetId', async (req, res) => {
    try {
        const { sheetId } = req.params;

        const query = `
            SELECT s.*, u.display_name as creator_name,
                   st.display_name as type_display_name,
                   st.columns_config, st.settings, st.theme_config
            FROM gtm_sheets s
            LEFT JOIN users u ON s.created_by = u.id
            LEFT JOIN gtm_sheet_types st ON s.sheet_type = st.type_key
            WHERE s.id = $1
        `;

        const result = await pool.query(query, [sheetId]);

        if (result.rows.length === 0) {
            return res.status(404).json({ error: '表格不存在' });
        }

        res.json(result.rows[0]);
    } catch (err) {
        console.error('获取表格详情失败:', err);
        res.status(500).json({ error: '获取表格详情失败' });
    }
});

// 6. 创建新表格
app.post('/api/projects/:projectId/sheets/:sheetType', async (req, res) => {
    const client = await pool.connect();

    try {
        await client.query('BEGIN');

        const { projectId, sheetType } = req.params;
        const { sheet_name, period, data, created_by } = req.body;

        // 验证表格类型是否存在
        const typeCheck = await client.query(
            'SELECT 1 FROM gtm_sheet_types WHERE type_key = $1 AND is_active = true',
            [sheetType]
        );

        if (typeCheck.rows.length === 0) {
            await client.query('ROLLBACK');
            return res.status(400).json({ error: '无效的表格类型' });
        }

        // 创建表格
        const insertQuery = `
            INSERT INTO gtm_sheets (project_id, sheet_type, sheet_name, period, data, created_by, status)
            VALUES ($1, $2, $3, $4, $5, $6, 'draft')
            RETURNING id
        `;

        const result = await client.query(insertQuery, [
            projectId,
            sheetType,
            sheet_name || `新建${sheetType}表格`,
            period,
            JSON.stringify(data || []),
            created_by
        ]);

        const sheetId = result.rows[0].id;

        // 记录历史版本
        await client.query(`
            INSERT INTO gtm_sheet_history (sheet_id, version, data, changed_by, change_summary)
            VALUES ($1, 1, $2, $3, '创建表格')
        `, [sheetId, JSON.stringify(data || []), created_by]);

        await client.query('COMMIT');
        res.json({ id: sheetId, message: '创建成功' });

    } catch (err) {
        await client.query('ROLLBACK');
        console.error('创建表格失败:', err);
        res.status(500).json({ error: '创建表格失败' });
    } finally {
        client.release();
    }
});

// 7. 更新表格
app.put('/api/sheets/:sheetId', async (req, res) => {
    const client = await pool.connect();

    try {
        await client.query('BEGIN');

        const { sheetId } = req.params;
        const { sheet_name, period, data, updated_by } = req.body;

        // 获取当前版本信息
        const currentSheet = await client.query(
            'SELECT version, data FROM gtm_sheets WHERE id = $1',
            [sheetId]
        );

        if (currentSheet.rows.length === 0) {
            await client.query('ROLLBACK');
            return res.status(404).json({ error: '表格不存在' });
        }

        const newVersion = currentSheet.rows[0].version + 1;

        // 更新表格
        const updateQuery = `
            UPDATE gtm_sheets
            SET sheet_name = $1, period = $2, data = $3, version = $4, updated_at = NOW()
            WHERE id = $5
        `;

        await client.query(updateQuery, [
            sheet_name,
            period,
            JSON.stringify(data),
            newVersion,
            sheetId
        ]);

        // 记录历史版本
        await client.query(`
            INSERT INTO gtm_sheet_history (sheet_id, version, data, changed_by, change_summary)
            VALUES ($1, $2, $3, $4, '更新表格数据')
        `, [sheetId, newVersion, JSON.stringify(data), updated_by]);

        await client.query('COMMIT');
        res.json({ message: '更新成功' });

    } catch (err) {
        await client.query('ROLLBACK');
        console.error('更新表格失败:', err);
        res.status(500).json({ error: '更新表格失败' });
    } finally {
        client.release();
    }
});

// 8. 删除表格
app.delete('/api/sheets/:sheetId', async (req, res) => {
    try {
        const { sheetId } = req.params;

        const result = await pool.query('DELETE FROM gtm_sheets WHERE id = $1', [sheetId]);

        if (result.rowCount === 0) {
            return res.status(404).json({ error: '表格不存在' });
        }

        res.json({ message: '删除成功' });
    } catch (err) {
        console.error('删除表格失败:', err);
        res.status(500).json({ error: '删除表格失败' });
    }
});

// 9. 发布表格（改变状态）
app.put('/api/sheets/:sheetId/publish', async (req, res) => {
    try {
        const { sheetId } = req.params;

        const result = await pool.query(
            'UPDATE gtm_sheets SET status = $1, updated_at = NOW() WHERE id = $2',
            ['published', sheetId]
        );

        if (result.rowCount === 0) {
            return res.status(404).json({ error: '表格不存在' });
        }

        res.json({ message: '发布成功' });
    } catch (err) {
        console.error('发布表格失败:', err);
        res.status(500).json({ error: '发布表格失败' });
    }
});

// ============ 项目信息API（兼容现有系统）============

// 10. 获取项目基本信息
app.get('/api/projects/:projectId', async (req, res) => {
    try {
        const { projectId } = req.params;

        const query = `
            SELECT p.*, u.display_name as owner_name
            FROM gtm_projects p
            LEFT JOIN users u ON p.owner_id = u.id
            WHERE p.id = $1
        `;

        const result = await pool.query(query, [projectId]);

        if (result.rows.length === 0) {
            return res.status(404).json({ error: '项目不存在' });
        }

        res.json(result.rows[0]);
    } catch (err) {
        console.error('获取项目信息失败:', err);
        res.status(500).json({ error: '获取项目信息失败' });
    }
});

// 错误处理中间件
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ error: '服务器内部错误' });
});

// 启动服务器
app.listen(port, () => {
    console.log(`🚀 GTM通用表格API服务器启动成功！`);
    console.log(`📍 服务地址: http://localhost:${port}`);
    console.log(`🎯 新版API特性:`);
    console.log(`   • 支持多种表格类型的统一管理`);
    console.log(`   • 配置化表格结构`);
    console.log(`   • 版本历史记录`);
    console.log(`   • 灵活的数据模型`);
    console.log(`📊 API端点:`);
    console.log(`   GET  /api/sheet-types - 获取所有表格类型`);
    console.log(`   GET  /api/sheet-types/:type - 获取表格类型配置`);
    console.log(`   GET  /api/projects/:id/sheets/:type - 获取项目特定类型表格`);
    console.log(`   GET  /api/projects/:id/sheets - 获取项目所有表格`);
    console.log(`   POST /api/projects/:id/sheets/:type - 创建新表格`);
    console.log(`   GET  /api/sheets/:id - 获取表格详情`);
    console.log(`   PUT  /api/sheets/:id - 更新表格`);
    console.log(`   DELETE /api/sheets/:id - 删除表格`);
    console.log(`   PUT  /api/sheets/:id/publish - 发布表格`);
});

module.exports = app;