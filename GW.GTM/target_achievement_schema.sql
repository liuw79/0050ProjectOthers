-- 目标达成回顾表结构
-- 创建目标达成回顾主表
CREATE TABLE target_achievement_reviews (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES gtm_projects(id) ON DELETE CASCADE,
    review_name VARCHAR(255) NOT NULL DEFAULT '阶段目标达成回顾',
    review_period VARCHAR(100),  -- 回顾周期，如"2024年Q1"
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 创建目标达成明细项目表
CREATE TABLE target_achievement_items (
    id SERIAL PRIMARY KEY,
    review_id INTEGER REFERENCES target_achievement_reviews(id) ON DELETE CASCADE,
    indicator_name VARCHAR(255) NOT NULL,  -- 指标名称
    target_value VARCHAR(100),             -- 目标值
    actual_value VARCHAR(100),             -- 实际值
    achievement_rate VARCHAR(50),          -- 达成率
    gap_analysis TEXT,                     -- 差距分析
    sort_order INTEGER DEFAULT 0,         -- 排序字段
    created_at TIMESTAMP DEFAULT NOW()
);

-- 创建索引优化查询
CREATE INDEX idx_target_reviews_project ON target_achievement_reviews(project_id);
CREATE INDEX idx_target_items_review ON target_achievement_items(review_id);

-- 创建更新时间触发器
CREATE TRIGGER update_target_reviews_updated_at
    BEFORE UPDATE ON target_achievement_reviews
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- 插入示例数据（可选）
INSERT INTO target_achievement_reviews (project_id, review_name, review_period, created_by)
VALUES (1, '2024年Q1目标达成回顾', '2024年Q1', 1);

INSERT INTO target_achievement_items (review_id, indicator_name, target_value, actual_value, achievement_rate, gap_analysis, sort_order)
VALUES
(1, '月活跃用户数', '10,000', '8,500', '85%', '距离目标还差1,500用户，主要原因是新用户获取渠道效果不及预期', 0),
(1, '客户满意度', '90%', '92%', '102%', '超出预期，用户反馈整体积极', 1),
(1, '收入增长率', '20%', '15%', '75%', '收入增长低于预期，需要优化定价策略', 2);