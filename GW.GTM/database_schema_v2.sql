-- GTM表格系统重构数据库设计 V2
-- 支持多种表格类型的通用数据模型

-- 1. 表格类型配置表
CREATE TABLE gtm_sheet_types (
    id SERIAL PRIMARY KEY,
    type_key VARCHAR(50) UNIQUE NOT NULL,      -- 如: target_achievement, customer_analysis
    display_name VARCHAR(255) NOT NULL,        -- 显示名称
    description TEXT,                          -- 描述
    columns_config JSONB NOT NULL,             -- 列配置 JSON
    settings JSONB DEFAULT '{}',               -- 表格设置
    validation_rules JSONB DEFAULT '{}',       -- 验证规则
    aggregation_config JSONB DEFAULT '{}',     -- 汇总配置
    theme_config JSONB DEFAULT '{}',           -- 主题配置
    is_active BOOLEAN DEFAULT true,            -- 是否启用
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 2. 通用表格实例表
CREATE TABLE gtm_sheets (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES gtm_projects(id) ON DELETE CASCADE,
    sheet_type VARCHAR(50) REFERENCES gtm_sheet_types(type_key),
    sheet_name VARCHAR(255) NOT NULL,          -- 表格名称
    period VARCHAR(100),                       -- 统计周期
    status VARCHAR(20) DEFAULT 'draft',        -- draft, published, archived
    data JSONB NOT NULL DEFAULT '[]',          -- 表格数据 JSON数组
    metadata JSONB DEFAULT '{}',               -- 元数据
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 3. 表格历史版本表（用于审计和回滚）
CREATE TABLE gtm_sheet_history (
    id SERIAL PRIMARY KEY,
    sheet_id INTEGER REFERENCES gtm_sheets(id) ON DELETE CASCADE,
    version INTEGER NOT NULL,
    data JSONB NOT NULL,                       -- 历史数据
    changed_by INTEGER REFERENCES users(id),
    change_summary TEXT,                       -- 变更说明
    created_at TIMESTAMP DEFAULT NOW()
);

-- 4. 项目汇总报告表
CREATE TABLE gtm_summary_reports (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES gtm_projects(id) ON DELETE CASCADE,
    report_name VARCHAR(255) NOT NULL,
    report_type VARCHAR(50) DEFAULT 'comprehensive', -- comprehensive, custom
    source_sheets JSONB NOT NULL,              -- 来源表格配置 [{"sheet_type": "target_achievement", "sheet_id": 1}]
    summary_data JSONB NOT NULL DEFAULT '{}',  -- 汇总数据
    generated_at TIMESTAMP,                    -- 生成时间
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 5. 创建索引
CREATE INDEX idx_gtm_sheets_project_type ON gtm_sheets(project_id, sheet_type);
CREATE INDEX idx_gtm_sheets_type ON gtm_sheets(sheet_type);
CREATE INDEX idx_gtm_sheets_status ON gtm_sheets(status);
CREATE INDEX idx_gtm_sheets_created ON gtm_sheets(created_at);
CREATE INDEX idx_gtm_sheet_history_sheet ON gtm_sheet_history(sheet_id);
CREATE INDEX idx_gtm_summary_reports_project ON gtm_summary_reports(project_id);

-- 6. 创建更新时间触发器
CREATE TRIGGER update_gtm_sheet_types_updated_at
    BEFORE UPDATE ON gtm_sheet_types
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_gtm_sheets_updated_at
    BEFORE UPDATE ON gtm_sheets
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_gtm_summary_reports_updated_at
    BEFORE UPDATE ON gtm_summary_reports
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- 7. 插入基础表格类型配置
INSERT INTO gtm_sheet_types (type_key, display_name, description, columns_config, settings, validation_rules, aggregation_config, theme_config) VALUES

-- 目标达成回顾表
('target_achievement', '目标达成回顾表', '分析阶段性目标完成情况，识别差距并制定改进措施',
'[
    {"key": "indicator_name", "label": "指标", "type": "text", "required": true, "width": "20%", "placeholder": "输入指标名称"},
    {"key": "target_value", "label": "阶段目标", "type": "text", "width": "15%", "placeholder": "输入目标值"},
    {"key": "actual_value", "label": "实际达成", "type": "text", "width": "15%", "placeholder": "输入实际值"},
    {"key": "achievement_rate", "label": "达成率", "type": "percentage", "width": "15%", "autoCalc": true, "placeholder": "自动计算或手动输入"},
    {"key": "gap_analysis", "label": "差距分析", "type": "textarea", "width": "35%", "placeholder": "输入差距分析"}
]',
'{"autoSave": true, "autoSaveDelay": 3000, "defaultRows": 5, "maxRows": 50, "allowAddRows": true, "allowDeleteRows": true}',
'{"minRows": 1, "requiredFields": ["indicator_name"]}',
'{"summaryFields": ["indicator_name", "achievement_rate", "gap_analysis"]}',
'{"headerColor": "#4a9eff", "accentColor": "#1890ff", "successColor": "#52c41a", "warningColor": "#faad14", "errorColor": "#ff4d4f"}'
),

-- 客户分析表
('customer_analysis', '目标客户分析表', '分析目标客户群体特征，制定精准营销策略',
'[
    {"key": "customer_segment", "label": "客户群体", "type": "text", "required": true, "width": "15%", "placeholder": "输入客户群体名称"},
    {"key": "characteristics", "label": "特征描述", "type": "textarea", "width": "25%", "placeholder": "描述客户群体特征"},
    {"key": "pain_points", "label": "痛点需求", "type": "textarea", "width": "20%", "placeholder": "客户痛点和需求"},
    {"key": "contact_channels", "label": "接触渠道", "type": "textarea", "width": "20%", "placeholder": "有效的接触渠道"},
    {"key": "expected_value", "label": "预期价值", "type": "text", "width": "20%", "placeholder": "客户生命周期价值"}
]',
'{"autoSave": true, "autoSaveDelay": 3000, "defaultRows": 6, "maxRows": 20, "allowAddRows": true, "allowDeleteRows": true}',
'{"minRows": 1, "requiredFields": ["customer_segment"]}',
'{"summaryFields": ["customer_segment", "pain_points", "contact_channels"]}',
'{"headerColor": "#52c41a", "accentColor": "#389e0d", "successColor": "#52c41a", "warningColor": "#faad14", "errorColor": "#ff4d4f"}'
),

-- 竞品分析表
('competitor_analysis', '竞品分析表', '深入分析竞争对手，识别差异化机会',
'[
    {"key": "competitor_name", "label": "竞品名称", "type": "text", "required": true, "width": "15%", "placeholder": "竞争对手名称"},
    {"key": "core_features", "label": "核心功能", "type": "textarea", "width": "20%", "placeholder": "主要功能特性"},
    {"key": "pricing_strategy", "label": "定价策略", "type": "text", "width": "15%", "placeholder": "价格区间和策略"},
    {"key": "target_market", "label": "目标市场", "type": "text", "width": "15%", "placeholder": "主要客户群体"},
    {"key": "strengths_weaknesses", "label": "优劣势分析", "type": "textarea", "width": "25%", "placeholder": "竞品的优势和劣势"},
    {"key": "market_share", "label": "市场份额", "type": "text", "width": "10%", "placeholder": "市场占有率"}
]',
'{"autoSave": true, "autoSaveDelay": 3000, "defaultRows": 5, "maxRows": 15, "allowAddRows": true, "allowDeleteRows": true}',
'{"minRows": 1, "requiredFields": ["competitor_name"]}',
'{"summaryFields": ["competitor_name", "core_features", "strengths_weaknesses"]}',
'{"headerColor": "#fa8c16", "accentColor": "#d46b08", "successColor": "#52c41a", "warningColor": "#faad14", "errorColor": "#ff4d4f"}'
);

-- 8. 数据迁移准备
-- 将现有的 target_achievement_reviews 和 target_achievement_items 数据迁移到新结构

-- 创建迁移函数
CREATE OR REPLACE FUNCTION migrate_target_achievement_data()
RETURNS void AS $$
DECLARE
    review_record RECORD;
    items_data JSONB;
BEGIN
    -- 遍历现有的目标达成回顾
    FOR review_record IN
        SELECT r.*, u.display_name as creator_name
        FROM target_achievement_reviews r
        LEFT JOIN users u ON r.created_by = u.id
    LOOP
        -- 获取该回顾的所有明细项目
        SELECT jsonb_agg(
            jsonb_build_object(
                'indicator_name', indicator_name,
                'target_value', target_value,
                'actual_value', actual_value,
                'achievement_rate', achievement_rate,
                'gap_analysis', gap_analysis
            ) ORDER BY sort_order
        ) INTO items_data
        FROM target_achievement_items
        WHERE review_id = review_record.id;

        -- 插入到新的表格系统
        INSERT INTO gtm_sheets (
            project_id,
            sheet_type,
            sheet_name,
            period,
            status,
            data,
            created_by,
            created_at,
            updated_at
        ) VALUES (
            review_record.project_id,
            'target_achievement',
            review_record.review_name,
            review_record.review_period,
            'published',
            COALESCE(items_data, '[]'::jsonb),
            review_record.created_by,
            review_record.created_at,
            review_record.updated_at
        );
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- 注释：执行迁移需要手动调用
-- SELECT migrate_target_achievement_data();

-- 9. 清理旧表（迁移完成后可选）
-- DROP TABLE IF EXISTS target_achievement_items;
-- DROP TABLE IF EXISTS target_achievement_reviews;