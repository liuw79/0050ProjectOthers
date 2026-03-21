#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Drucker's Time Management Analysis
Based on "The Effective Executive" principles
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from collections import defaultdict

def parse_time(time_str):
    """Parse time string to datetime"""
    return pd.to_datetime(time_str, format='%Y/%m/%d %H:%M')

def calculate_duration(row):
    """Calculate duration in hours"""
    start = parse_time(row['日程开始时间'])
    end = parse_time(row['日程结束时间'])
    return (end - start).total_seconds() / 3600

def analyze_drucker_time_management(csv_file):
    """Analyze time records using Drucker's framework"""
    
    # Load data
    df = pd.read_csv(csv_file)
    
    # Calculate duration for each event
    df['时长(小时)'] = df.apply(calculate_duration, axis=1)
    
    # Convert start time to datetime for date analysis
    df['开始日期'] = pd.to_datetime(df['日程开始时间'], format='%Y/%m/%d %H:%M')
    df['日期'] = df['开始日期'].dt.date
    df['星期几'] = df['开始日期'].dt.day_name()
    df['小时'] = df['开始日期'].dt.hour
    
    print("="*80)
    print("德鲁克时间管理分析报告")
    print("基于《卓有成效的管理者》(The Effective Executive)")
    print("="*80)
    print()
    
    # Basic statistics
    total_days = (df['开始日期'].max() - df['开始日期'].min()).days + 1
    total_hours = df['时长(小时)'].sum()
    total_events = len(df)
    
    print(f"📊 基本统计")
    print(f"  分析时段: {df['开始日期'].min().date()} 至 {df['开始日期'].max().date()}")
    print(f"  总天数: {total_days} 天")
    print(f"  总事件数: {total_events} 个")
    print(f"  总时间投入: {total_hours:.1f} 小时")
    print(f"  日均时间投入: {total_hours/total_days:.1f} 小时/天")
    print()
    
    # ========================================
    # Drucker Principle 1: Record Time (诊断)
    # ========================================
    print("="*80)
    print("一、时间记录分析 (Record Time - 诊断)")
    print("="*80)
    print()
    
    # Time distribution by category
    print("1.1 时间分布 - 实际时间都花在哪里？")
    print("-"*80)
    category_time = df.groupby('分类')['时长(小时)'].agg(['sum', 'count', 'mean'])
    category_time['占比%'] = (category_time['sum'] / total_hours * 100)
    category_time = category_time.sort_values('sum', ascending=False)
    category_time.columns = ['总时长(小时)', '事件数', '平均时长(小时)', '占比%']
    
    for idx, row in category_time.iterrows():
        print(f"  {idx}")
        print(f"    总时长: {row['总时长(小时)']:.1f}小时 ({row['占比%']:.1f}%)")
        print(f"    事件数: {int(row['事件数'])}个, 平均时长: {row['平均时长(小时)']:.1f}小时")
        print()
    
    # Strategic vs Operational time
    print("1.2 战略性 vs 运营性时间分配")
    print("-"*80)
    strategic_categories = ['公司战略与组织建设', '产品开发与创新', '产品开发与新品创新']
    operational_categories = ['后端服务', '团队管理与组织建设', '组织建设']
    personal_categories = ['个人成长与生活']
    
    strategic_time = df[df['分类'].isin(strategic_categories)]['时长(小时)'].sum()
    operational_time = df[df['分类'].isin(operational_categories)]['时长(小时)'].sum()
    personal_time = df[df['分类'].isin(personal_categories)]['时长(小时)'].sum()
    
    print(f"  战略性工作: {strategic_time:.1f}小时 ({strategic_time/total_hours*100:.1f}%)")
    print(f"  运营性工作: {operational_time:.1f}小时 ({operational_time/total_hours*100:.1f}%)")
    print(f"  个人成长与生活: {personal_time:.1f}小时 ({personal_time/total_hours*100:.1f}%)")
    print()
    print(f"  💡 德鲁克观点: 高层管理者应该将更多时间用于战略性工作，")
    print(f"     而非陷入日常运营事务中。")
    print()
    
    # ========================================
    # Drucker Principle 2: Manage Time (治疗)
    # ========================================
    print("="*80)
    print("二、时间管理分析 (Manage Time - 识别时间浪费)")
    print("="*80)
    print()
    
    # 2.1 Meeting fragmentation
    print("2.1 会议碎片化分析")
    print("-"*80)
    
    # Count meetings per day
    meetings_per_day = df.groupby('日期').size()
    avg_meetings_per_day = meetings_per_day.mean()
    
    # Short meetings (< 1 hour)
    short_meetings = df[df['时长(小时)'] < 1]
    short_meeting_ratio = len(short_meetings) / len(df) * 100
    
    # Very short meetings (< 0.5 hour)
    very_short_meetings = df[df['时长(小时)'] <= 0.5]
    very_short_ratio = len(very_short_meetings) / len(df) * 100
    
    print(f"  日均会议/事件数: {avg_meetings_per_day:.1f} 个")
    print(f"  短会议(<1小时): {len(short_meetings)}个 ({short_meeting_ratio:.1f}%)")
    print(f"  超短会议(≤30分钟): {len(very_short_meetings)}个 ({very_short_ratio:.1f}%)")
    print()
    print(f"  ⚠️  德鲁克警告: 过多的短会议会造成时间碎片化，")
    print(f"      降低深度工作效率。每次切换任务都有认知成本。")
    print()
    
    # 2.2 Recurring meetings analysis
    print("2.2 重复性会议分析")
    print("-"*80)
    recurring = df[df['是否重复性日程'].str.contains('是', na=False)]
    recurring_time = recurring['时长(小时)'].sum()
    recurring_ratio = recurring_time / total_hours * 100
    
    print(f"  重复性会议总时间: {recurring_time:.1f}小时 ({recurring_ratio:.1f}%)")
    print(f"  重复性会议数量: {len(recurring)}个")
    print()
    
    recurring_summary = recurring.groupby('日程主题')['时长(小时)'].agg(['count', 'sum', 'mean'])
    recurring_summary = recurring_summary.sort_values('sum', ascending=False)
    recurring_summary.columns = ['出现次数', '总时长(小时)', '平均时长(小时)']
    
    print("  主要重复性会议:")
    for idx, row in recurring_summary.head(10).iterrows():
        print(f"    • {idx}")
        print(f"      {int(row['出现次数'])}次, 共{row['总时长(小时)']:.1f}小时, 均{row['平均时长(小时)']:.1f}小时/次")
    print()
    print(f"  💡 德鲁克建议: 定期审视重复性会议是否仍然必要，")
    print(f"     是否可以合并、缩短或取消。")
    print()
    
    # 2.3 Time distribution by hour
    print("2.3 时间分布 - 一天中的高峰时段")
    print("-"*80)
    hourly_dist = df.groupby('小时').size()
    peak_hours = hourly_dist.nlargest(5)
    
    print("  会议/活动最集中的时段:")
    for hour, count in peak_hours.items():
        print(f"    {hour:02d}:00-{hour+1:02d}:00  {count}个事件")
    print()
    print(f"  💡 德鲁克建议: 识别自己的高效时段，将其保护起来")
    print(f"     用于处理最重要的工作，而非被会议占满。")
    print()
    
    # 2.4 Long meetings and events
    print("2.4 长时间会议/事件分析")
    print("-"*80)
    long_events = df[df['时长(小时)'] >= 4].sort_values('时长(小时)', ascending=False)
    
    print(f"  长时间事件(≥4小时): {len(long_events)}个")
    print()
    if len(long_events) > 0:
        print("  主要长时间事件:")
        for _, row in long_events.head(10).iterrows():
            print(f"    • {row['日程主题']}: {row['时长(小时)']:.1f}小时 [{row['分类']}]")
        print()
    
    # ========================================
    # Drucker Principle 3: Consolidate Time (整合)
    # ========================================
    print("="*80)
    print("三、时间整合分析 (Consolidate Time - 大块连续时间)")
    print("="*80)
    print()
    
    # 3.1 Continuous time blocks
    print("3.1 可支配连续时间分析")
    print("-"*80)
    
    # Group by date and analyze
    daily_analysis = []
    for date in df['日期'].unique():
        daily = df[df['日期'] == date].sort_values('开始日期')
        
        # Calculate gaps between events
        gaps = []
        for i in range(len(daily) - 1):
            end_current = parse_time(daily.iloc[i]['日程结束时间'])
            start_next = parse_time(daily.iloc[i+1]['日程开始时间'])
            gap = (start_next - end_current).total_seconds() / 3600
            if gap > 0:
                gaps.append(gap)
        
        daily_events = len(daily)
        daily_hours = daily['时长(小时)'].sum()
        max_gap = max(gaps) if gaps else 0
        avg_gap = np.mean(gaps) if gaps else 0
        
        daily_analysis.append({
            'date': date,
            'events': daily_events,
            'hours': daily_hours,
            'max_gap': max_gap,
            'avg_gap': avg_gap
        })
    
    daily_df = pd.DataFrame(daily_analysis)
    
    # Days with large continuous time blocks
    good_days = daily_df[daily_df['max_gap'] >= 3]
    
    print(f"  有≥3小时连续空档的天数: {len(good_days)}天 (占{len(good_days)/len(daily_df)*100:.1f}%)")
    print(f"  平均最大连续空档: {daily_df['max_gap'].mean():.1f}小时")
    print(f"  平均事件间隔: {daily_df['avg_gap'].mean():.1f}小时")
    print()
    print(f"  ⚠️  德鲁克强调: 管理者需要大块的连续时间(至少3-4小时)")
    print(f"      来处理重要工作。零碎时间只能处理琐事。")
    print()
    
    # 3.2 Deep work time availability
    print("3.2 深度工作时间评估")
    print("-"*80)
    
    # Estimate available deep work time (assuming 8-hour workday minus meetings)
    workdays = len([d for d in daily_df['date'] if pd.to_datetime(d).weekday() < 5])
    total_scheduled = total_hours
    theoretical_work_hours = workdays * 8
    theoretical_available = theoretical_work_hours - total_scheduled
    
    print(f"  工作日天数: {workdays}天")
    print(f"  理论工作时间: {theoretical_work_hours:.0f}小时 (按8小时/天)")
    print(f"  已安排时间: {total_scheduled:.1f}小时")
    print(f"  理论可支配时间: {theoretical_available:.1f}小时 ({theoretical_available/theoretical_work_hours*100:.1f}%)")
    print()
    
    # But considering fragmentation...
    fragmented_days = len(daily_df[daily_df['max_gap'] < 2])
    print(f"  高度碎片化天数(最大空档<2h): {fragmented_days}天 ({fragmented_days/len(daily_df)*100:.1f}%)")
    print()
    print(f"  💡 德鲁克观点: 可支配时间越少，管理者越无法完成重要工作。")
    print(f"     应该主动创造大块时间，而非被动接受碎片化日程。")
    print()
    
    # ========================================
    # Drucker Key Questions
    # ========================================
    print("="*80)
    print("四、德鲁克三个关键问题")
    print("="*80)
    print()
    
    print("4.1 哪些活动完全不必做？(如果不做，会有什么影响？)")
    print("-"*80)
    
    # Identify potentially unnecessary activities
    low_impact_keywords = ['沟通', '对齐', '同步', '预备会', '会前会']
    potential_unnecessary = df[df['日程主题'].str.contains('|'.join(low_impact_keywords), na=False)]
    potential_time = potential_unnecessary['时长(小时)'].sum()
    
    print(f"  包含'沟通/对齐/同步/预备'关键词的会议:")
    print(f"    数量: {len(potential_unnecessary)}个")
    print(f"    时间: {potential_time:.1f}小时 ({potential_time/total_hours*100:.1f}%)")
    print()
    print("  主要事项:")
    for _, row in potential_unnecessary.nlargest(10, '时长(小时)').iterrows():
        print(f"    • {row['日程主题']}: {row['时长(小时)']:.1f}小时")
    print()
    print(f"  💭 反思: 这些沟通会议是否都必要？能否通过文档、异步沟通代替？")
    print()
    
    print("4.2 哪些活动可以由别人代做？(授权)")
    print("-"*80)
    
    # Activities that might be delegated
    delegatable_categories = ['后端服务', '团队管理与组织建设']
    delegatable = df[df['分类'].isin(delegatable_categories)]
    delegatable_time = delegatable['时长(小时)'].sum()
    
    print(f"  可能可授权的工作(后端服务+团队管理):")
    print(f"    时间: {delegatable_time:.1f}小时 ({delegatable_time/total_hours*100:.1f}%)")
    print()
    
    # Specific activities
    operational_meetings = df[
        (df['分类'] == '团队管理与组织建设') & 
        (df['日程主题'].str.contains('周会|同步|对齐', na=False))
    ]
    print(f"  运营性周会/同步会:")
    print(f"    数量: {len(operational_meetings)}个")
    print(f"    时间: {operational_meetings['时长(小时)'].sum():.1f}小时")
    print()
    print(f"  💭 反思: 作为高层管理者，哪些会议必须亲自参加？")
    print(f"     哪些可以授权下属处理后汇报关键信息？")
    print()
    
    print("4.3 哪些活动在浪费别人的时间？")
    print("-"*80)
    
    # Very short meetings that might waste others' time
    very_short = df[df['时长(小时)'] <= 0.5]
    very_short_time = very_short['时长(小时)'].sum()
    
    print(f"  超短会议(≤30分钟):")
    print(f"    数量: {len(very_short)}个")
    print(f"    时间: {very_short_time:.1f}小时")
    print()
    print("  主要超短会议:")
    for _, row in very_short.nlargest(15, '时长(小时)').iterrows():
        print(f"    • {row['日程主题']}: {row['时长(小时)']*60:.0f}分钟")
    print()
    print(f"  💭 反思: 这些30分钟会议，考虑到准备和切换成本，")
    print(f"     是否真的有效率？能否合并或改为邮件/异步沟通？")
    print()
    
    # ========================================
    # Recommendations
    # ========================================
    print("="*80)
    print("五、基于德鲁克理论的改进建议")
    print("="*80)
    print()
    
    print("✅ 关键建议:")
    print()
    
    # Recommendation 1
    strategic_ratio = strategic_time / total_hours * 100
    if strategic_ratio < 50:
        print("1. 增加战略性工作时间")
        print(f"   当前战略性工作仅占{strategic_ratio:.1f}%，建议提升至50%以上。")
        print(f"   作为高层管理者，应该'做正确的事'而非仅'正确地做事'。")
        print()
    
    # Recommendation 2
    if very_short_ratio > 30:
        print("2. 减少碎片化会议")
        print(f"   当前{very_short_ratio:.1f}%的会议≤30分钟，碎片化严重。")
        print(f"   建议:")
        print(f"   - 设定最短会议时长(如45分钟)")
        print(f"   - 合并相关主题的会议")
        print(f"   - 用异步沟通替代部分短会")
        print()
    
    # Recommendation 3
    if recurring_ratio > 25:
        print("3. 审视重复性会议的必要性")
        print(f"   当前{recurring_ratio:.1f}%时间用于重复性会议。")
        print(f"   建议每季度审视:")
        print(f"   - 哪些可以取消？")
        print(f"   - 哪些可以降低频率？")
        print(f"   - 哪些可以缩短时长？")
        print()
    
    # Recommendation 4
    if len(good_days) < len(daily_df) * 0.3:
        print("4. 主动创造大块连续时间")
        print(f"   当前仅{len(good_days)/len(daily_df)*100:.1f}%的天数有≥3小时连续时间。")
        print(f"   建议:")
        print(f"   - 每周设定1-2个'无会议日'(No Meeting Days)")
        print(f"   - 将会议集中在特定时段(如下午)")
        print(f"   - 上午时段保护起来做深度工作")
        print()
    
    # Recommendation 5
    print("5. 应用德鲁克的时间管理流程")
    print(f"   - 持续记录: 保持当前的时间记录习惯")
    print(f"   - 定期诊断: 每月分析一次时间使用情况")
    print(f"   - 果断治疗: 识别并消除时间浪费")
    print(f"   - 系统整合: 创造并保护大块时间用于重要工作")
    print()
    
    # Recommendation 6
    print("6. 区分'重要'与'紧急'")
    print(f"   德鲁克提醒: 管理者容易被'紧急'的事情驱动，")
    print(f"   而忽略'重要但不紧急'的战略性工作。")
    print(f"   建议每周固定时间处理重要但不紧急的工作:")
    print(f"   - 战略思考")
    print(f"   - 人才发展")
    print(f"   - 创新探索")
    print(f"   - 系统优化")
    print()
    
    print("="*80)
    print("💡 德鲁克名言:")
    print("   '时间是最稀缺的资源，如果不能管理时间，")
    print("    就什么都管理不了。'")
    print("="*80)
    print()
    
    # Export detailed analysis
    return {
        'category_time': category_time,
        'daily_analysis': daily_df,
        'recurring_summary': recurring_summary,
        'strategic_time': strategic_time,
        'operational_time': operational_time,
        'personal_time': personal_time
    }

if __name__ == "__main__":
    csv_file = "2025-10-16 - 2025-11-14-classified-v3.csv"
    results = analyze_drucker_time_management(csv_file)
    
    print("\n分析完成！")


