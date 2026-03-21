import csv

file_path = '/Users/comdir/SynologyDrive/0050Project/KK.Time/2025-10-16 - 2025-11-14-classified.csv'
discrepancies = []

with open(file_path, mode='r', encoding='utf-8-sig') as infile:
    reader = csv.DictReader(infile)
    # 检查表头是否正确
    if '分类' not in reader.fieldnames or '修正分类' not in reader.fieldnames:
        print("错误：CSV文件缺少'分类'或'修正分类'列。")
        exit()

    for row in reader:
        manual_classification = row.get('修正分类', '').strip()
        auto_classification = row.get('分类', '').strip()
        
        if manual_classification and auto_classification != manual_classification:
            discrepancies.append({
                'title': row['日程主题'],
                'auto': auto_classification,
                'manual': manual_classification
            })

if discrepancies:
    print(f"发现 {len(discrepancies)} 处自动分类与您的手动修正不一致：")
    print("-" * 80)
    print(f"{'日程主题':<40} | {'自动分类':<20} | {'您的修正':<20}")
    print("-" * 80)
    for item in discrepancies:
        print(f"{item['title']:<40} | {item['auto']:<20} | {item['manual']:<20}")
    print("-" * 80)
else:
    print("未发现自动分类与手动修正的差异。")