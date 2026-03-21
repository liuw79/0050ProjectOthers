// 产品复盘表配置
export const PRODUCT_REVIEW_CONFIG = {
    type: 'product_review',
    displayName: '产品复盘表',
    description: '全面复盘产品表现，识别优势、不足和待解决问题',

    // 表格列配置 - 基于图片的三个方面结构
    columns: [
        {
            key: 'review_aspect',
            label: '三个方面',
            type: 'select',
            required: true,
            width: '15%',
            options: [
                { value: 'good_performance', label: '做的好的' },
                { value: 'poor_performance', label: '做的不好' },
                { value: 'unsolved_issues', label: '依然没有解决的问题' }
            ],
            placeholder: '选择复盘方面'
        },
        {
            key: 'top3_items',
            label: 'TOP3的表现',
            type: 'textarea',
            width: '42%',
            placeholder: '请列出3个最重要的表现：\n1. \n2. \n3. ',
            rows: 6
        },
        {
            key: 'root_causes',
            label: '原因',
            type: 'textarea',
            width: '43%',
            placeholder: '请分析对应的原因：\n1. \n2. \n3. ',
            rows: 6
        }
    ],

    // 表格设置
    settings: {
        autoSave: true,
        autoSaveDelay: 3000,
        defaultRows: 3, // 默认3行，对应3个方面
        maxRows: 10,
        allowAddRows: true,
        allowDeleteRows: false, // 建议不允许删除，保持结构完整性
        showRowNumbers: false,
        groupByColumn: 'review_aspect' // 按复盘方面分组显示
    },

    // 验证规则
    validation: {
        minRows: 3, // 至少要有3个方面
        requiredFields: ['review_aspect', 'top3_items'],
        customValidation: (data) => {
            const errors = [];

            // 检查是否包含三个必要方面
            const aspects = data.map(row => row.review_aspect).filter(aspect => aspect);
            const requiredAspects = ['good_performance', 'poor_performance', 'unsolved_issues'];

            requiredAspects.forEach(aspect => {
                if (!aspects.includes(aspect)) {
                    const aspectNames = {
                        'good_performance': '做的好的',
                        'poor_performance': '做的不好',
                        'unsolved_issues': '依然没有解决的问题'
                    };
                    errors.push(`缺少"${aspectNames[aspect]}"方面的复盘`);
                }
            });

            return errors;
        }
    },

    // 汇总配置
    aggregation: {
        summaryFields: ['review_aspect', 'top3_items', 'root_causes'],
        overallMetrics: {
            total_good_items: {
                label: '优势项目数',
                formula: (data) => {
                    const goodItems = data.filter(row => row.review_aspect === 'good_performance');
                    return goodItems.length;
                }
            },
            total_improvement_areas: {
                label: '改进领域数',
                formula: (data) => {
                    const poorItems = data.filter(row => row.review_aspect === 'poor_performance');
                    return poorItems.length;
                }
            },
            unresolved_issues_count: {
                label: '待解决问题数',
                formula: (data) => {
                    const unsolvedItems = data.filter(row => row.review_aspect === 'unsolved_issues');
                    return unsolvedItems.length;
                }
            }
        }
    },

    // UI主题 - 使用蓝色系，符合图片设计
    theme: {
        headerColor: '#1890ff',
        accentColor: '#0050b3',
        successColor: '#52c41a',
        warningColor: '#faad14',
        errorColor: '#ff4d4f'
    },

    // 特殊设置：预定义行数据
    defaultData: [
        {
            review_aspect: 'good_performance',
            top3_items: '1. \n2. \n3. ',
            root_causes: '1. \n2. \n3. '
        },
        {
            review_aspect: 'poor_performance',
            top3_items: '1. \n2. \n3. ',
            root_causes: '1. \n2. \n3. '
        },
        {
            review_aspect: 'unsolved_issues',
            top3_items: '1. \n2. \n3. ',
            root_causes: '1. \n2. \n3. '
        }
    ]
};