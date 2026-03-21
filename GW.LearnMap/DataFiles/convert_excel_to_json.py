import pandas as pd
import json
import math
import os # Import os module

# --- 配置 ---
excel_file_path = 'datafiles/原始表格.xlsx'  # 输入的 Excel 文件路径
json_output_dir = 'datafiles'              # 输出 JSON 文件的目录
json_file_name = 'courses.json'        # 输出的 JSON 文件名
json_file_path = os.path.join(json_output_dir, json_file_name) # 组合完整的输出路径
header_row_index = 2                   # Excel 中实际表头所在的行号（0-based index, 第3行是2）(已更正)
# --- 配置结束 ---

def clean_value(value):
    """处理 Pandas 读取可能产生的 NaN 值，并去除不必要的空格"""
    if isinstance(value, float) and math.isnan(value):
        return ""
    if isinstance(value, str):
        # Preserve intentional newlines within cells, just strip leading/trailing whitespace
        return value.strip()
    return value

print(f"正在读取 Excel 文件: {excel_file_path}...")
try:
    # 读取 Excel，指定表头行，并将所有数据读为字符串以避免类型推断问题
    df = pd.read_excel(excel_file_path, header=header_row_index, dtype=str)

    # 在处理前打印原始读取到的列名，用于调试
    print("原始读取到的列名:", df.columns.tolist())

    # 清理列名中的潜在换行符和多余空格
    df.columns = [str(col).replace('\n', '').replace('\r', '').strip() for col in df.columns]
    print("清理后的列名:", df.columns.tolist()) # 打印清理后的列名

    # 填充 NaN 值为空字符串 (即使读为str, fillna仍然有用)
    df = df.fillna('')

    # 重命名课程名称列
    course_name_original = '商学课/课后辅导/入企服务'
    course_name_clean = '课程名称'
    if course_name_original in df.columns:
        df.rename(columns={course_name_original: course_name_clean}, inplace=True)
        print(f"列 '{course_name_original}' 已重命名为 '{course_name_clean}'")
    else:
        print(f"警告：未找到列 '{course_name_original}' 用于重命名。检查上面打印的列名。")
        # Try to proceed if the column already has the clean name or exists anyway
        if course_name_clean in df.columns:
            print(f"列 '{course_name_clean}' 已存在.")
        elif any(col == course_name_original for col in df.columns):
             course_name_clean = course_name_original # Fallback if original name exists
             print(f"将使用原始列名 '{course_name_original}'")
        else:
             print(f"错误：无法找到关键的课程名称列 '{course_name_original}' 或 '{course_name_clean}'。请检查Excel表头行 ({header_row_index+1}) 和上面打印的列名。")
             exit(1) # Exit with error code 1

    # 识别主要列
    category_col = '分类'
    date_col = '上课日期'
    city_col = '上课城市'

    # 检查其他必要列是否存在
    missing_cols = []
    if category_col not in df.columns:
        missing_cols.append(category_col)
    if date_col not in df.columns:
        missing_cols.append(date_col)
    if city_col not in df.columns:
        missing_cols.append(city_col)
    if missing_cols:
        print(f"错误：Excel文件中 (表头行 {header_row_index+1}) 缺少以下必要列: {', '.join(missing_cols)}。请检查上面打印的列名。")
        exit(1)

    processed_courses = []
    current_course = None

    print("开始处理数据行...")
    for index, row in df.iterrows():
        # 将 row 转换为字典，方便访问，并清理值
        # Only include columns that have a non-empty name
        row_dict = {col: clean_value(row[col]) for col in df.columns if col and str(col).strip()}

        is_new_course = bool(row_dict.get(category_col)) and bool(row_dict.get(course_name_clean))
        has_schedule = bool(row_dict.get(date_col)) or bool(row_dict.get(city_col))

        if is_new_course:
            # 开始一个新课程
            # Make a copy to avoid modifying the original dict iterated over
            current_course = row_dict.copy()
            current_course['schedules'] = []

            if has_schedule:
                current_course['schedules'].append({
                    "date": row_dict.get(date_col, ""),
                    "city": row_dict.get(city_col, "")
                })
            # 清理掉原始的单独日期和城市字段
            current_course.pop(date_col, None)
            current_course.pop(city_col, None)
            processed_courses.append(current_course)

        elif current_course and has_schedule:
            # 这是现有课程的附加排期
            current_course['schedules'].append({
                "date": row_dict.get(date_col, ""),
                "city": row_dict.get(city_col, "")
            })
        # else: # 忽略既不是新课程，也没有排期的行 (可能是空行或注释行)
        #     pass # print(f"忽略行 {index+header_row_index+2}: {row_dict}")


    print(f"数据处理完成，共处理 {len(processed_courses)} 个主课程条目。")

    # 确保输出目录存在
    os.makedirs(json_output_dir, exist_ok=True)

    print(f"正在写入 JSON 文件: {json_file_path}...")

    # 写入 JSON 文件
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(processed_courses, f, ensure_ascii=False, indent=2)

    print("JSON 文件生成成功！")

except FileNotFoundError:
    print(f"错误：无法找到 Excel 文件 '{excel_file_path}'。请确保文件路径正确。")
except ImportError:
    print("错误：缺少必要的库。请运行 'pip install pandas openpyxl'")
except Exception as e:
    print(f"处理过程中发生错误：{e}")
    import traceback
    traceback.print_exc() # Print detailed traceback for debugging 