#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
公开课产品可视化工具
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rcParams

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent.parent.parent))
from config.settings import CHART_CONFIG, CHARTS_DIR, EXPORTS_DIR

# 设置中文字体和样式
rcParams['font.sans-serif'] = CHART_CONFIG['font_family']
rcParams['axes.unicode_minus'] = False

def create_open_course_charts():
    """创建公开课产品图表"""
    
    # 加载数据
    from scripts.analysis.open_course_analyzer import load_open_course_data
    df = load_open_course_data()
    
    # 创建各类图表
    create_performance_ranking_chart(df)
    create_business_metrics_chart(df)
    create_instructor_analysis_chart(df)
    create_correlation_analysis_chart(df)
    
    print("公开课可视化图表生成完成！")

def create_performance_ranking_chart(df):
    """创建业绩排名图表"""
    
    fig, axes = plt.subplots(2, 2, figsize=(20, 16))
    
    # 收入排名TOP20
    top_20_revenue = df.head(20)
    ax1 = axes[0, 0]
    bars1 = ax1.barh(range(len(top_20_revenue)), top_20_revenue['收入'], 
                     color=plt.cm.viridis(np.linspace(0, 1, len(top_20_revenue))))
    ax1.set_yticks(range(len(top_20_revenue)))
    ax1.set_yticklabels([name[:15] + '...' if len(name) > 15 else name for name in top_20_revenue['班级名称']], 
                       fontsize=9)
    ax1.set_xlabel('收入 (万元)', fontsize=12)
    ax1.set_title('收入排名TOP20', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # 添加数值标签
    for i, v in enumerate(top_20_revenue['收入']):
        ax1.text(v + 2, i, f'{v}万', va='center', fontsize=8)
    
    # 利润排名TOP20
    top_20_profit = df.sort_values('项目利润', ascending=False).head(20)
    ax2 = axes[0, 1]
    bars2 = ax2.barh(range(len(top_20_profit)), top_20_profit['项目利润'], 
                     color=plt.cm.plasma(np.linspace(0, 1, len(top_20_profit))))
    ax2.set_yticks(range(len(top_20_profit)))
    ax2.set_yticklabels([name[:15] + '...' if len(name) > 15 else name for name in top_20_profit['班级名称']], 
                       fontsize=9)
    ax2.set_xlabel('项目利润 (万元)', fontsize=12)
    ax2.set_title('利润排名TOP20', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    # 添加数值标签
    for i, v in enumerate(top_20_profit['项目利润']):
        ax2.text(v + 1, i, f'{v}万', va='center', fontsize=8)
    
    # 订单数量排名TOP20
    top_20_orders = df.sort_values('订单数量', ascending=False).head(20)
    ax3 = axes[1, 0]
    bars3 = ax3.barh(range(len(top_20_orders)), top_20_orders['订单数量'], 
                     color=plt.cm.coolwarm(np.linspace(0, 1, len(top_20_orders))))
    ax3.set_yticks(range(len(top_20_orders)))
    ax3.set_yticklabels([name[:15] + '...' if len(name) > 15 else name for name in top_20_orders['班级名称']], 
                       fontsize=9)
    ax3.set_xlabel('订单数量', fontsize=12)
    ax3.set_title('订单数量排名TOP20', fontsize=14, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    
    # 添加数值标签
    for i, v in enumerate(top_20_orders['订单数量']):
        ax3.text(v + 10, i, f'{v}单', va='center', fontsize=8)
    
    # 利润率排名TOP20
    df['利润率'] = df['项目利润'] / df['收入'] * 100
    top_20_rate = df.sort_values('利润率', ascending=False).head(20)
    ax4 = axes[1, 1]
    bars4 = ax4.barh(range(len(top_20_rate)), top_20_rate['利润率'], 
                     color=plt.cm.spring(np.linspace(0, 1, len(top_20_rate))))
    ax4.set_yticks(range(len(top_20_rate)))
    ax4.set_yticklabels([name[:15] + '...' if len(name) > 15 else name for name in top_20_rate['班级名称']], 
                       fontsize=9)
    ax4.set_xlabel('利润率 (%)', fontsize=12)
    ax4.set_title('利润率排名TOP20', fontsize=14, fontweight='bold')
    ax4.grid(True, alpha=0.3)
    
    # 添加数值标签
    for i, v in enumerate(top_20_rate['利润率']):
        ax4.text(v + 1, i, f'{v:.1f}%', va='center', fontsize=8)
    
    plt.tight_layout()
    
    # 保存图表
    charts_dir = Path(CHARTS_DIR)
    charts_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(charts_dir / 'open_course_performance_ranking.png', dpi=300, bbox_inches='tight')
    plt.savefig(charts_dir / 'open_course_performance_ranking.pdf', bbox_inches='tight')
    plt.close()
    
    print("业绩排名图表已生成")

def create_business_metrics_chart(df):
    """创建业务指标分析图表"""
    
    fig, axes = plt.subplots(2, 3, figsize=(24, 16))
    
    # 收入分布箱线图
    ax1 = axes[0, 0]
    ax1.boxplot(df['收入'], patch_artist=True, 
                boxprops=dict(facecolor='lightblue', alpha=0.7))
    ax1.set_ylabel('收入 (万元)', fontsize=12)
    ax1.set_title('收入分布箱线图', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # 利润分布箱线图
    ax2 = axes[0, 1]
    ax2.boxplot(df['项目利润'], patch_artist=True, 
                boxprops=dict(facecolor='lightgreen', alpha=0.7))
    ax2.set_ylabel('项目利润 (万元)', fontsize=12)
    ax2.set_title('利润分布箱线图', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    # 订单数量分布箱线图
    ax3 = axes[0, 2]
    ax3.boxplot(df['订单数量'], patch_artist=True, 
                boxprops=dict(facecolor='lightcoral', alpha=0.7))
    ax3.set_ylabel('订单数量', fontsize=12)
    ax3.set_title('订单数量分布箱线图', fontsize=14, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    
    # 收入区间分布
    ax4 = axes[1, 0]
    revenue_ranges = ['<20万', '20-50万', '50-100万', '100-150万', '>150万']
    revenue_counts = [
        len(df[df['收入'] < 20]),
        len(df[(df['收入'] >= 20) & (df['收入'] < 50)]),
        len(df[(df['收入'] >= 50) & (df['收入'] < 100)]),
        len(df[(df['收入'] >= 100) & (df['收入'] < 150)]),
        len(df[df['收入'] >= 150])
    ]
    
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc']
    bars = ax4.bar(revenue_ranges, revenue_counts, color=colors, alpha=0.8)
    ax4.set_xlabel('收入区间', fontsize=12)
    ax4.set_ylabel('课程数量', fontsize=12)
    ax4.set_title('收入区间分布', fontsize=14, fontweight='bold')
    ax4.grid(True, alpha=0.3)
    
    # 添加数值标签
    for bar, count in zip(bars, revenue_counts):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{count}', ha='center', va='bottom', fontsize=10)
    
    # 利润区间分布
    ax5 = axes[1, 1]
    profit_ranges = ['<10万', '10-30万', '30-60万', '60-90万', '>90万']
    profit_counts = [
        len(df[df['项目利润'] < 10]),
        len(df[(df['项目利润'] >= 10) & (df['项目利润'] < 30)]),
        len(df[(df['项目利润'] >= 30) & (df['项目利润'] < 60)]),
        len(df[(df['项目利润'] >= 60) & (df['项目利润'] < 90)]),
        len(df[df['项目利润'] >= 90])
    ]
    
    bars = ax5.bar(profit_ranges, profit_counts, color=colors, alpha=0.8)
    ax5.set_xlabel('利润区间', fontsize=12)
    ax5.set_ylabel('课程数量', fontsize=12)
    ax5.set_title('利润区间分布', fontsize=14, fontweight='bold')
    ax5.grid(True, alpha=0.3)
    
    # 添加数值标签
    for bar, count in zip(bars, profit_counts):
        height = bar.get_height()
        ax5.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{count}', ha='center', va='bottom', fontsize=10)
    
    # 订单数量区间分布
    ax6 = axes[1, 2]
    order_ranges = ['<50单', '50-100单', '100-200单', '200-300单', '>300单']
    order_counts = [
        len(df[df['订单数量'] < 50]),
        len(df[(df['订单数量'] >= 50) & (df['订单数量'] < 100)]),
        len(df[(df['订单数量'] >= 100) & (df['订单数量'] < 200)]),
        len(df[(df['订单数量'] >= 200) & (df['订单数量'] < 300)]),
        len(df[df['订单数量'] >= 300])
    ]
    
    bars = ax6.bar(order_ranges, order_counts, color=colors, alpha=0.8)
    ax6.set_xlabel('订单数量区间', fontsize=12)
    ax6.set_ylabel('课程数量', fontsize=12)
    ax6.set_title('订单数量区间分布', fontsize=14, fontweight='bold')
    ax6.grid(True, alpha=0.3)
    
    # 添加数值标签
    for bar, count in zip(bars, order_counts):
        height = bar.get_height()
        ax6.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{count}', ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    
    # 保存图表
    charts_dir = Path(CHARTS_DIR)
    plt.savefig(charts_dir / 'open_course_business_metrics.png', dpi=300, bbox_inches='tight')
    plt.savefig(charts_dir / 'open_course_business_metrics.pdf', bbox_inches='tight')
    plt.close()
    
    print("业务指标分析图表已生成")

def create_instructor_analysis_chart(df):
    """创建讲师分析图表"""
    
    # 按讲师汇总数据
    instructor_stats = df.groupby('讲师').agg({
        '收入': 'sum',
        '项目利润': 'sum',
        '订单数量': 'sum',
        '班级名称': 'count'
    }).rename(columns={'班级名称': '课程数量'})
    
    instructor_stats['平均课程收入'] = instructor_stats['收入'] / instructor_stats['课程数量']
    instructor_stats['平均课程利润'] = instructor_stats['项目利润'] / instructor_stats['课程数量']
    
    fig, axes = plt.subplots(2, 2, figsize=(20, 16))
    
    # 讲师收入排名
    top_instructors = instructor_stats.sort_values('收入', ascending=False).head(15)
    ax1 = axes[0, 0]
    bars1 = ax1.barh(range(len(top_instructors)), top_instructors['收入'], 
                     color=plt.cm.tab20(np.linspace(0, 1, len(top_instructors))))
    ax1.set_yticks(range(len(top_instructors)))
    ax1.set_yticklabels(top_instructors.index, fontsize=10)
    ax1.set_xlabel('总收入 (万元)', fontsize=12)
    ax1.set_title('讲师收入排名TOP15', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # 添加数值标签
    for i, v in enumerate(top_instructors['收入']):
        ax1.text(v + 2, i, f'{v:.1f}万', va='center', fontsize=9)
    
    # 讲师平均课程收入
    avg_revenue = instructor_stats.sort_values('平均课程收入', ascending=False).head(15)
    ax2 = axes[0, 1]
    bars2 = ax2.barh(range(len(avg_revenue)), avg_revenue['平均课程收入'], 
                     color=plt.cm.Set3(np.linspace(0, 1, len(avg_revenue))))
    ax2.set_yticks(range(len(avg_revenue)))
    ax2.set_yticklabels(avg_revenue.index, fontsize=10)
    ax2.set_xlabel('平均课程收入 (万元)', fontsize=12)
    ax2.set_title('讲师平均课程收入TOP15', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    # 添加数值标签
    for i, v in enumerate(avg_revenue['平均课程收入']):
        ax2.text(v + 2, i, f'{v:.1f}万', va='center', fontsize=9)
    
    # 讲师课程数量分布
    ax3 = axes[1, 0]
    course_counts = instructor_stats['课程数量'].value_counts().sort_index()
    bars3 = ax3.bar(course_counts.index, course_counts.values, 
                    color='skyblue', alpha=0.8, edgecolor='navy')
    ax3.set_xlabel('课程数量', fontsize=12)
    ax3.set_ylabel('讲师人数', fontsize=12)
    ax3.set_title('讲师课程数量分布', fontsize=14, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    
    # 添加数值标签
    for bar, count in zip(bars3, course_counts.values):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{count}人', ha='center', va='bottom', fontsize=10)
    
    # 讲师收入 vs 课程数量散点图
    ax4 = axes[1, 1]
    scatter = ax4.scatter(instructor_stats['课程数量'], instructor_stats['收入'], 
                         s=100, alpha=0.6, c=instructor_stats['平均课程收入'], 
                         cmap='viridis')
    ax4.set_xlabel('课程数量', fontsize=12)
    ax4.set_ylabel('总收入 (万元)', fontsize=12)
    ax4.set_title('讲师收入 vs 课程数量关系', fontsize=14, fontweight='bold')
    ax4.grid(True, alpha=0.3)
    
    # 添加颜色条
    cbar = plt.colorbar(scatter, ax=ax4)
    cbar.set_label('平均课程收入 (万元)', fontsize=10)
    
    # 标注特殊点
    for idx, row in instructor_stats.iterrows():
        if row['收入'] > 100 or row['课程数量'] > 1:
            ax4.annotate(idx, (row['课程数量'], row['收入']), 
                        xytext=(5, 5), textcoords='offset points', fontsize=8)
    
    plt.tight_layout()
    
    # 保存图表
    charts_dir = Path(CHARTS_DIR)
    plt.savefig(charts_dir / 'open_course_instructor_analysis.png', dpi=300, bbox_inches='tight')
    plt.savefig(charts_dir / 'open_course_instructor_analysis.pdf', bbox_inches='tight')
    plt.close()
    
    print("讲师分析图表已生成")

def create_correlation_analysis_chart(df):
    """创建相关性分析图表"""
    
    # 准备数值数据
    numeric_cols = ['订单数量', '收入', '项目利润', '高维毛利']
    df_numeric = df[numeric_cols].copy()
    df_numeric['利润率'] = df['项目利润'] / df['收入'] * 100
    
    fig, axes = plt.subplots(2, 2, figsize=(20, 16))
    
    # 相关系数热力图
    ax1 = axes[0, 0]
    corr_matrix = df_numeric.corr()
    im = ax1.imshow(corr_matrix, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
    ax1.set_xticks(range(len(corr_matrix.columns)))
    ax1.set_yticks(range(len(corr_matrix.columns)))
    ax1.set_xticklabels(corr_matrix.columns, rotation=45, ha='right')
    ax1.set_yticklabels(corr_matrix.columns)
    ax1.set_title('指标相关性热力图', fontsize=14, fontweight='bold')
    
    # 添加相关系数数值
    for i in range(len(corr_matrix.columns)):
        for j in range(len(corr_matrix.columns)):
            text = ax1.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                           ha="center", va="center", color="black", fontsize=10)
    
    # 添加颜色条
    cbar = plt.colorbar(im, ax=ax1)
    cbar.set_label('相关系数', fontsize=10)
    
    # 订单数量 vs 收入散点图
    ax2 = axes[0, 1]
    ax2.scatter(df['订单数量'], df['收入'], alpha=0.6, s=60, color='blue')
    ax2.set_xlabel('订单数量', fontsize=12)
    ax2.set_ylabel('收入 (万元)', fontsize=12)
    ax2.set_title('订单数量 vs 收入关系', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    # 添加趋势线
    z = np.polyfit(df['订单数量'], df['收入'], 1)
    p = np.poly1d(z)
    ax2.plot(df['订单数量'], p(df['订单数量']), "r--", alpha=0.8, linewidth=2)
    
    # 添加相关系数
    corr_coef = df['订单数量'].corr(df['收入'])
    ax2.text(0.05, 0.95, f'相关系数: {corr_coef:.3f}', transform=ax2.transAxes,
             bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))
    
    # 收入 vs 利润散点图
    ax3 = axes[1, 0]
    ax3.scatter(df['收入'], df['项目利润'], alpha=0.6, s=60, color='green')
    ax3.set_xlabel('收入 (万元)', fontsize=12)
    ax3.set_ylabel('项目利润 (万元)', fontsize=12)
    ax3.set_title('收入 vs 利润关系', fontsize=14, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    
    # 添加趋势线
    z = np.polyfit(df['收入'], df['项目利润'], 1)
    p = np.poly1d(z)
    ax3.plot(df['收入'], p(df['收入']), "r--", alpha=0.8, linewidth=2)
    
    # 添加相关系数
    corr_coef = df['收入'].corr(df['项目利润'])
    ax3.text(0.05, 0.95, f'相关系数: {corr_coef:.3f}', transform=ax3.transAxes,
             bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))
    
    # 利润率分布直方图
    ax4 = axes[1, 1]
    df['利润率'] = df['项目利润'] / df['收入'] * 100
    n, bins, patches = ax4.hist(df['利润率'], bins=20, alpha=0.7, edgecolor='black')
    
    # 根据利润率给直方图着色
    for i, p in enumerate(patches):
        if bins[i] < 40:
            p.set_facecolor('red')
        elif bins[i] < 60:
            p.set_facecolor('orange')
        else:
            p.set_facecolor('green')
    
    ax4.set_xlabel('利润率 (%)', fontsize=12)
    ax4.set_ylabel('课程数量', fontsize=12)
    ax4.set_title('利润率分布', fontsize=14, fontweight='bold')
    ax4.grid(True, alpha=0.3)
    
    # 添加统计信息
    mean_rate = df['利润率'].mean()
    median_rate = df['利润率'].median()
    ax4.axvline(mean_rate, color='red', linestyle='--', linewidth=2, label=f'平均值: {mean_rate:.1f}%')
    ax4.axvline(median_rate, color='blue', linestyle='--', linewidth=2, label=f'中位数: {median_rate:.1f}%')
    ax4.legend()
    
    plt.tight_layout()
    
    # 保存图表
    charts_dir = Path(CHARTS_DIR)
    plt.savefig(charts_dir / 'open_course_correlation_analysis.png', dpi=300, bbox_inches='tight')
    plt.savefig(charts_dir / 'open_course_correlation_analysis.pdf', bbox_inches='tight')
    plt.close()
    
    print("相关性分析图表已生成")

if __name__ == "__main__":
    print("开始生成公开课可视化图表...")
    create_open_course_charts()
    print("公开课可视化图表生成完成！") 