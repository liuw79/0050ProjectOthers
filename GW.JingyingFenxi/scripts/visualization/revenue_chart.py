#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
营收数据折线图生成器
"""

import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib import rcParams

# 设置中文字体
rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
rcParams['axes.unicode_minus'] = False

def create_revenue_chart():
    """创建营收折线图"""
    
    # 华北区数据（从第一张图）
    huabei_data = {
        '月份': ['1月', '2月', '3月', '4月', '5月', '6月'],
        '经营单元-华北区': [13.5, 25.6, 40.8, 90.7, 23.6, 37.7],
        '华北区（公开课）': [0.0, 0.0, 19.9, 58.9, 13.2, 19.7],
        '商学课': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        '团队课': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        '方案班': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        '华北区（咨询内训）': [13.5, 25.6, 20.9, 31.8, 10.4, 18.0]
    }
    
    # 华南区数据（从第二张图）
    huanan_data = {
        '月份': ['1月', '2月', '3月', '4月', '5月', '6月'],
        '经营单元-华南区': [774.6, 329.7, 759.5, 795.7, 776.3, 791.4],
        '华南区（公开课）': [75.8, 122.6, 453.3, 224.8, 303.2, 244.3],
        '商学课': [26.5, 113.9, 269.2, 100.4, 167.0, 213.4],
        '团队课': [49.3, 0.0, 163.8, 124.5, 118.3, 31.0],
        '方案班': [0.0, 8.7, 20.3, 0.0, 18.0, 0.0],
        '华南区（咨询内训）': [698.8, 207.1, 306.2, 570.8, 473.1, 547.1]
    }
    
    # 创建华北区图表
    create_region_chart(huabei_data, '华北区', 'huabei_revenue_chart')
    
    # 创建华南区图表
    create_region_chart(huanan_data, '华南区', 'huanan_revenue_chart')
    
    # 创建对比图表
    create_comparison_chart(huabei_data, huanan_data)

def create_region_chart(data, region_name, filename):
    """创建单个区域的营收折线图"""
    df = pd.DataFrame(data)
    
    # 创建图表
    plt.figure(figsize=(14, 8))
    
    # 绘制折线图
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']
    line_styles = ['-', '--', '-.', ':', '-', '--', '-.', ':']
    markers = ['o', 's', '^', 'D', 'v', 'p', '*', 'h']
    
    for i, column in enumerate(df.columns[1:]):
        plt.plot(df['月份'], df[column], 
                color=colors[i], 
                linewidth=2.5,
                linestyle=line_styles[i],
                marker=markers[i],
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
    plt.savefig(f'{filename}.png', dpi=300, bbox_inches='tight')
    plt.savefig(f'{filename}.pdf', bbox_inches='tight')
    
    # 关闭图表以释放内存
    plt.close()
    
    print(f"{region_name}折线图已生成并保存为 '{filename}.png' 和 '{filename}.pdf'")

def create_comparison_chart(huabei_data, huanan_data):
    """创建华北区与华南区对比图表"""
    plt.figure(figsize=(16, 10))
    
    # 提取经营单元数据进行对比
    months = huabei_data['月份']
    huabei_total = huabei_data['经营单元-华北区']
    huanan_total = huanan_data['经营单元-华南区']
    
    # 创建对比图
    x = np.arange(len(months))
    width = 0.35
    
    plt.subplot(2, 1, 1)
    plt.bar(x - width/2, huabei_total, width, label='华北区', color='#1f77b4', alpha=0.8)
    plt.bar(x + width/2, huanan_total, width, label='华南区', color='#ff7f0e', alpha=0.8)
    
    plt.title('2025年华北区 vs 华南区营收对比（经营单元）', fontsize=16, fontweight='bold')
    plt.xlabel('月份', fontsize=12)
    plt.ylabel('营收 (万元)', fontsize=12)
    plt.xticks(x, months)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 添加数值标签
    for i, (hb, hn) in enumerate(zip(huabei_total, huanan_total)):
        plt.text(i - width/2, hb + 10, f'{hb}', ha='center', va='bottom', fontsize=10)
        plt.text(i + width/2, hn + 10, f'{hn}', ha='center', va='bottom', fontsize=10)
    
    # 创建折线对比图
    plt.subplot(2, 1, 2)
    plt.plot(months, huabei_total, marker='o', linewidth=2.5, markersize=8, label='华北区', color='#1f77b4')
    plt.plot(months, huanan_total, marker='s', linewidth=2.5, markersize=8, label='华南区', color='#ff7f0e')
    
    plt.title('2025年华北区 vs 华南区营收趋势对比', fontsize=16, fontweight='bold')
    plt.xlabel('月份', fontsize=12)
    plt.ylabel('营收 (万元)', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 添加数值标签
    for i, (month, hb, hn) in enumerate(zip(months, huabei_total, huanan_total)):
        plt.annotate(f'{hb}', (i, hb), textcoords="offset points", xytext=(0,10), ha='center', fontsize=9)
        plt.annotate(f'{hn}', (i, hn), textcoords="offset points", xytext=(0,10), ha='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('huabei_vs_huanan_comparison.png', dpi=300, bbox_inches='tight')
    plt.savefig('huabei_vs_huanan_comparison.pdf', bbox_inches='tight')
    plt.close()
    
    print("华北区与华南区对比图已生成并保存为 'huabei_vs_huanan_comparison.png' 和 'huabei_vs_huanan_comparison.pdf'")

def create_summary_table():
    """创建营收汇总表"""
    # 华北区数据
    huabei_data = {
        '月份': ['1月', '2月', '3月', '4月', '5月', '6月'],
        '经营单元-华北区': [13.5, 25.6, 40.8, 90.7, 23.6, 37.7],
        '华北区（公开课）': [0.0, 0.0, 19.9, 58.9, 13.2, 19.7],
        '商学课': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        '团队课': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        '方案班': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        '华北区（咨询内训）': [13.5, 25.6, 20.9, 31.8, 10.4, 18.0]
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
    
    # 创建华北区汇总表
    df_huabei = pd.DataFrame(huabei_data)
    df_huabei.loc['总计'] = df_huabei.sum(numeric_only=True)
    df_huabei.loc['平均值'] = df_huabei.iloc[:-1].mean(numeric_only=True)
    df_huabei.loc['总计', '月份'] = '总计'
    df_huabei.loc['平均值', '月份'] = '平均值'
    
    # 创建华南区汇总表
    df_huanan = pd.DataFrame(huanan_data)
    df_huanan.loc['总计'] = df_huanan.sum(numeric_only=True)
    df_huanan.loc['平均值'] = df_huanan.iloc[:-1].mean(numeric_only=True)
    df_huanan.loc['总计', '月份'] = '总计'
    df_huanan.loc['平均值', '月份'] = '平均值'
    
    # 保存为CSV文件
    df_huabei.to_csv('huabei_revenue_summary.csv', index=False, encoding='utf-8-sig')
    df_huanan.to_csv('huanan_revenue_summary.csv', index=False, encoding='utf-8-sig')
    
    print("\n华北区营收汇总表:")
    print(df_huabei.to_string(index=False))
    print("\n华南区营收汇总表:")
    print(df_huanan.to_string(index=False))
    print("\n汇总表已保存为 'huabei_revenue_summary.csv' 和 'huanan_revenue_summary.csv'")

if __name__ == "__main__":
    print("正在生成营收折线图...")
    create_revenue_chart()
    create_summary_table() 