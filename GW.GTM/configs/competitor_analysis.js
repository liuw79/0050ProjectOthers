// 竞品分析表配置
export const COMPETITOR_ANALYSIS_CONFIG = {
    type: 'competitor_analysis',
    displayName: '竞品分析表',
    description: '深入分析竞争对手，识别差异化机会',

    columns: [
        {
            key: 'competitor_name',
            label: '竞品名称',
            type: 'text',
            required: true,
            width: '15%',
            placeholder: '竞争对手名称'
        },
        {
            key: 'core_features',
            label: '核心功能',
            type: 'textarea',
            width: '20%',
            placeholder: '主要功能特性'
        },
        {
            key: 'pricing_strategy',
            label: '定价策略',
            type: 'text',
            width: '15%',
            placeholder: '价格区间和策略'
        },
        {
            key: 'target_market',
            label: '目标市场',
            type: 'text',
            width: '15%',
            placeholder: '主要客户群体'
        },
        {
            key: 'strengths_weaknesses',
            label: '优劣势分析',
            type: 'textarea',
            width: '25%',
            placeholder: '竞品的优势和劣势'
        },
        {
            key: 'market_share',
            label: '市场份额',
            type: 'text',
            width: '10%',
            placeholder: '市场占有率'
        }
    ],

    settings: {
        autoSave: true,
        autoSaveDelay: 3000,
        defaultRows: 5,
        maxRows: 15,
        allowAddRows: true,
        allowDeleteRows: true
    },

    validation: {
        minRows: 1,
        requiredFields: ['competitor_name']
    },

    aggregation: {
        summaryFields: ['competitor_name', 'core_features', 'strengths_weaknesses'],
        overallMetrics: {
            competitor_count: {
                label: '竞品数量',
                formula: (data) => data.filter(row => row.competitor_name?.trim()).length
            }
        }
    },

    theme: {
        headerColor: '#fa8c16',
        accentColor: '#d46b08',
        successColor: '#52c41a',
        warningColor: '#faad14',
        errorColor: '#ff4d4f'
    }
};