#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目配置文件
"""

import os
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent

# 数据目录配置
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EXPORTS_DIR = DATA_DIR / "exports"

# 报告目录配置
REPORTS_DIR = PROJECT_ROOT / "reports"
CHARTS_DIR = REPORTS_DIR / "charts"
SUMMARIES_DIR = REPORTS_DIR / "summaries"
PRESENTATIONS_DIR = REPORTS_DIR / "presentations"

# 脚本目录配置
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
ANALYSIS_DIR = SCRIPTS_DIR / "analysis"
VISUALIZATION_DIR = SCRIPTS_DIR / "visualization"
UTILS_DIR = SCRIPTS_DIR / "utils"

# 图表配置
CHART_CONFIG = {
    "figure_size": (14, 8),
    "dpi": 300,
    "font_family": ['SimHei', 'Arial Unicode MS', 'DejaVu Sans'],
    "colors": ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f'],
    "line_styles": ['-', '--', '-.', ':', '-', '--', '-.', ':'],
    "markers": ['o', 's', '^', 'D', 'v', 'p', '*', 'h'],
    "output_formats": ['png', 'pdf']
}

# 数据配置
DATA_CONFIG = {
    "months": ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
    "regions": ['华北区', '华南区', '华东区', '华西区', '华中区'],
    "business_lines": ['经营单元', '公开课', '商学课', '团队课', '方案班', '咨询内训']
}

# 分析配置
ANALYSIS_CONFIG = {
    "currency_unit": "万元",
    "decimal_places": 2,
    "enable_trend_analysis": True,
    "enable_comparison": True,
    "enable_prediction": False  # 待开发
}

# 确保目录存在
def ensure_directories():
    """确保所有必要的目录都存在"""
    directories = [
        RAW_DATA_DIR, PROCESSED_DATA_DIR, EXPORTS_DIR,
        CHARTS_DIR, SUMMARIES_DIR, PRESENTATIONS_DIR,
        ANALYSIS_DIR, VISUALIZATION_DIR, UTILS_DIR
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    ensure_directories()
    print("项目目录结构已创建完成！") 