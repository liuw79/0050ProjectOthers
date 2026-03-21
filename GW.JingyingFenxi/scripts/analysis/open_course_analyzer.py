#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
公开课产品分析器
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

# 设置中文字体
rcParams['font.sans-serif'] = CHART_CONFIG['font_family']
rcParams['axes.unicode_minus'] = False

def load_open_course_data():
    """加载公开课数据"""
    data = {
        '序号': list(range(1, 50)),
        '班级名称': [
            '月度经营分析会', 'OGSM业务规划与执行', '升级定位与品牌战略', '流程型组织', '供应链管理',
            '人人都是自己的CEO', '极简项目管理', '跨境爆品打造', '产品供应链全链条', '教练式领导力',
            '科学分线', '超级面试官', '增长与印刷打造', '品牌体验设计', '卓越经营者',
            '1号找人官', '产品开发管理IPD', '需求预测管理&库存管控', '打造竞争领先型餐饮供应链', '战略级项目管理',
            '业务领先战略', 'AI时代的企业进化', '财务BP能力提升', '组织设计总纲课', 'AI5用户产品经理实战',
            '战略设计总纲课', 'B2B渠道销售', '做实企业文化', '超级UI设计流程再造', '餐饮私域会员增长实战课',
            '品牌授权策略', '高复购产品定位与采单体系', '超级转化率', '餐饮线上营销与爆品打造', 'B2B销售业绩管理',
            '超级数据分析', '科学分线（无饮版）', '外卖盈利模型重塑（连锁企业）', '餐饮人IP打造', '产品供应链全链条',
            '创始人财务进阶', '做对股权激励', '科学调优单店模型', 'AI驱动业务增效', '创始人的极简法律课',
            '餐饮股权动态合伙制', '跨境供应链提效降本', 'OGSM战略解码', '全面预算管理2.0'
        ],
        '讲师': [
            '祝鹏程', '高旭', '冯卫东', '蒋伟良', '高上',
            '王潇航', '郭嘉', '张雷', '张晓', '李益祥',
            '下志汉', '曾川盛', '汤君权', '王志谦', '祝鹏程',
            '刘攸锋', '汤君权', '高上', '赵传书', '郭嘉',
            '高旭', '董俊豪', '徐薇', '蒋伟良', '高上',
            '刘绍荣', '崔建中', '欧德张', '高旭', '郭君鹏',
            '陈陶琦', '北比', '郭嘉', '李宜倍', '崔建中',
            '陈雨点', '下志汉', '刘晴', '柴园', '张晓',
            '徐薇', '罗毅', '赵建光', '高旭', '范杏',
            '刘振宇', '高上', '高旭', '何绍茂'
        ],
        '订单数量': [
            770, 412, 172, 356, 244, 251, 262, 229, 196, 220,
            234, 270, 171, 187, 179, 239, 143, 108, 115, 100,
            119, 107, 108, 113, 88, 184, 73, 77, 133, 64,
            66, 83, 138, 83, 42, 42, 33, 27, 79, 26,
            35, 52, 31, 25, 26, 24, 20, 19, 11
        ],
        '收入': [
            202.0, 187.1, 166.2, 174.8, 110.9, 116.0, 118.0, 107.4, 87.6, 98.6,
            127.3, 66.3, 76.9, 94.9, 84.1, 64.6, 63.2, 48.6, 61.7, 47.9,
            57.6, 26.7, 48.5, 53.3, 40.7, 88.5, 33.5, 34.8, 63.4, 29.4,
            34.3, 38.9, 65.8, 21.4, 19.2, 19.5, 19.3, 12.4, 23.1, 11.7,
            16.3, 13.1, 8.0, 6.2, 6.3, 11.7, 8.7, 9.4, 5.3
        ],
        '收入排名': [
            1, 2, 4, 3, 8, 7, 6, 9, 13, 10,
            5, 16, 15, 11, 14, 18, 20, 24, 21, 26,
            22, 33, 25, 23, 27, 12, 31, 29, 19, 32,
            30, 28, 17, 35, 38, 36, 37, 41, 34, 42,
            39, 40, 46, 48, 47, 43, 45, 44, 49
        ],
        '收入占比': [
            0.07, 0.06, 0.06, 0.06, 0.04, 0.04, 0.04, 0.04, 0.03, 0.03,
            0.04, 0.02, 0.03, 0.03, 0.03, 0.02, 0.02, 0.02, 0.02, 0.02,
            0.02, 0.01, 0.02, 0.02, 0.01, 0.03, 0.01, 0.01, 0.02, 0.01,
            0.01, 0.01, 0.02, 0.01, 0.01, 0.01, 0.01, 0.00, 0.01, 0.00,
            0.01, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00
        ],
        '项目利润': [
            125.9, 103.5, 94.0, 80.6, 68.6, 64.4, 55.2, 53.3, 51.7, 47.9,
            41.9, 36.4, 36.5, 35.7, 34.7, 34.0, 27.1, 24.1, 23.9, 23.3,
            19.7, 18.5, 18.0, 17.3, 17.0, 16.2, 15.0, 15.0, 14.1, 12.6,
            12.9, 12.1, 11.4, 10.7, 9.7, 9.1, 7.1, 5.6, 5.7, 5.1,
            5.1, 3.7, 3.1, 2.9, 2.4, 2.1, 1.8, 0.8, -2.7
        ],
        '项目利润排名': [
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
            11, 13, 12, 14, 15, 16, 17, 18, 19, 20,
            21, 22, 23, 24, 25, 26, 27, 28, 29, 31,
            30, 32, 33, 34, 35, 36, 37, 39, 38, 41,
            40, 42, 43, 44, 45, 46, 47, 48, 49
        ],
        '项目利润占比': [
            0.09, 0.08, 0.07, 0.06, 0.05, 0.05, 0.04, 0.04, 0.04, 0.04,
            0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.02, 0.02, 0.02, 0.02,
            0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01,
            0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.00, 0.00, 0.00,
            0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00
        ],
        '高维毛利': [
            118.8, 96.7, 90.5, 76.0, 65.5, 61.2, 52.3, 50.0, 49.7, 45.6,
            38.7, 34.5, 34.4, 33.1, 32.6, 32.3, 25.8, 23.1, 22.0, 22.0,
            18.2, 17.8, 17.0, 16.2, 16.0, 14.4, 14.3, 14.2, 12.9, 12.0,
            12.0, 11.0, 10.4, 10.2, 9.1, 8.5, 6.7, 5.4, 5.1, 5.0,
            4.8, 3.5, 3.0, 2.8, 2.3, 2.0, 1.8, 0.6, -2.8
        ],
        '高维毛利排名': [
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
            11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
            21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
            31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
            41, 42, 43, 44, 45, 46, 47, 48, 49
        ],
        '高维毛利占比': [
            0.09, 0.08, 0.07, 0.06, 0.05, 0.05, 0.04, 0.04, 0.04, 0.04,
            0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.02, 0.02, 0.02, 0.02,
            0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01,
            0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.00, 0.00, 0.00,
            0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00
        ]
    }
    
    return pd.DataFrame(data)

def create_open_course_analysis():
    """创建公开课产品分析图表"""
    
    df = load_open_course_data()
    
    # 创建多个分析图表
    create_top_courses_chart(df)
    create_revenue_distribution_chart(df)
    create_profit_analysis_chart(df)
    create_instructor_performance_chart(df)
    create_comprehensive_dashboard(df)
    
    # 保存数据
    save_analysis_data(df)
    
    print("公开课产品分析完成！")

def create_top_courses_chart(df):
    """创建TOP课程分析图表"""
    
    # 取前15名课程
    top_15 = df.head(15)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12))
    
    # 收入TOP15
    ax1.barh(range(len(top_15)), top_15['收入'], color='#1f77b4', alpha=0.8)
    ax1.set_yticks(range(len(top_15)))
    ax1.set_yticklabels(top_15['班级名称'], fontsize=10)
    ax1.set_xlabel('收入 (万元)', fontsize=12)
    ax1.set_title('公开课收入TOP15', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # 添加数值标签
    for i, v in enumerate(top_15['收入']):
        ax1.text(v + 1, i, f'{v}万', va='center', fontsize=9)
    
    # 利润TOP15
    ax2.barh(range(len(top_15)), top_15['项目利润'], color='#ff7f0e', alpha=0.8)
    ax2.set_yticks(range(len(top_15)))
    ax2.set_yticklabels(top_15['班级名称'], fontsize=10)
    ax2.set_xlabel('项目利润 (万元)', fontsize=12)
    ax2.set_title('公开课利润TOP15', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    # 添加数值标签
    for i, v in enumerate(top_15['项目利润']):
        ax2.text(v + 1, i, f'{v}万', va='center', fontsize=9)
    
    plt.tight_layout()
    
    # 保存图表
    charts_dir = Path(CHARTS_DIR)
    charts_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(charts_dir / 'open_course_top15.png', dpi=300, bbox_inches='tight')
    plt.savefig(charts_dir / 'open_course_top15.pdf', bbox_inches='tight')
    plt.close()
    
    print("TOP15课程分析图表已生成")

def create_revenue_distribution_chart(df):
    """创建收入分布分析图表"""
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # 收入分布直方图
    ax1.hist(df['收入'], bins=20, color='#1f77b4', alpha=0.7, edgecolor='black')
    ax1.set_xlabel('收入 (万元)', fontsize=12)
    ax1.set_ylabel('课程数量', fontsize=12)
    ax1.set_title('收入分布直方图', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # 订单数量 vs 收入散点图
    ax2.scatter(df['订单数量'], df['收入'], alpha=0.6, color='#ff7f0e')
    ax2.set_xlabel('订单数量', fontsize=12)
    ax2.set_ylabel('收入 (万元)', fontsize=12)
    ax2.set_title('订单数量 vs 收入关系', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    # 添加趋势线
    z = np.polyfit(df['订单数量'], df['收入'], 1)
    p = np.poly1d(z)
    ax2.plot(df['订单数量'], p(df['订单数量']), "r--", alpha=0.8)
    
    # 利润率分析
    df['利润率'] = df['项目利润'] / df['收入'] * 100
    ax3.hist(df['利润率'], bins=20, color='#2ca02c', alpha=0.7, edgecolor='black')
    ax3.set_xlabel('利润率 (%)', fontsize=12)
    ax3.set_ylabel('课程数量', fontsize=12)
    ax3.set_title('利润率分布', fontsize=14, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    
    # 收入占比饼图（前10名）
    top_10 = df.head(10)
    others_revenue = df[10:]['收入'].sum()
    
    labels = list(top_10['班级名称']) + ['其他']
    sizes = list(top_10['收入']) + [others_revenue]
    colors = plt.cm.Set3(np.linspace(0, 1, len(labels)))
    
    ax4.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
    ax4.set_title('收入占比分布（TOP10+其他）', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    
    # 保存图表
    charts_dir = Path(CHARTS_DIR)
    plt.savefig(charts_dir / 'open_course_revenue_distribution.png', dpi=300, bbox_inches='tight')
    plt.savefig(charts_dir / 'open_course_revenue_distribution.pdf', bbox_inches='tight')
    plt.close()
    
    print("收入分布分析图表已生成")

def create_profit_analysis_chart(df):
    """创建利润分析图表"""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # 收入 vs 利润散点图
    ax1.scatter(df['收入'], df['项目利润'], alpha=0.6, s=60, color='#1f77b4')
    ax1.set_xlabel('收入 (万元)', fontsize=12)
    ax1.set_ylabel('项目利润 (万元)', fontsize=12)
    ax1.set_title('收入 vs 利润关系', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # 添加趋势线
    z = np.polyfit(df['收入'], df['项目利润'], 1)
    p = np.poly1d(z)
    ax1.plot(df['收入'], p(df['收入']), "r--", alpha=0.8)
    
    # 标注异常点
    for i, row in df.iterrows():
        if row['项目利润'] < 0:
            ax1.annotate(row['班级名称'], (row['收入'], row['项目利润']), 
                        xytext=(5, 5), textcoords='offset points', fontsize=8)
    
    # 利润率排名
    df_sorted = df.sort_values('利润率', ascending=False).head(20)
    
    ax2.barh(range(len(df_sorted)), df_sorted['利润率'], color='#2ca02c', alpha=0.8)
    ax2.set_yticks(range(len(df_sorted)))
    ax2.set_yticklabels(df_sorted['班级名称'], fontsize=9)
    ax2.set_xlabel('利润率 (%)', fontsize=12)
    ax2.set_title('利润率TOP20', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    # 添加数值标签
    for i, v in enumerate(df_sorted['利润率']):
        ax2.text(v + 1, i, f'{v:.1f}%', va='center', fontsize=8)
    
    plt.tight_layout()
    
    # 保存图表
    charts_dir = Path(CHARTS_DIR)
    plt.savefig(charts_dir / 'open_course_profit_analysis.png', dpi=300, bbox_inches='tight')
    plt.savefig(charts_dir / 'open_course_profit_analysis.pdf', bbox_inches='tight')
    plt.close()
    
    print("利润分析图表已生成")

def create_instructor_performance_chart(df):
    """创建讲师表现分析图表"""
    
    # 按讲师汇总数据
    instructor_stats = df.groupby('讲师').agg({
        '收入': 'sum',
        '项目利润': 'sum',
        '订单数量': 'sum',
        '班级名称': 'count'
    }).rename(columns={'班级名称': '课程数量'})
    
    instructor_stats = instructor_stats.sort_values('收入', ascending=False)
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # 讲师收入排名（前15）
    top_instructors = instructor_stats.head(15)
    ax1.barh(range(len(top_instructors)), top_instructors['收入'], color='#1f77b4', alpha=0.8)
    ax1.set_yticks(range(len(top_instructors)))
    ax1.set_yticklabels(top_instructors.index, fontsize=10)
    ax1.set_xlabel('总收入 (万元)', fontsize=12)
    ax1.set_title('讲师收入排名TOP15', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # 讲师利润排名（前15）
    top_profit_instructors = instructor_stats.sort_values('项目利润', ascending=False).head(15)
    ax2.barh(range(len(top_profit_instructors)), top_profit_instructors['项目利润'], color='#ff7f0e', alpha=0.8)
    ax2.set_yticks(range(len(top_profit_instructors)))
    ax2.set_yticklabels(top_profit_instructors.index, fontsize=10)
    ax2.set_xlabel('总利润 (万元)', fontsize=12)
    ax2.set_title('讲师利润排名TOP15', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    # 讲师课程数量分布
    course_counts = instructor_stats['课程数量'].value_counts().sort_index()
    ax3.bar(course_counts.index, course_counts.values, color='#2ca02c', alpha=0.8)
    ax3.set_xlabel('课程数量', fontsize=12)
    ax3.set_ylabel('讲师人数', fontsize=12)
    ax3.set_title('讲师课程数量分布', fontsize=14, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    
    # 讲师平均课程收入
    instructor_stats['平均课程收入'] = instructor_stats['收入'] / instructor_stats['课程数量']
    avg_revenue = instructor_stats.sort_values('平均课程收入', ascending=False).head(15)
    
    ax4.barh(range(len(avg_revenue)), avg_revenue['平均课程收入'], color='#d62728', alpha=0.8)
    ax4.set_yticks(range(len(avg_revenue)))
    ax4.set_yticklabels(avg_revenue.index, fontsize=10)
    ax4.set_xlabel('平均课程收入 (万元)', fontsize=12)
    ax4.set_title('讲师平均课程收入TOP15', fontsize=14, fontweight='bold')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # 保存图表
    charts_dir = Path(CHARTS_DIR)
    plt.savefig(charts_dir / 'open_course_instructor_performance.png', dpi=300, bbox_inches='tight')
    plt.savefig(charts_dir / 'open_course_instructor_performance.pdf', bbox_inches='tight')
    plt.close()
    
    print("讲师表现分析图表已生成")

def create_comprehensive_dashboard(df):
    """创建综合仪表板"""
    
    fig = plt.figure(figsize=(20, 16))
    
    # 创建网格布局
    gs = fig.add_gridspec(4, 4, hspace=0.3, wspace=0.3)
    
    # 1. 关键指标概览
    ax1 = fig.add_subplot(gs[0, :2])
    metrics = {
        '总收入': f"{df['收入'].sum():.1f}万元",
        '总利润': f"{df['项目利润'].sum():.1f}万元",
        '总订单': f"{df['订单数量'].sum()}单",
        '平均利润率': f"{(df['项目利润'].sum() / df['收入'].sum() * 100):.1f}%",
        '课程数量': f"{len(df)}门",
        '讲师数量': f"{df['讲师'].nunique()}人"
    }
    
    ax1.text(0.5, 0.5, '公开课关键指标\n\n' + '\n'.join([f'{k}: {v}' for k, v in metrics.items()]), 
             transform=ax1.transAxes, fontsize=14, ha='center', va='center',
             bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.5))
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.axis('off')
    
    # 2. 收入TOP10
    ax2 = fig.add_subplot(gs[0, 2:])
    top_10_revenue = df.head(10)
    ax2.bar(range(len(top_10_revenue)), top_10_revenue['收入'], color='#1f77b4', alpha=0.8)
    ax2.set_xticks(range(len(top_10_revenue)))
    ax2.set_xticklabels([name[:8] + '...' if len(name) > 8 else name for name in top_10_revenue['班级名称']], 
                       rotation=45, ha='right', fontsize=9)
    ax2.set_ylabel('收入 (万元)', fontsize=10)
    ax2.set_title('收入TOP10', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    # 3. 利润分布
    ax3 = fig.add_subplot(gs[1, :2])
    ax3.hist(df['项目利润'], bins=20, color='#ff7f0e', alpha=0.7, edgecolor='black')
    ax3.set_xlabel('项目利润 (万元)', fontsize=10)
    ax3.set_ylabel('课程数量', fontsize=10)
    ax3.set_title('利润分布', fontsize=12, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    
    # 4. 订单数量 vs 收入
    ax4 = fig.add_subplot(gs[1, 2:])
    ax4.scatter(df['订单数量'], df['收入'], alpha=0.6, color='#2ca02c')
    ax4.set_xlabel('订单数量', fontsize=10)
    ax4.set_ylabel('收入 (万元)', fontsize=10)
    ax4.set_title('订单数量 vs 收入', fontsize=12, fontweight='bold')
    ax4.grid(True, alpha=0.3)
    
    # 5. 讲师表现
    ax5 = fig.add_subplot(gs[2, :])
    instructor_revenue = df.groupby('讲师')['收入'].sum().sort_values(ascending=False).head(15)
    ax5.barh(range(len(instructor_revenue)), instructor_revenue.values, color='#d62728', alpha=0.8)
    ax5.set_yticks(range(len(instructor_revenue)))
    ax5.set_yticklabels(instructor_revenue.index, fontsize=10)
    ax5.set_xlabel('总收入 (万元)', fontsize=10)
    ax5.set_title('讲师收入排名TOP15', fontsize=12, fontweight='bold')
    ax5.grid(True, alpha=0.3)
    
    # 6. 收入占比
    ax6 = fig.add_subplot(gs[3, :2])
    top_5 = df.head(5)
    others_revenue = df[5:]['收入'].sum()
    labels = list(top_5['班级名称']) + ['其他44门课程']
    sizes = list(top_5['收入']) + [others_revenue]
    colors = plt.cm.Set3(np.linspace(0, 1, len(labels)))
    ax6.pie(sizes, labels=[label[:10] + '...' if len(label) > 10 else label for label in labels], 
            autopct='%1.1f%%', colors=colors, startangle=90)
    ax6.set_title('收入占比（TOP5+其他）', fontsize=12, fontweight='bold')
    
    # 7. 利润率分析
    ax7 = fig.add_subplot(gs[3, 2:])
    df['利润率'] = df['项目利润'] / df['收入'] * 100
    profit_rate_ranges = ['<20%', '20-40%', '40-60%', '60-80%', '>80%']
    profit_counts = [
        len(df[df['利润率'] < 20]),
        len(df[(df['利润率'] >= 20) & (df['利润率'] < 40)]),
        len(df[(df['利润率'] >= 40) & (df['利润率'] < 60)]),
        len(df[(df['利润率'] >= 60) & (df['利润率'] < 80)]),
        len(df[df['利润率'] >= 80])
    ]
    
    ax7.bar(profit_rate_ranges, profit_counts, color='#9467bd', alpha=0.8)
    ax7.set_xlabel('利润率区间', fontsize=10)
    ax7.set_ylabel('课程数量', fontsize=10)
    ax7.set_title('利润率分布区间', fontsize=12, fontweight='bold')
    ax7.grid(True, alpha=0.3)
    
    plt.suptitle('公开课产品综合分析仪表板', fontsize=16, fontweight='bold')
    
    # 保存图表
    charts_dir = Path(CHARTS_DIR)
    plt.savefig(charts_dir / 'open_course_dashboard.png', dpi=300, bbox_inches='tight')
    plt.savefig(charts_dir / 'open_course_dashboard.pdf', bbox_inches='tight')
    plt.close()
    
    print("综合仪表板已生成")

def save_analysis_data(df):
    """保存分析数据"""
    
    exports_dir = Path(EXPORTS_DIR)
    exports_dir.mkdir(parents=True, exist_ok=True)
    
    # 保存原始数据
    df.to_csv(exports_dir / 'open_course_data.csv', index=False, encoding='utf-8-sig')
    
    # 保存讲师汇总数据
    instructor_stats = df.groupby('讲师').agg({
        '收入': 'sum',
        '项目利润': 'sum',
        '订单数量': 'sum',
        '班级名称': 'count'
    }).rename(columns={'班级名称': '课程数量'})
    
    instructor_stats['平均课程收入'] = instructor_stats['收入'] / instructor_stats['课程数量']
    instructor_stats = instructor_stats.sort_values('收入', ascending=False)
    instructor_stats.to_csv(exports_dir / 'instructor_performance.csv', encoding='utf-8-sig')
    
    # 保存分析摘要
    summary = {
        '总收入': float(df['收入'].sum()),
        '总利润': float(df['项目利润'].sum()),
        '总订单': int(df['订单数量'].sum()),
        '平均利润率': float(df['项目利润'].sum() / df['收入'].sum() * 100),
        '课程数量': int(len(df)),
        '讲师数量': int(df['讲师'].nunique()),
        '收入最高课程': str(df.loc[df['收入'].idxmax(), '班级名称']),
        '利润最高课程': str(df.loc[df['项目利润'].idxmax(), '班级名称']),
        '收入最高讲师': str(instructor_stats.index[0]),
        '平均课程收入': float(df['收入'].mean()),
        '平均课程利润': float(df['项目利润'].mean())
    }
    
    import json
    with open(exports_dir / 'open_course_summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print("分析数据已保存")

if __name__ == "__main__":
    print("开始公开课产品分析...")
    create_open_course_analysis()
    print("公开课产品分析完成！") 