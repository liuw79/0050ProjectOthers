import os
import json
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import SQLAlchemyError

DB_DRIVER_PATH = "/usr/local/opt/freetds/lib/libtdsodbc.so"
DB_HOST = "47.115.38.118"
DB_PORT = "9024"
DB_USER = "gw_reader"
DB_PASSWORD = "cZ1cM5nX5eX7"
DB_NAME = "GW_Course"

os.environ['ODBCINSTINI'] = '/usr/local/etc/odbcinst.ini'

DATABASE_URL = f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_HOST},{DB_PORT}/{DB_NAME}?driver={DB_DRIVER_PATH}"

try:
    engine = create_engine(DATABASE_URL)
    inspector = inspect(engine)

    db_tables = inspector.get_table_names()

    # Read existing data_dictionary.json
    data_dict_path = "/Users/liuwei/SynologyDrive/0050Project/GW.Database/docs/data_dictionary.json"
    existing_dict = {}
    if os.path.exists(data_dict_path):
        with open(data_dict_path, "r") as f:
            existing_dict = json.load(f)

    existing_table_names = set(existing_dict.keys())

    missing_tables = [table for table in db_tables if table not in existing_table_names]

    if missing_tables:
        print("以下表格在数据库中存在，但未包含在 data_dictionary.json 中：")
        for table_name in missing_tables:
            print(f"- {table_name}")
            try:
                columns = inspector.get_columns(table_name)
                print("  字段：")
                for col in columns:
                    print(f"    - {col['name']} ({col['type']})")
            except SQLAlchemyError as e:
                print(f"  无法获取表 {table_name} 的字段信息: {e}")
    else:
        print("data_dictionary.json 中已包含数据库中的所有表格。")

except SQLAlchemyError as e:
    print(f"数据库连接或操作失败: {e}")
except FileNotFoundError:
    print(f"错误: 未找到 data_dictionary.json 文件于 {data_dict_path}")
except json.JSONDecodeError:
    print(f"错误: data_dictionary.json 文件格式不正确于 {data_dict_path}")
