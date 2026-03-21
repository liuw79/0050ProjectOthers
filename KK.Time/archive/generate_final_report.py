import csv
from datetime import datetime
from collections import defaultdict

# --- 1. 辅助函数：计算时长 ---
def calculate_duration_hours(start_str, end_str):
    try:
        # 尝试匹配 "YYYY/MM/DD HH:MM" 格式
        start_time = datetime.strptime(start_str, '%Y/%m/%d %H:%M')
        end_time = datetime.strptime(end_str, '%Y/%m/%d %H:%M')
        duration = end_time - start_time
        return duration.total_seconds() / 3600
    except ValueError:
        # 如果格式不匹配，可以添加其他格式的处理或返回0
        return 0

# --- 2. 主逻辑 ---
def main():
    input_csv = '/Users/comdir/SynologyDrive/0050Project/KK.Time/2025-10-16 - 2025-11-14-classified-v2.csv'
    output_md = '/Users/comdir/SynologyDrive/0050Project/KK.Time/时间投入战略贡献度最终分析报告.md'

    category_hours = defaultdict(float)
    total_hours = 0

    with open(input_csv, mode='r', encoding='utf-8-sig') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            # 优先使用修正分类，否则使用新自动分类
            category = row.get('修正分类', '').strip()
            if not category:
                category = row.get('新自动分类', '未分类').strip()

            duration = calculate_duration_hours(row['日程开始时间'], row['日程结束时间'])
            
            if duration > 0:
                category_hours[category] += duration
                total_hours += duration

    # --- 3. 生成Markdown报告 ---
    with open(output_md, 'w', encoding='utf-8') as md_file:
        md_file.write("# 时间投入战略贡献度最终分析报告\n\n")
        md_file.write("**分析周期**: 2025-10-16 至 2025-11-14\n")
        md_file.write(f"**总记录时长**: {total_hours:.2f} 小时\n\n")
        md_file.write("## 各战略方向时间投入分布\n\n")
        md_file.write("| 战略分类 | 总时长（小时） | 时间占比 |\n")
        md_file.write("|:---|:---:|:---:|\n")

        # 按时间降序排序
        sorted_categories = sorted(category_hours.items(), key=lambda item: item[1], reverse=True)

        for category, hours in sorted_categories:
            percentage = (hours / total_hours) * 100 if total_hours > 0 else 0
            md_file.write(f"| {category} | {hours:.2f} | {percentage:.2f}% |\n")
        
        md_file.write("\n## 结论与建议\n\n")
        md_file.write("1.  **核心投入**: 从数据上看，您的时间主要投入在...（请根据数据自行解读）。\n")
        md_file.write("2.  **潜在优化点**: ...（例如，某个非核心分类占比过高，或某个核心分类投入不足）。\n")
        md_file.write("3.  **后续步骤**: 建议定期（如每月）进行此类分析，以持续追踪和优化时间分配，确保与您的战略目标保持一致。\n")

    print(f"分析报告已生成：{output_md}")

if __name__ == "__main__":
    main()