// 目标达成回顾表配置
export const TARGET_ACHIEVEMENT_CONFIG = {
    type: 'target_achievement',
    displayName: '目标达成回顾表',
    description: '分析阶段性目标完成情况，识别差距并制定改进措施',

    // 表格列配置
    columns: [
        {
            key: 'indicator_name',
            label: '指标',
            type: 'text',
            required: true,
            width: '20%',
            placeholder: '输入指标名称'
        },
        {
            key: 'target_value',
            label: '阶段目标',
            type: 'text',
            width: '15%',
            placeholder: '输入目标值'
        },
        {
            key: 'actual_value',
            label: '实际达成',
            type: 'text',
            width: '15%',
            placeholder: '输入实际值'
        },
        {
            key: 'achievement_rate',
            label: '达成率',
            type: 'percentage',
            width: '15%',
            autoCalc: true,
            formula: (row) => {
                const target = parseFloat(row.target_value?.replace(/[,%]/g, ''));
                const actual = parseFloat(row.actual_value?.replace(/[,%]/g, ''));
                if (!isNaN(target) && !isNaN(actual) && target !== 0) {
                    return ((actual / target) * 100).toFixed(1) + '%';
                }
                return '';
            },
            placeholder: '自动计算或手动输入'
        },
        {
            key: 'gap_analysis',
            label: '差距分析',
            type: 'textarea',
            width: '35%',
            placeholder: '输入差距分析'
        }
    ],

    // 表格设置
    settings: {
        autoSave: true,
        autoSaveDelay: 3000,
        defaultRows: 5,
        maxRows: 50,
        allowAddRows: true,
        allowDeleteRows: true,
        showRowNumbers: false
    },

    // 验证规则
    validation: {
        minRows: 1,
        requiredFields: ['indicator_name'],
        customValidation: (data) => {
            // 自定义验证逻辑
            const errors = [];
            if (data.length === 0) {
                errors.push('至少需要一个指标');
            }
            return errors;
        }
    },

    // 汇总配置
    aggregation: {
        // 哪些字段需要在最终汇总中展示
        summaryFields: ['indicator_name', 'achievement_rate', 'gap_analysis'],
        // 计算总体达成率
        overallMetrics: {
            avg_achievement_rate: {
                label: '平均达成率',
                formula: (data) => {
                    const rates = data
                        .map(row => parseFloat(row.achievement_rate?.replace('%', '')))
                        .filter(rate => !isNaN(rate));

                    if (rates.length === 0) return '0%';
                    const avg = rates.reduce((sum, rate) => sum + rate, 0) / rates.length;
                    return avg.toFixed(1) + '%';
                }
            }
        }
    },

    // UI主题
    theme: {
        headerColor: '#4a9eff',
        accentColor: '#1890ff',
        successColor: '#52c41a',
        warningColor: '#faad14',
        errorColor: '#ff4d4f'
    }
};