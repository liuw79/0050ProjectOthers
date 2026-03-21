# GTM表格系统重构方案

## 🎯 目标
支持7-8个表格，实现数据汇总，保持系统简洁统一，降低维护成本

## 🏗️ 架构设计

### 1. 数据库层重构
```sql
-- 通用表格配置表
CREATE TABLE sheet_configs (
    id SERIAL PRIMARY KEY,
    sheet_type VARCHAR(50) NOT NULL,  -- 'target_achievement', 'customer_analysis', etc.
    display_name VARCHAR(255),
    columns_config JSONB NOT NULL,    -- 列配置
    validation_rules JSONB,           -- 验证规则
    auto_calc_rules JSONB,           -- 自动计算规则
    created_at TIMESTAMP DEFAULT NOW()
);

-- 通用表格数据表
CREATE TABLE sheet_data (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES gtm_projects(id),
    sheet_type VARCHAR(50) NOT NULL,
    sheet_name VARCHAR(255),
    period VARCHAR(100),
    data JSONB NOT NULL,              -- 灵活的数据存储
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 汇总报告表
CREATE TABLE summary_reports (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES gtm_projects(id),
    report_name VARCHAR(255),
    source_sheets JSONB,              -- 来源表格IDs
    summary_data JSONB,               -- 汇总数据
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 2. 前端组件化架构

#### 核心组件：
- `GTMTable`：通用表格组件
- `SheetManager`：表格管理器
- `DataAggregator`：数据汇总器
- `ConfigManager`：配置管理器

#### 文件结构：
```
/components/
  ├── GTMTable.js          # 通用表格组件
  ├── SheetManager.js      # 表格管理器
  ├── DataAggregator.js    # 数据汇总
  └── ConfigManager.js     # 配置管理

/configs/
  ├── target_achievement.js    # 目标达成表配置
  ├── customer_analysis.js     # 客户分析表配置
  ├── competitor_analysis.js   # 竞品分析表配置
  └── ...                      # 其他表格配置

/templates/
  └── sheet_template.html      # 统一表格模板

/api/
  ├── gtm_sheets_api.js        # 通用表格API
  └── summary_api.js           # 汇总API
```

### 3. API层重构

#### 统一API接口：
```javascript
// 通用表格CRUD
GET    /api/projects/:id/sheets/:type
POST   /api/projects/:id/sheets/:type
PUT    /api/sheets/:id
DELETE /api/sheets/:id

// 配置管理
GET    /api/sheet-configs/:type
PUT    /api/sheet-configs/:type

// 数据汇总
GET    /api/projects/:id/summary
POST   /api/projects/:id/summary
```

### 4. 配置化表格定义

每个表格类型通过配置文件定义：

```javascript
// target_achievement.js
export const TARGET_ACHIEVEMENT_CONFIG = {
    type: 'target_achievement',
    displayName: '目标达成回顾表',
    columns: [
        {
            key: 'indicator_name',
            label: '指标',
            type: 'text',
            required: true,
            width: '20%'
        },
        {
            key: 'target_value',
            label: '阶段目标',
            type: 'text',
            width: '15%'
        },
        {
            key: 'actual_value',
            label: '实际达成',
            type: 'text',
            width: '15%'
        },
        {
            key: 'achievement_rate',
            label: '达成率',
            type: 'percentage',
            autoCalc: true,
            formula: 'actual_value / target_value * 100',
            width: '15%'
        },
        {
            key: 'gap_analysis',
            label: '差距分析',
            type: 'textarea',
            width: '35%'
        }
    ],
    autoSave: true,
    validation: {
        minRows: 1,
        requiredFields: ['indicator_name']
    }
};
```

## 🚀 实施步骤

### 第一阶段：基础重构
1. 重构数据库设计
2. 创建通用表格组件
3. 迁移现有目标达成表

### 第二阶段：配置化
1. 创建配置管理系统
2. 实现表格类型注册机制
3. 重构API为通用接口

### 第三阶段：多表格支持
1. 添加其余6-7个表格配置
2. 实现表格间数据关联
3. 创建汇总功能

### 第四阶段：优化完善
1. 性能优化
2. 用户体验优化
3. 测试和文档

## 💡 优势

1. **代码复用**：所有表格共享核心组件
2. **配置化**：新增表格只需配置文件
3. **统一性**：UI/UX完全一致
4. **可维护性**：修改一处影响所有表格
5. **扩展性**：易于添加新功能
6. **数据一致性**：统一的数据模型

## 🎯 立即开始的工作

1. 创建通用表格组件
2. 重构数据库结构
3. 建立配置系统
4. 迁移现有表格