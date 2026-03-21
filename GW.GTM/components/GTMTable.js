// GTM通用表格组件
class GTMTable {
    constructor(container, config, apiBase = 'http://localhost:3001/api') {
        this.container = container;
        this.config = config;
        this.apiBase = apiBase;
        this.projectId = null;
        this.currentSheetId = null;
        this.data = [];
        this.isModified = false;
        this.autoSaveTimer = null;

        this.init();
    }

    init() {
        this.createHTML();
        this.setupEventListeners();
        this.loadProjectInfo();
    }

    createHTML() {
        this.container.innerHTML = `
            <div class="gtm-table-container">
                <!-- 头部控制区 -->
                <div class="gtm-header">
                    <h1>${this.config.displayName}</h1>
                    <div class="gtm-logo">
                        <span class="logo-text">高维学堂</span>
                        <div class="logo-icon">®</div>
                    </div>
                </div>

                <!-- 控制面板 -->
                <div class="gtm-controls">
                    <div class="gtm-sheet-info">
                        <h3>项目：<span id="projectName">加载中...</span></h3>
                    </div>

                    <div class="gtm-form-controls">
                        <div class="gtm-input-group">
                            <label>表格名称：</label>
                            <input type="text" id="sheetName" placeholder="如：2024年Q3${this.config.displayName}">
                        </div>

                        <div class="gtm-input-group">
                            <label>统计周期：</label>
                            <input type="text" id="sheetPeriod" placeholder="如：2024年Q3">
                        </div>

                        <div class="gtm-action-buttons">
                            <button id="saveBtn" class="gtm-btn gtm-btn-primary">💾 保存</button>
                            <div class="gtm-secondary-buttons">
                                <button id="loadHistoryBtn" class="gtm-btn gtm-btn-info">📋 历史记录</button>
                                <button id="newSheetBtn" class="gtm-btn gtm-btn-success">✨ 新建</button>
                                <button id="addRowBtn" class="gtm-btn gtm-btn-secondary">➕ 添加行</button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 历史记录列表 -->
                <div id="historyList" class="gtm-history-list" style="display: none;">
                    <h4>历史记录</h4>
                    <div id="historyContainer"></div>
                </div>

                <!-- 表格区域 -->
                <div class="gtm-table-wrapper">
                    <table class="gtm-table">
                        <thead>
                            <tr>
                                ${this.config.columns.map(col =>
                                    `<th style="width: ${col.width || 'auto'}">${col.label}</th>`
                                ).join('')}
                            </tr>
                        </thead>
                        <tbody id="tableBody">
                            <!-- 动态生成行 -->
                        </tbody>
                    </table>
                </div>

                <!-- 浮动保存按钮 -->
                <div id="floatingSaveBtn" class="gtm-floating-save" style="display: none;">
                    <button class="gtm-btn gtm-btn-primary gtm-btn-round" title="快速保存">💾</button>
                </div>

                <!-- 消息提示区域 -->
                <div id="messageArea"></div>
            </div>
        `;

        this.loadCSS();
    }

    loadCSS() {
        const style = document.createElement('style');
        style.textContent = `
            .gtm-table-container {
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                font-family: "Microsoft YaHei", "PingFang SC", sans-serif;
            }

            .gtm-header {
                background: linear-gradient(135deg, #e8f4fd 0%, #f0f8ff 100%);
                padding: 20px 30px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 3px solid ${this.config.theme.headerColor};
            }

            .gtm-header h1 {
                color: ${this.config.theme.accentColor};
                font-size: 28px;
                font-weight: bold;
                margin: 0;
            }

            .gtm-logo {
                display: flex;
                align-items: center;
                gap: 10px;
            }

            .logo-text {
                color: ${this.config.theme.accentColor};
                font-size: 18px;
                font-weight: bold;
            }

            .logo-icon {
                width: 40px;
                height: 40px;
                background: ${this.config.theme.accentColor};
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-weight: bold;
            }

            .gtm-controls {
                padding: 20px 30px;
                background: #fafafa;
                border-bottom: 1px solid #e0e0e0;
            }

            .gtm-form-controls {
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                gap: 20px;
                flex-wrap: wrap;
            }

            .gtm-input-group {
                display: flex;
                align-items: center;
                gap: 10px;
            }

            .gtm-input-group label {
                font-weight: bold;
                color: #666;
                min-width: 80px;
            }

            .gtm-input-group input {
                padding: 10px 15px;
                border: 2px solid #e8e8e8;
                border-radius: 8px;
                min-width: 250px;
                font-size: 14px;
                transition: all 0.3s ease;
            }

            .gtm-input-group input:focus {
                border-color: ${this.config.theme.accentColor};
                box-shadow: 0 0 8px rgba(24, 144, 255, 0.2);
                outline: none;
            }

            .gtm-action-buttons {
                display: flex;
                flex-direction: column;
                gap: 15px;
                align-items: flex-end;
            }

            .gtm-secondary-buttons {
                display: flex;
                gap: 8px;
            }

            .gtm-btn {
                padding: 8px 16px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-size: 14px;
                font-weight: bold;
                transition: all 0.3s ease;
            }

            .gtm-btn-primary {
                background: linear-gradient(135deg, ${this.config.theme.accentColor} 0%, ${this.config.theme.successColor} 100%);
                color: white;
                font-size: 16px;
                padding: 12px 24px;
                box-shadow: 0 4px 15px rgba(24, 144, 255, 0.4);
            }

            .gtm-btn-primary:hover {
                transform: translateY(-1px);
                box-shadow: 0 6px 20px rgba(24, 144, 255, 0.6);
            }

            .gtm-btn-info {
                background: #13c2c2;
                color: white;
                font-size: 13px;
                padding: 6px 12px;
            }

            .gtm-btn-success {
                background: ${this.config.theme.successColor};
                color: white;
                font-size: 13px;
                padding: 6px 12px;
            }

            .gtm-btn-secondary {
                background: #d9d9d9;
                color: #666;
                font-size: 13px;
                padding: 6px 12px;
            }

            .gtm-table-wrapper {
                padding: 0;
            }

            .gtm-table {
                width: 100%;
                border-collapse: collapse;
                font-size: 14px;
            }

            .gtm-table thead {
                background: ${this.config.theme.headerColor};
                color: white;
            }

            .gtm-table th {
                padding: 15px 20px;
                text-align: center;
                font-weight: bold;
                font-size: 16px;
                border-right: 1px solid rgba(255,255,255,0.3);
            }

            .gtm-table th:last-child {
                border-right: none;
            }

            .gtm-table td {
                padding: 15px 20px;
                text-align: center;
                border-bottom: 1px solid #e0e0e0;
                border-right: 1px solid #e0e0e0;
                background: #fafafa;
            }

            .gtm-table td:last-child {
                border-right: none;
            }

            .gtm-table tbody tr:hover {
                background-color: #f8f9fa;
            }

            .gtm-table input {
                border: none;
                background: transparent;
                width: 100%;
                text-align: center;
                padding: 5px;
                font-size: 14px;
                color: #333;
            }

            .gtm-table input:focus {
                outline: 2px solid ${this.config.theme.accentColor};
                background: white;
                border-radius: 4px;
            }

            .gtm-table textarea {
                border: none;
                background: transparent;
                width: 100%;
                min-height: 40px;
                padding: 5px;
                font-size: 14px;
                color: #333;
                resize: vertical;
            }

            .gtm-floating-save {
                position: fixed;
                bottom: 30px;
                right: 30px;
                z-index: 1000;
            }

            .gtm-btn-round {
                width: 60px;
                height: 60px;
                border-radius: 50%;
                font-size: 20px;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 0;
            }

            .gtm-message {
                padding: 10px 15px;
                margin: 10px 30px;
                border-radius: 6px;
                font-weight: bold;
            }

            .gtm-message-success {
                background: #f6ffed;
                color: ${this.config.theme.successColor};
                border: 1px solid #b7eb8f;
            }

            .gtm-message-error {
                background: #fff2f0;
                color: ${this.config.theme.errorColor};
                border: 1px solid #ffccc7;
            }

            .gtm-message-info {
                background: #e6f7ff;
                color: ${this.config.theme.accentColor};
                border: 1px solid #91d5ff;
            }

            @media (max-width: 768px) {
                .gtm-header {
                    flex-direction: column;
                    gap: 15px;
                    text-align: center;
                }

                .gtm-form-controls {
                    flex-direction: column;
                    align-items: stretch;
                }

                .gtm-input-group {
                    flex-direction: column;
                    align-items: stretch;
                }

                .gtm-input-group input {
                    min-width: auto;
                    width: 100%;
                }
            }
        `;
        document.head.appendChild(style);
    }

    setupEventListeners() {
        // 保存按钮
        this.container.querySelector('#saveBtn').addEventListener('click', () => this.save());
        this.container.querySelector('#floatingSaveBtn button').addEventListener('click', () => this.save());

        // 其他按钮
        this.container.querySelector('#loadHistoryBtn').addEventListener('click', () => this.loadHistory());
        this.container.querySelector('#newSheetBtn').addEventListener('click', () => this.newSheet());
        this.container.querySelector('#addRowBtn').addEventListener('click', () => this.addRow());

        // 输入变化监听
        this.container.addEventListener('input', (e) => {
            if (e.target.matches('input, textarea')) {
                this.onDataChange();
                this.handleAutoCalc(e.target);
            }
        });

        // 滚动监听（浮动按钮）
        window.addEventListener('scroll', () => this.updateFloatingButton());
    }

    // 其他方法将在下一部分实现...
    showMessage(text, type = 'info') {
        const messageArea = this.container.querySelector('#messageArea');
        const message = document.createElement('div');
        message.className = `gtm-message gtm-message-${type}`;
        message.textContent = text;

        messageArea.appendChild(message);

        setTimeout(() => {
            if (message.parentNode) {
                message.parentNode.removeChild(message);
            }
        }, 3000);
    }

    addRow() {
        const tbody = this.container.querySelector('#tableBody');
        const row = document.createElement('tr');

        row.innerHTML = this.config.columns.map(col => {
            if (col.type === 'textarea') {
                return `<td><textarea placeholder="${col.placeholder || ''}"></textarea></td>`;
            } else {
                return `<td><input type="text" placeholder="${col.placeholder || ''}"></td>`;
            }
        }).join('');

        tbody.appendChild(row);
    }

    // 初始化默认行
    initializeRows() {
        for (let i = 0; i < this.config.settings.defaultRows; i++) {
            this.addRow();
        }
    }

    onDataChange() {
        this.isModified = true;
        this.updateFloatingButton();

        if (this.config.settings.autoSave) {
            this.scheduleAutoSave();
        }
    }

    scheduleAutoSave() {
        clearTimeout(this.autoSaveTimer);
        this.autoSaveTimer = setTimeout(() => {
            if (this.isModified && this.currentSheetId) {
                this.autoSave();
            }
        }, this.config.settings.autoSaveDelay);
    }

    updateFloatingButton() {
        const floatingBtn = this.container.querySelector('#floatingSaveBtn');
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

        if (scrollTop > 200 || this.isModified) {
            floatingBtn.style.display = 'block';
        } else {
            floatingBtn.style.display = 'none';
        }
    }

    handleAutoCalc(input) {
        const row = input.closest('tr');
        if (!row) return;

        // 找到需要自动计算的列
        this.config.columns.forEach((col, index) => {
            if (col.autoCalc && col.formula) {
                const cell = row.cells[index];
                const targetInput = cell.querySelector('input, textarea');
                if (targetInput) {
                    const rowData = this.getRowData(row);
                    const result = col.formula(rowData);
                    if (result) {
                        targetInput.value = result;
                    }
                }
            }
        });
    }

    getRowData(row) {
        const data = {};
        this.config.columns.forEach((col, index) => {
            const cell = row.cells[index];
            const input = cell.querySelector('input, textarea');
            if (input) {
                data[col.key] = input.value;
            }
        });
        return data;
    }

    // API相关方法需要后续实现
    async loadProjectInfo() {
        // 实现项目信息加载
        this.container.querySelector('#projectName').textContent = '测试GTM项目';
        this.projectId = 6; // 临时硬编码

        // 初始化表格
        this.initializeRows();
    }

    async save() {
        this.showMessage('保存功能待实现', 'info');
    }

    async loadHistory() {
        this.showMessage('历史记录功能待实现', 'info');
    }

    newSheet() {
        this.currentSheetId = null;
        this.container.querySelector('#sheetName').value = '';
        this.container.querySelector('#sheetPeriod').value = '';
        this.container.querySelector('#tableBody').innerHTML = '';
        this.initializeRows();
        this.isModified = false;
        this.updateFloatingButton();
    }

    async autoSave() {
        // 实现自动保存逻辑
        console.log('自动保存...');
    }
}