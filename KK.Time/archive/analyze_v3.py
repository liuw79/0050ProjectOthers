import csv
from datetime import datetime
from collections import defaultdict

# --- 1. 辅助函数：计算时长 ---
def calculate_duration_hours(start_str, end_str):
    try:
        start_time = datetime.strptime(start_str, '%Y/%m/%d %H:%M')
        end_time = datetime.strptime(end_str, '%Y/%m/%d %H:%M')
        duration = end_time - start_time
        return duration.total_seconds() / 3600
    except ValueError:
        return 0

# --- 2. 主逻辑 ---
def main():
    input_csv = '/Users/comdir/SynologyDrive/0050Project/KK.Time/2025-10-16 - 2025-11-14-classified-v3.csv'
    output_md = '/Users/comdir/SynologyDrive/0050Project/KK.Time/时间投入战略贡献度分析报告-v3.md'

    category_hours = defaultdict(float)
    total_hours = 0

    with open(input_csv, mode='r', encoding='utf-8-sig') as infile:
        # 跳过可能存在的元数据行，直接找到表头
        # 在v3版本中，我们假设第一行就是表头
        reader = csv.DictReader(infile)
        for row in reader:
            category = row.get('分类', '未分类').strip()
            duration = calculate_duration_hours(row['日程开始时间'], row['日程结束时间'])
            
            if duration > 0:
                category_hours[category] += duration
                total_hours += duration

    # --- 3. 生成Markdown报告 ---
    with open(output_md, 'w', encoding='utf-8') as md_file:
        md_file.write("# 时间投入战略贡献度分析报告 (v3)\n\n")
        md_file.write("**分析文件**: `2025-10-16 - 2025-11-14-classified-v3.csv`\n")
        md_file.write("**分析周期**: 2025-10-16 至 2025-11-14\n")
        md_file.write(f"**总记录时长**: {total_hours:.2f} 小时\n\n")
        md_file.write("## 各战略方向时间投入分布\n\n")
        md_file.write("| 战略分类 | 总时长（小时） | 时间占比 |\n")
        md_file.write("|:---|:---:|:---:|\n")

        sorted_categories = sorted(category_hours.items(), key=lambda item: item[1], reverse=True)

        for category, hours in sorted_categories:
            percentage = (hours / total_hours) * 100 if total_hours > 0 else 0
            md_file.write(f"| {category} | {hours:.2f} | {percentage:.2f}% |\n")
        
        md_file.write("\n---\n*这份报告基于最终清理版的 v3 数据生成。*")

    print(f"最终分析报告已生成：{output_md}")

if __name__ == "__main__":
    main()