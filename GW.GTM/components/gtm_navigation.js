// GTM流程导航配置
const GTM_NAVIGATION_CONFIG = {
    steps: [
        {
            id: 'target_achievement',
            name: '目标达成回顾',
            description: '回顾阶段性目标完成情况',
            url: 'http://localhost:3001/target_achievement_table.html',
            status: 'completed' // completed, current, pending, disabled
        },
        {
            id: 'product_review',
            name: '产品复盘',
            description: '全面复盘产品表现',
            url: 'http://localhost:3002/product_review_simple.html',
            status: 'current'
        },
        {
            id: 'customer_analysis',
            name: '客户分析',
            description: '深入分析目标客户群体',
            url: '#',
            status: 'pending'
        },
        {
            id: 'competitor_analysis',
            name: '竞品分析',
            description: '分析竞争对手策略',
            url: '#',
            status: 'pending'
        },
        {
            id: 'market_strategy',
            name: '市场策略',
            description: '制定市场推广策略',
            url: '#',
            status: 'pending'
        },
        {
            id: 'action_plan',
            name: '行动计划',
            description: '具体执行计划制定',
            url: '#',
            status: 'pending'
        },
        {
            id: 'risk_assessment',
            name: '风险评估',
            description: '识别和评估潜在风险',
            url: '#',
            status: 'pending'
        },
        {
            id: 'final_summary',
            name: '综合汇总',
            description: '生成最终GTM报告',
            url: '#',
            status: 'pending'
        }
    ],

    // 根据当前页面自动设置状态
    setCurrentStep: function(currentStepId) {
        this.steps.forEach((step, index) => {
            if (step.id === currentStepId) {
                step.status = 'current';
                // 将当前步骤之前的设为completed
                for (let i = 0; i < index; i++) {
                    this.steps[i].status = 'completed';
                }
                // 将当前步骤之后的设为pending
                for (let i = index + 1; i < this.steps.length; i++) {
                    this.steps[i].status = 'pending';
                }
            }
        });
    },

    // 获取当前步骤
    getCurrentStep: function() {
        return this.steps.find(step => step.status === 'current');
    },

    // 获取下一步骤
    getNextStep: function() {
        const currentIndex = this.steps.findIndex(step => step.status === 'current');
        return currentIndex < this.steps.length - 1 ? this.steps[currentIndex + 1] : null;
    },

    // 获取上一步骤
    getPreviousStep: function() {
        const currentIndex = this.steps.findIndex(step => step.status === 'current');
        return currentIndex > 0 ? this.steps[currentIndex - 1] : null;
    }
};

// 创建导航HTML的函数
function createGTMNavigation(currentStepId) {
    GTM_NAVIGATION_CONFIG.setCurrentStep(currentStepId);

    const navigationHTML = \`
        <div class="gtm-navigation">
            <div class="gtm-nav-container">
                <div class="gtm-nav-header">
                    <h2>GTM作业流程</h2>
                    <div class="gtm-nav-progress">
                        <span class="progress-text">进度: \${GTM_NAVIGATION_CONFIG.steps.filter(s => s.status === 'completed').length + 1}/\${GTM_NAVIGATION_CONFIG.steps.length}</span>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: \${((GTM_NAVIGATION_CONFIG.steps.filter(s => s.status === 'completed').length + 1) / GTM_NAVIGATION_CONFIG.steps.length * 100)}%"></div>
                        </div>
                    </div>
                </div>

                <div class="gtm-nav-steps">
                    \${GTM_NAVIGATION_CONFIG.steps.map((step, index) => \`
                        <div class="gtm-nav-step \${step.status}" onclick="navigateToStep('\${step.id}', '\${step.url}')">
                            <div class="step-number">\${index + 1}</div>
                            <div class="step-content">
                                <div class="step-name">\${step.name}</div>
                                <div class="step-description">\${step.description}</div>
                            </div>
                            <div class="step-status-icon">
                                \${step.status === 'completed' ? '✅' : step.status === 'current' ? '🔄' : '⏸️'}
                            </div>
                        </div>
                    \`).join('')}
                </div>

                <div class="gtm-nav-controls">
                    \${GTM_NAVIGATION_CONFIG.getPreviousStep() ? \`
                        <button class="nav-btn nav-btn-prev" onclick="navigateToStep('\${GTM_NAVIGATION_CONFIG.getPreviousStep().id}', '\${GTM_NAVIGATION_CONFIG.getPreviousStep().url}')">
                            ← 上一步: \${GTM_NAVIGATION_CONFIG.getPreviousStep().name}
                        </button>
                    \` : '<div></div>'}

                    \${GTM_NAVIGATION_CONFIG.getNextStep() ? \`
                        <button class="nav-btn nav-btn-next" onclick="navigateToStep('\${GTM_NAVIGATION_CONFIG.getNextStep().id}', '\${GTM_NAVIGATION_CONFIG.getNextStep().url}')">
                            下一步: \${GTM_NAVIGATION_CONFIG.getNextStep().name} →
                        </button>
                    \` : '<div></div>'}
                </div>
            </div>
        </div>
    \`;

    return navigationHTML;
}

// 导航样式CSS
const GTM_NAVIGATION_CSS = \`
    .gtm-navigation {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        position: sticky;
        top: 0;
        z-index: 100;
    }

    .gtm-nav-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 20px;
    }

    .gtm-nav-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }

    .gtm-nav-header h2 {
        margin: 0;
        font-size: 24px;
        font-weight: bold;
    }

    .gtm-nav-progress {
        display: flex;
        align-items: center;
        gap: 15px;
    }

    .progress-text {
        font-weight: bold;
        font-size: 14px;
    }

    .progress-bar {
        width: 200px;
        height: 8px;
        background: rgba(255,255,255,0.3);
        border-radius: 4px;
        overflow: hidden;
    }

    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #52c41a, #73d13d);
        border-radius: 4px;
        transition: width 0.3s ease;
    }

    .gtm-nav-steps {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 15px;
        margin-bottom: 20px;
    }

    .gtm-nav-step {
        background: rgba(255,255,255,0.1);
        border-radius: 8px;
        padding: 15px;
        display: flex;
        align-items: center;
        gap: 15px;
        cursor: pointer;
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }

    .gtm-nav-step:hover {
        background: rgba(255,255,255,0.2);
        transform: translateY(-2px);
    }

    .gtm-nav-step.completed {
        background: rgba(82, 196, 26, 0.2);
        border-color: #52c41a;
    }

    .gtm-nav-step.current {
        background: rgba(24, 144, 255, 0.3);
        border-color: #1890ff;
        box-shadow: 0 0 20px rgba(24, 144, 255, 0.4);
    }

    .gtm-nav-step.pending {
        background: rgba(255,255,255,0.05);
        opacity: 0.7;
    }

    .step-number {
        background: rgba(255,255,255,0.2);
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 16px;
    }

    .gtm-nav-step.completed .step-number {
        background: #52c41a;
    }

    .gtm-nav-step.current .step-number {
        background: #1890ff;
    }

    .step-content {
        flex: 1;
    }

    .step-name {
        font-weight: bold;
        font-size: 16px;
        margin-bottom: 4px;
    }

    .step-description {
        font-size: 12px;
        opacity: 0.9;
        line-height: 1.4;
    }

    .step-status-icon {
        font-size: 18px;
    }

    .gtm-nav-controls {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 20px;
    }

    .nav-btn {
        padding: 12px 24px;
        border: none;
        border-radius: 6px;
        font-size: 14px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        min-width: 160px;
    }

    .nav-btn-prev {
        background: rgba(255,255,255,0.2);
        color: white;
        border: 2px solid rgba(255,255,255,0.3);
    }

    .nav-btn-prev:hover {
        background: rgba(255,255,255,0.3);
        transform: translateX(-5px);
    }

    .nav-btn-next {
        background: linear-gradient(135deg, #52c41a, #73d13d);
        color: white;
        border: 2px solid transparent;
    }

    .nav-btn-next:hover {
        background: linear-gradient(135deg, #389e0d, #52c41a);
        transform: translateX(5px);
    }

    @media (max-width: 768px) {
        .gtm-nav-header {
            flex-direction: column;
            gap: 15px;
            text-align: center;
        }

        .gtm-nav-steps {
            grid-template-columns: 1fr;
        }

        .gtm-nav-controls {
            flex-direction: column;
            gap: 10px;
        }

        .nav-btn {
            width: 100%;
        }
    }
\`;

// 导航跳转函数
function navigateToStep(stepId, url) {
    if (url && url !== '#') {
        window.location.href = url;
    } else {
        alert(\`"\${stepId}"页面正在开发中，敬请期待！\`);
    }
}

// 初始化导航的函数
function initGTMNavigation(currentStepId) {
    // 添加CSS样式
    const style = document.createElement('style');
    style.textContent = GTM_NAVIGATION_CSS;
    document.head.appendChild(style);

    // 创建导航HTML
    const navigationHTML = createGTMNavigation(currentStepId);

    // 将导航插入到body的开头
    document.body.insertAdjacentHTML('afterbegin', navigationHTML);
}