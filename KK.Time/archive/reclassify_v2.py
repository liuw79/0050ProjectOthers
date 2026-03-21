import csv
import re

# --- 1. 解析规则文件 ---
def parse_rules(rule_file_path):
    cat_map = {}
    keyword_to_cat = {}
    default_category = ''

    with open(rule_file_path, 'r', encoding='utf-8') as f:
        current_category = ''
        for line in f:
            # 匹配 "### X. Category Name"
            cat_match = re.match(r"### \d+\. (.+)", line)
            if cat_match:
                current_category = cat_match.group(1).strip()
                continue

            # 匹配关键词行
            if '关键词' in line and current_category:
                keywords_line = next(f, '').strip()
                keywords = [k.strip() for k in keywords_line.split(',')]
                cat_map[current_category] = keywords
                for keyword in keywords:
                    if keyword:
                        keyword_to_cat[keyword] = current_category
            
            # 查找默认分类
            if '这是默认分类' in line and current_category:
                default_category = current_category

    if not default_category:
        # 如果没有明确的默认分类，则使用最后一个解析的分类
        if current_category:
            default_category = current_category
        else:
            raise ValueError("无法在规则文件中确定默认分类。")
            
    return keyword_to_cat, default_category

# --- 2. 分类函数 ---
def classify_event(title, keyword_to_cat, default_category):
    for keyword, category in keyword_to_cat.items():
        if keyword in title:
            return category
    return default_category

# --- 3. 主逻辑 ---
def main():
    rule_file = '/Users/comdir/SynologyDrive/0050Project/KK.Time/时间分析分类规则.md'
    original_csv = '/Users/comdir/SynologyDrive/0050Project/KK.Time/2025-10-16 - 2025-11-14.csv'
    manual_classified_csv = '/Users/comdir/SynologyDrive/0050Project/KK.Time/2025-10-16 - 2025-11-14-classified.csv'
    output_csv = '/Users/comdir/SynologyDrive/0050Project/KK.Time/2025-10-16 - 2025-11-14-classified-v2.csv'

    # 加载手动分类数据
    manual_classifications = {}
    with open(manual_classified_csv, mode='r', encoding='utf-8-sig') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            # 使用日程主题和开始时间作为唯一键
            key = (row['日程主题'], row['日程开始时间'])
            manual_classifications[key] = row.get('修正分类', '').strip()

    # 解析新规则并重新分类
    keyword_to_cat, default_cat = parse_rules(rule_file)
    
    output_data = []
    fieldnames = []
    with open(original_csv, mode='r', encoding='utf-8-sig') as infile:
        # 跳过前两行元数据
        next(infile)
        next(infile)
        
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['新自动分类', '修正分类']
        for row in reader:
            # 清理可能的空列名键
            row = {k: v for k, v in row.items() if k is not None}
            title = row['日程主题']
            key = (title, row['日程开始时间'])
            
            new_auto_class = classify_event(title, keyword_to_cat, default_cat)
            manual_class = manual_classifications.get(key, '')
            
            new_row = row.copy()
            new_row['新自动分类'] = new_auto_class
            new_row['修正分类'] = manual_class
            output_data.append(new_row)

    # 写入新的CSV文件
    with open(output_csv, mode='w', encoding='utf-8-sig', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_data)

    print(f"处理完成！已生成新的分类文件：{output_csv}")

    # --- 4. 对比分析 ---
    correct_count = 0
    remaining_discrepancies = []
    total_manual = 0
    for row in output_data:
        if row['修正分类']:
            total_manual += 1
            if row['新自动分类'] == row['修正分类']:
                correct_count += 1
            else:
                remaining_discrepancies.append(row)

    print("\n--- 分类效果验证 ---")
    if total_manual > 0:
        accuracy = (correct_count / total_manual) * 100
        print(f"在您手动修正的 {total_manual} 个条目中，新规则的准确率为: {accuracy:.2f}% ({correct_count}/{total_manual})")
        print(f"剩余不一致条目数量: {len(remaining_discrepancies)}")

        if remaining_discrepancies:
            print("\n--- 剩余不一致的条目 ---")
            print("-" * 80)
            print(f"{'日程主题':<40} | {'新自动分类':<20} | {'您的修正':<20}")
            print("-" * 80)
            for item in remaining_discrepancies:
                print(f"{item['日程主题']:<40} | {item['新自动分类']:<20} | {item['修正分类']:<20}")
            print("-" * 80)
    else:
        print("未找到可供对比的手动修正分类。")

if __name__ == "__main__":
    main()