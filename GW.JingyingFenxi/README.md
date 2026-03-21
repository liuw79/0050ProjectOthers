# 经营分析项目 (GW.JingyingFenxi)

## 项目概述
本项目用于分析各区域营收数据和产品业绩，生成可视化图表和分析报告，支持多维度的业务数据分析。

## 目录结构

```
GW.JingyingFenxi/
├── README.md                   # 项目说明文档
├── progress.md                 # 项目进度记录
├── run_open_course_analysis.py # 公开课分析快速启动脚本
├── config/                     # 配置文件
│   ├── requirements.txt        # Python依赖包
│   └── settings.py            # 项目配置
├── data/                       # 数据文件
│   ├── raw/                   # 原始数据
│   ├── processed/             # 处理后的数据
│   └── exports/               # 导出的汇总数据
│       ├── huabei_revenue_summary.csv
│       ├── huanan_revenue_summary.csv
│       ├── huadong_revenue_summary.csv
│       ├── open_course_data.csv
│       ├── instructor_performance.csv
│       └── open_course_summary.json
├── scripts/                    # 脚本文件
│   ├── analysis/              # 数据分析脚本
│   │   ├── revenue_analyzer.py
│   │   └── open_course_analyzer.py
│   ├── visualization/         # 可视化脚本
│   │   ├── revenue_chart.py
│   │   ├── huanan_huadong_comparison.py
│   │   └── open_course_visualizer.py
│   └── utils/                 # 工具函数
│       └── data_loader.py
├── reports/                    # 报告输出
│   ├── charts/                # 图表文件
│   │   ├── huabei_revenue_chart.png
│   │   ├── huanan_revenue_chart.png
│   │   ├── huabei_vs_huanan_comparison.png
│   │   ├── huadong_vs_huanan_comparison.png
│   │   └── open_course_*.png (9个公开课分析图表)
│   ├── summaries/             # 分析摘要
│   │   ├── huanan_huadong_analysis.md
│   │   └── open_course_analysis_report.md
│   └── presentations/         # 演示文件
├── docs/                       # 文档
├── tests/                      # 测试文件
└── .gitignore                 # Git忽略文件
```

## 当前功能

### 📊 区域营收分析
- ✅ 华北区营收折线图生成
- ✅ 华南区营收折线图生成
- ✅ 华东区营收折线图生成
- ✅ 多区域营收对比分析
- ✅ 营收数据汇总表生成

### 📈 公开课产品分析
- ✅ 49门公开课全面分析
- ✅ 收入、利润、订单多维度分析
- ✅ 讲师表现深度分析
- ✅ 业绩排名和分布分析
- ✅ 相关性分析和趋势预测
- ✅ 9套专业图表生成
- ✅ 综合分析报告生成

## 规划中的功能
- 🔄 更多区域数据支持（华西、华中等）
- 🔄 时间维度分析（季度、年度、同比环比）
- 🔄 业务线深度分析
- 🔄 营收预测模型
- 🔄 自动化报告生成
- 🔄 数据源集成（Excel、数据库等）
- 🔄 商学课、团队课产品分析
- 🔄 讲师绩效管理系统

## 快速开始

### 1. 环境准备
```bash
pip install -r config/requirements.txt
```

### 2. 区域营收分析
```bash
python scripts/visualization/revenue_chart.py
```

### 3. 公开课产品分析
```bash
python run_open_course_analysis.py
```

### 4. 查看结果
- 图表文件：`reports/charts/`
- 数据汇总：`data/exports/`
- 分析报告：`reports/summaries/`

## 核心分析模块

### 公开课产品分析系统
**关键指标：**
- 总收入：2,931.1万元
- 总利润：1,334.7万元
- 平均利润率：45.5%
- 课程数量：49门
- 讲师数量：33人

**生成图表：**
1. TOP15课程分析
2. 收入分布分析
3. 利润分析
4. 讲师表现分析
5. 综合仪表板
6. 业绩排名图表
7. 业务指标分析
8. 相关性分析

### 区域营收分析系统
**支持区域：**
- 华北区、华南区、华东区
- 多区域对比分析
- 月度趋势分析

## 数据格式要求

### 营收数据格式
营收数据应包含以下字段：
- 月份
- 经营单元营收
- 公开课营收
- 商学课营收
- 团队课营收
- 方案班营收
- 咨询内训营收

### 公开课数据格式
公开课数据应包含以下字段：
- 序号、班级名称、讲师
- 订单数量、收入、收入排名、收入占比
- 项目利润、项目利润排名、项目利润占比
- 高维毛利、高维毛利排名、高维毛利占比

## 贡献指南
1. 所有数据文件放入`data/`目录
2. 分析脚本放入`scripts/analysis/`
3. 可视化脚本放入`scripts/visualization/`
4. 生成的报告放入`reports/`对应子目录
5. 更新`progress.md`记录重要变更

## 版本历史
- v1.0 (2025-01-09): 华北区和华南区营收折线图分析
- v1.1 (2025-01-09): 项目结构重构，添加配置管理
- v1.2 (2025-01-09): 华东区数据支持，华南华东对比分析
- v2.0 (2025-01-09): 公开课产品分析系统，49门课程全面分析 