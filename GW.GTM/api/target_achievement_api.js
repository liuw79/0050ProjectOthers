// GTM目标达成回顾表 API接口
// Node.js + Express + PostgreSQL

const express = require('express');
const { Pool } = require('pg');
const cors = require('cors');

const app = express();
const port = 3001;

// 中间件
app.use(cors());
app.use(express.json());
app.use(express.static('.')); // 服务当前目录的静态文件

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

// API路由

// 1. 获取项目的所有目标达成回顾
app.get('/api/projects/:projectId/target-reviews', async (req, res) => {
    try {
        const { projectId } = req.params;

        const query = `
            SELECT r.*, u.display_name as creator_name,
                   COUNT(i.id) as item_count
            FROM target_achievement_reviews r
            LEFT JOIN users u ON r.created_by = u.id
            LEFT JOIN target_achievement_items i ON r.id = i.review_id
            WHERE r.project_id = $1
            GROUP BY r.id, u.display_name
            ORDER BY r.created_at DESC
        `;

        const result = await pool.query(query, [projectId]);
        res.json(result.rows);
    } catch (err) {
        console.error('获取目标达成回顾失败:', err);
        res.status(500).json({ error: '获取数据失败' });
    }
});

// 2. 获取特定回顾的详细数据
app.get('/api/target-reviews/:reviewId', async (req, res) => {
    try {
        const { reviewId } = req.params;

        // 获取回顾基本信息
        const reviewQuery = `
            SELECT r.*, u.display_name as creator_name
            FROM target_achievement_reviews r
            LEFT JOIN users u ON r.created_by = u.id
            WHERE r.id = $1
        `;
        const reviewResult = await pool.query(reviewQuery, [reviewId]);

        if (reviewResult.rows.length === 0) {
            return res.status(404).json({ error: '未找到该回顾' });
        }

        // 获取回顾明细项目
        const itemsQuery = `
            SELECT * FROM target_achievement_items
            WHERE review_id = $1
            ORDER BY sort_order, id
        `;
        const itemsResult = await pool.query(itemsQuery, [reviewId]);

        const response = {
            review: reviewResult.rows[0],
            items: itemsResult.rows
        };

        res.json(response);
    } catch (err) {
        console.error('获取回顾详情失败:', err);
        res.status(500).json({ error: '获取数据失败' });
    }
});

// 3. 创建新的目标达成回顾
app.post('/api/projects/:projectId/target-reviews', async (req, res) => {
    const client = await pool.connect();

    try {
        await client.query('BEGIN');

        const { projectId } = req.params;
        const { review_name, review_period, created_by, items } = req.body;

        // 创建回顾记录
        const reviewQuery = `
            INSERT INTO target_achievement_reviews (project_id, review_name, review_period, created_by)
            VALUES ($1, $2, $3, $4)
            RETURNING id
        `;
        const reviewResult = await client.query(reviewQuery, [
            projectId,
            review_name || '阶段目标达成回顾',
            review_period,
            created_by
        ]);

        const reviewId = reviewResult.rows[0].id;

        // 批量插入明细项目
        if (items && items.length > 0) {
            const itemsQuery = `
                INSERT INTO target_achievement_items
                (review_id, indicator_name, target_value, actual_value, achievement_rate, gap_analysis, sort_order)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
            `;

            for (let i = 0; i < items.length; i++) {
                const item = items[i];
                await client.query(itemsQuery, [
                    reviewId,
                    item.indicator_name,
                    item.target_value,
                    item.actual_value,
                    item.achievement_rate,
                    item.gap_analysis,
                    i
                ]);
            }
        }

        await client.query('COMMIT');
        res.json({ id: reviewId, message: '创建成功' });

    } catch (err) {
        await client.query('ROLLBACK');
        console.error('创建回顾失败:', err);
        res.status(500).json({ error: '创建失败' });
    } finally {
        client.release();
    }
});

// 4. 更新目标达成回顾
app.put('/api/target-reviews/:reviewId', async (req, res) => {
    const client = await pool.connect();

    try {
        await client.query('BEGIN');

        const { reviewId } = req.params;
        const { review_name, review_period, items } = req.body;

        // 更新回顾基本信息
        const updateReviewQuery = `
            UPDATE target_achievement_reviews
            SET review_name = $1, review_period = $2, updated_at = NOW()
            WHERE id = $3
        `;
        await client.query(updateReviewQuery, [review_name, review_period, reviewId]);

        // 删除旧的明细项目
        await client.query('DELETE FROM target_achievement_items WHERE review_id = $1', [reviewId]);

        // 插入新的明细项目
        if (items && items.length > 0) {
            const itemsQuery = `
                INSERT INTO target_achievement_items
                (review_id, indicator_name, target_value, actual_value, achievement_rate, gap_analysis, sort_order)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
            `;

            for (let i = 0; i < items.length; i++) {
                const item = items[i];
                if (item.indicator_name && item.indicator_name.trim()) { // 只保存有内容的行
                    await client.query(itemsQuery, [
                        reviewId,
                        item.indicator_name,
                        item.target_value || '',
                        item.actual_value || '',
                        item.achievement_rate || '',
                        item.gap_analysis || '',
                        i
                    ]);
                }
            }
        }

        await client.query('COMMIT');
        res.json({ message: '更新成功' });

    } catch (err) {
        await client.query('ROLLBACK');
        console.error('更新回顾失败:', err);
        res.status(500).json({ error: '更新失败' });
    } finally {
        client.release();
    }
});

// 5. 删除目标达成回顾
app.delete('/api/target-reviews/:reviewId', async (req, res) => {
    try {
        const { reviewId } = req.params;

        // 由于有CASCADE，删除回顾时会自动删除相关的明细项目
        const result = await pool.query('DELETE FROM target_achievement_reviews WHERE id = $1', [reviewId]);

        if (result.rowCount === 0) {
            return res.status(404).json({ error: '未找到该回顾' });
        }

        res.json({ message: '删除成功' });
    } catch (err) {
        console.error('删除回顾失败:', err);
        res.status(500).json({ error: '删除失败' });
    }
});

// 6. 获取项目基本信息（用于页面显示）
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
            return res.status(404).json({ error: '未找到该项目' });
        }

        res.json(result.rows[0]);
    } catch (err) {
        console.error('获取项目信息失败:', err);
        res.status(500).json({ error: '获取数据失败' });
    }
});

// 错误处理中间件
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ error: '服务器内部错误' });
});

// 启动服务器
app.listen(port, () => {
    console.log(`🚀 GTM目标达成API服务器启动成功！`);
    console.log(`📍 服务地址: http://localhost:${port}`);
    console.log(`📊 API文档:`);
    console.log(`   GET /api/projects/:projectId/target-reviews - 获取项目的目标达成回顾列表`);
    console.log(`   GET /api/target-reviews/:reviewId - 获取回顾详情`);
    console.log(`   POST /api/projects/:projectId/target-reviews - 创建新回顾`);
    console.log(`   PUT /api/target-reviews/:reviewId - 更新回顾`);
    console.log(`   DELETE /api/target-reviews/:reviewId - 删除回顾`);
});

module.exports = app;