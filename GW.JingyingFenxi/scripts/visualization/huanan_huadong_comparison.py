#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
华南华东区域对比图生成器
"""

import sys
from pathlib import Path
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib import rcParams

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent.parent.parent))
from config.settings import CHART_CONFIG, CHARTS_DIR

# 设置中文字体
rcParams['font.sans-serif'] = CHART_CONFIG['font_family']
rcParams['axes.unicode_minus'] = False

def create_huanan_huadong_comparison():
    """创建华南华东对比图"""
    
    # 华东区数据（需要您提供实际数据，这里使用示例数据）
    huadong_data = {
        '月份': ['1月', '2月', '3月', '4月', '5月', '6月'],
        '经营单元-华东区': [208.7, 218.0, 507.5, 597.9, 406.7, 313.9],
        '华东区（公开课）': [62.3, 110.0, 363.5, 232.6, 152.6, 185.2],
        '商学课': [23.1, 71.5, 224.5, 125.5, 72.8, 107.0],
        '团队课': [39.2, 38.5, 139.0, 87.5, 79.8, 78.2],
        '方案班': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        '华东区（咨询内训）': [146.4, 108.0, 144.0, 365.3, 254.1, 128.7]
    }
    
    # 华南区数据
    huanan_data = {
        '月份': ['1月', '2月', '3月', '4月', '5月', '6月'],
        '经营单元-华南区': [774.6, 329.7, 759.5, 795.7, 776.3, 791.4],
        '华南区（公开课）': [75.8, 122.6, 453.3, 224.8, 303.2, 244.3],
        '商学课': [26.5, 113.9, 269.2, 100.4, 167.0, 213.4],
        '团队课': [49.3, 0.0, 163.8, 124.5, 118.3, 31.0],
        '方案班': [0.0, 8.7, 20.3, 0.0, 18.0, 0.0],
        '华南区（咨询内训）': [698.8, 207.1, 306.2, 570.8, 473.1, 547.1]
    }
    
    # 创建华东区折线图
    create_region_chart(huadong_data, '华东区', 'huadong_revenue_chart')
    
    # 创建华南区折线图
    create_region_chart(huanan_data, '华南区', 'huanan_revenue_chart')
    
    # 创建对比图表
    create_comparison_chart(huadong_data, huanan_data)
    
    # 创建汇总表
    create_summary_table(huadong_data, huanan_data)

def create_region_chart(data, region_name, filename):
    """创建单个区域的营收折线图"""
    df = pd.DataFrame(data)
    
    # 创建图表
    plt.figure(figsize=CHART_CONFIG['figure_size'])
    
    # 绘制折线图
    colors = CHART_CONFIG['colors']
    line_styles = CHART_CONFIG['line_styles']
    markers = CHART_CONFIG['markers']
    
    for i, column in enumerate(df.columns[1:]):
        plt.plot(df['月份'], df[column], 
                color=colors[i % len(colors)], 
                linewidth=2.5,
                linestyle=line_styles[i % len(line_styles)],
                marker=markers[i % len(markers)],
                markersize=8,
                label=column,
                alpha=0.8)
    
    # 图表美化
    plt.title(f'2025年{region_name}部门营收趋势图', fontsize=18, fontweight='bold', pad=20)
    plt.xlabel('月份', fontsize=14, fontweight='bold')
    plt.ylabel('营收 (万元)', fontsize=14, fontweight='bold')
    
    # 设置网格
    plt.grid(True, alpha=0.3, linestyle='--')
    
    # 设置图例
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=11)
    
    # 设置y轴范围
    plt.ylim(0, max(df.iloc[:, 1:].max()) * 1.1)
    
    # 在每个数据点上显示数值
    for i, column in enumerate(df.columns[1:]):
        for j, value in enumerate(df[column]):
            if value > 0:  # 只显示非零值
                plt.annotate(f'{value}', 
                            (j, value), 
                            textcoords="offset points", 
                            xytext=(0,10), 
                            ha='center',
                            fontsize=9,
                            alpha=0.7)
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图表
    charts_dir = Path(CHARTS_DIR)
    charts_dir.mkdir(parents=True, exist_ok=True)
    
    plt.savefig(charts_dir / f'{filename}.png', dpi=CHART_CONFIG['dpi'], bbox_inches='tight')
    plt.savefig(charts_dir / f'{filename}.pdf', bbox_inches='tight')
    
    # 关闭图表以释放内存
    plt.close()
    
    print(f"{region_name}折线图已生成并保存为 '{filename}.png' 和 '{filename}.pdf'")

def create_comparison_chart(huadong_data, huanan_data):
    """创建华东区与华南区对比图表"""
    plt.figure(figsize=(16, 12))
    
    # 提取经营单元数据进行对比
    months = huadong_data['月份']
    huadong_total = huadong_data['经营单元-华东区']
    huanan_total = huanan_data['经营单元-华南区']
    
    # 创建对比图
    x = np.arange(len(months))
    width = 0.35
    
    # 第一个子图：柱状图对比
    plt.subplot(3, 1, 1)
    plt.bar(x - width/2, huadong_total, width, label='华东区', color='#1f77b4', alpha=0.8)
    plt.bar(x + width/2, huanan_total, width, label='华南区', color='#ff7f0e', alpha=0.8)
    
    plt.title('2025年华东区 vs 华南区营收对比（经营单元）', fontsize=16, fontweight='bold')
    plt.xlabel('月份', fontsize=12)
    plt.ylabel('营收 (万元)', fontsize=12)
    plt.xticks(x, months)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 添加数值标签
    for i, (hd, hn) in enumerate(zip(huadong_total, huanan_total)):
        plt.text(i - width/2, hd + 10, f'{hd}', ha='center', va='bottom', fontsize=10)
        plt.text(i + width/2, hn + 10, f'{hn}', ha='center', va='bottom', fontsize=10)
    
    # 第二个子图：折线图对比
    plt.subplot(3, 1, 2)
    plt.plot(months, huadong_total, marker='o', linewidth=2.5, markersize=8, label='华东区', color='#1f77b4')
    plt.plot(months, huanan_total, marker='s', linewidth=2.5, markersize=8, label='华南区', color='#ff7f0e')
    
    plt.title('2025年华东区 vs 华南区营收趋势对比', fontsize=16, fontweight='bold')
    plt.xlabel('月份', fontsize=12)
    plt.ylabel('营收 (万元)', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 添加数值标签
    for i, (month, hd, hn) in enumerate(zip(months, huadong_total, huanan_total)):
        plt.annotate(f'{hd}', (i, hd), textcoords="offset points", xytext=(0,10), ha='center', fontsize=9)
        plt.annotate(f'{hn}', (i, hn), textcoords="offset points", xytext=(0,10), ha='center', fontsize=9)
    
    # 第三个子图：业务线对比
    plt.subplot(3, 1, 3)
    
    # 计算各业务线总营收
    huadong_business = {
        '公开课': sum(huadong_data['华东区（公开课）']),
        '商学课': sum(huadong_data['商学课']),
        '团队课': sum(huadong_data['团队课']),
        '咨询内训': sum(huadong_data['华东区（咨询内训）'])
    }
    
    huanan_business = {
        '公开课': sum(huanan_data['华南区（公开课）']),
        '商学课': sum(huanan_data['商学课']),
        '团队课': sum(huanan_data['团队课']),
        '咨询内训': sum(huanan_data['华南区（咨询内训）'])
    }
    
    business_names = list(huadong_business.keys())
    huadong_values = list(huadong_business.values())
    huanan_values = list(huanan_business.values())
    
    x_business = np.arange(len(business_names))
    plt.bar(x_business - width/2, huadong_values, width, label='华东区', color='#1f77b4', alpha=0.8)
    plt.bar(x_business + width/2, huanan_values, width, label='华南区', color='#ff7f0e', alpha=0.8)
    
    plt.title('2025年华东区 vs 华南区各业务线营收对比（6个月总计）', fontsize=16, fontweight='bold')
    plt.xlabel('业务线', fontsize=12)
    plt.ylabel('营收 (万元)', fontsize=12)
    plt.xticks(x_business, business_names)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 添加数值标签
    for i, (hd, hn) in enumerate(zip(huadong_values, huanan_values)):
        plt.text(i - width/2, hd + 10, f'{hd:.1f}', ha='center', va='bottom', fontsize=10)
        plt.text(i + width/2, hn + 10, f'{hn:.1f}', ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    
    # 保存图表
    charts_dir = Path(CHARTS_DIR)
    charts_dir.mkdir(parents=True, exist_ok=True)
    
    plt.savefig(charts_dir / 'huadong_vs_huanan_comparison.png', dpi=CHART_CONFIG['dpi'], bbox_inches='tight')
    plt.savefig(charts_dir / 'huadong_vs_huanan_comparison.pdf', bbox_inches='tight')
    plt.close()
    
    print("华东区与华南区对比图已生成并保存为 'huadong_vs_huanan_comparison.png' 和 'huadong_vs_huanan_comparison.pdf'")

def create_summary_table(huadong_data, huanan_data):
    """创建营收汇总表"""
    
    # 创建华东区汇总表
    df_huadong = pd.DataFrame(huadong_data)
    df_huadong.loc['总计'] = df_huadong.sum(numeric_only=True)
    df_huadong.loc['平均值'] = df_huadong.iloc[:-1].mean(numeric_only=True)
    df_huadong.loc['总计', '月份'] = '总计'
    df_huadong.loc['平均值', '月份'] = '平均值'
    
    # 创建华南区汇总表
    df_huanan = pd.DataFrame(huanan_data)
    df_huanan.loc['总计'] = df_huanan.sum(numeric_only=True)
    df_huanan.loc['平均值'] = df_huanan.iloc[:-1].mean(numeric_only=True)
    df_huanan.loc['总计', '月份'] = '总计'
    df_huanan.loc['平均值', '月份'] = '平均值'
    
    # 保存为CSV文件
    from config.settings import EXPORTS_DIR
    exports_dir = Path(EXPORTS_DIR)
    exports_dir.mkdir(parents=True, exist_ok=True)
    
    df_huadong.to_csv(exports_dir / 'huadong_revenue_summary.csv', index=False, encoding='utf-8-sig')
    df_huanan.to_csv(exports_dir / 'huanan_revenue_summary.csv', index=False, encoding='utf-8-sig')
    
    print("\n华东区营收汇总表:")
    print(df_huadong.to_string(index=False))
    print("\n华南区营收汇总表:")
    print(df_huanan.to_string(index=False))
    print("\n汇总表已保存为 'huadong_revenue_summary.csv' 和 'huanan_revenue_summary.csv'")

if __name__ == "__main__":
    print("正在生成华南华东对比图...")
    create_huanan_huadong_comparison()
    print("华南华东对比图生成完成！") 