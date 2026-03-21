-- GTM作业AI助手数据库设计
-- 使用PostgreSQL + JSONB实现灵活且安全的数据存储

-- 用户表
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    display_name VARCHAR(100),
    avatar_url TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- GTM项目表
CREATE TABLE gtm_projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    owner_id INTEGER REFERENCES users(id),
    status VARCHAR(50) DEFAULT 'active', -- active, completed, archived
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- GTM工作表类型定义
CREATE TABLE sheet_templates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,        -- 如：目标客户分析表、竞品分析表等
    description TEXT,
    structure JSONB NOT NULL,          -- 表格结构定义
    ai_prompts JSONB,                  -- AI助手提示配置
    validation_rules JSONB,            -- 数据验证规则
    created_at TIMESTAMP DEFAULT NOW()
);

-- GTM工作表实例
CREATE TABLE gtm_sheets (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES gtm_projects(id) ON DELETE CASCADE,
    template_id INTEGER REFERENCES sheet_templates(id),
    name VARCHAR(255) NOT NULL,
    data JSONB NOT NULL DEFAULT '{}',  -- 表格数据
    ai_suggestions JSONB DEFAULT '{}', -- AI建议
    completion_status JSONB DEFAULT '{}', -- 填写完成状态
    version INTEGER DEFAULT 1,
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 操作历史记录
CREATE TABLE sheet_history (
    id SERIAL PRIMARY KEY,
    sheet_id INTEGER REFERENCES gtm_sheets(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id),
    operation_type VARCHAR(50),        -- insert, update, delete, ai_suggest
    old_data JSONB,
    new_data JSONB,
    change_summary TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- GTM行动方案汇总表
CREATE TABLE gtm_action_plans (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES gtm_projects(id) ON DELETE CASCADE,
    plan_data JSONB NOT NULL,          -- 汇总的行动方案
    auto_generated BOOLEAN DEFAULT true, -- 是否AI自动生成
    approved_by INTEGER REFERENCES users(id),
    approved_at TIMESTAMP,
    version INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 项目协作者
CREATE TABLE project_collaborators (
    project_id INTEGER REFERENCES gtm_projects(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(50) DEFAULT 'member', -- owner, admin, member, viewer
    joined_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (project_id, user_id)
);

-- 创建索引优化查询性能
CREATE INDEX idx_gtm_sheets_project ON gtm_sheets(project_id);
CREATE INDEX idx_gtm_sheets_data ON gtm_sheets USING gin(data);
CREATE INDEX idx_sheet_history_sheet ON sheet_history(sheet_id);
CREATE INDEX idx_sheet_history_created ON sheet_history(created_at);
CREATE INDEX idx_action_plans_project ON gtm_action_plans(project_id);

-- 创建更新时间触发器
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_gtm_projects_updated_at BEFORE UPDATE ON gtm_projects
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_gtm_sheets_updated_at BEFORE UPDATE ON gtm_sheets
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_gtm_action_plans_updated_at BEFORE UPDATE ON gtm_action_plans
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- 插入示例模板数据
INSERT INTO sheet_templates (name, description, structure, ai_prompts) VALUES
('目标客户分析表', 'GTM战略中的目标客户群体分析',
 '{"columns": ["客户群体", "特征描述", "需求分析", "接触渠道", "预期价值"], "rows": 10}',
 '{"customer_analysis": "请基于产品特性分析目标客户群体...", "channel_suggestion": "建议最有效的客户接触渠道..."}'
),
('竞品分析表', '竞争对手产品和策略分析',
 '{"columns": ["竞品名称", "核心功能", "定价策略", "目标客户", "优劣势分析"], "rows": 8}',
 '{"competitor_analysis": "请分析主要竞争对手的产品特点...", "positioning_advice": "基于竞品情况建议产品定位..."}'
),
('市场推广策略表', '产品上市推广渠道和策略规划',
 '{"columns": ["推广渠道", "目标受众", "预算分配", "时间计划", "预期效果"], "rows": 12}',
 '{"channel_optimization": "建议最适合的推广渠道组合...", "budget_allocation": "建议合理的预算分配比例..."}'
);

-- 数据备份和恢复说明注释
-- 备份：pg_dump gtm_assistant > backup.sql
-- 恢复：psql gtm_assistant < backup.sql
-- 实时备份：可以设置pg_basebackup定期备份