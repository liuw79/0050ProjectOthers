import csv

input_csv = '/Users/comdir/SynologyDrive/0050Project/KK.Time/2025-10-16 - 2025-11-14-classified-v2.csv'
output_csv = '/Users/comdir/SynologyDrive/0050Project/KK.Time/2025-10-16 - 2025-11-14-classified-v3.csv'

output_data = []
final_fieldnames = []

try:
    with open(input_csv, mode='r', encoding='utf-8-sig') as infile:
        reader = csv.DictReader(infile)
        
        # 确定输出文件的列名：排除所有中间分类列，最后统一为'分类'
        base_fieldnames = [f for f in reader.fieldnames if f not in ['分类', '新自动分类', '修正分类']]
        final_fieldnames = base_fieldnames + ['分类']

        for row in reader:
            # 整合分类：优先使用'修正分类'，其次是'新自动分类'
            final_category = row.get('修正分类', '').strip()
            if not final_category:
                final_category = row.get('新自动分类', '').strip()
            
            # 构建新的行数据
            new_row = {key: row[key] for key in base_fieldnames if key in row}
            new_row['分类'] = final_category
            output_data.append(new_row)

    # 写入新的 v3 文件
    if output_data:
        with open(output_csv, mode='w', encoding='utf-8-sig', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=final_fieldnames)
            writer.writeheader()
            writer.writerows(output_data)
        print(f"文件已成功清理并保存为: {output_csv}")
    else:
        print("未能读取输入文件或文件为空。")

except FileNotFoundError:
    print(f"错误：输入文件未找到 {input_csv}")
except Exception as e:
    print(f"处理过程中发生未知错误: {e}")