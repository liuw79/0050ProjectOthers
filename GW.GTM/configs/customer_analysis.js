// 客户分析表配置
export const CUSTOMER_ANALYSIS_CONFIG = {
    type: 'customer_analysis',
    displayName: '目标客户分析表',
    description: '分析目标客户群体特征，制定精准营销策略',

    columns: [
        {
            key: 'customer_segment',
            label: '客户群体',
            type: 'text',
            required: true,
            width: '15%',
            placeholder: '输入客户群体名称'
        },
        {
            key: 'characteristics',
            label: '特征描述',
            type: 'textarea',
            width: '25%',
            placeholder: '描述客户群体特征'
        },
        {
            key: 'pain_points',
            label: '痛点需求',
            type: 'textarea',
            width: '20%',
            placeholder: '客户痛点和需求'
        },
        {
            key: 'contact_channels',
            label: '接触渠道',
            type: 'textarea',
            width: '20%',
            placeholder: '有效的接触渠道'
        },
        {
            key: 'expected_value',
            label: '预期价值',
            type: 'text',
            width: '20%',
            placeholder: '客户生命周期价值'
        }
    ],

    settings: {
        autoSave: true,
        autoSaveDelay: 3000,
        defaultRows: 6,
        maxRows: 20,
        allowAddRows: true,
        allowDeleteRows: true
    },

    validation: {
        minRows: 1,
        requiredFields: ['customer_segment']
    },

    aggregation: {
        summaryFields: ['customer_segment', 'pain_points', 'contact_channels'],
        overallMetrics: {
            total_segments: {
                label: '客户群体数量',
                formula: (data) => data.filter(row => row.customer_segment?.trim()).length
            }
        }
    },

    theme: {
        headerColor: '#52c41a',
        accentColor: '#389e0d',
        successColor: '#52c41a',
        warningColor: '#faad14',
        errorColor: '#ff4d4f'
    }
};