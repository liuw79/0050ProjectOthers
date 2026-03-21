import os
import json
import requests # Import requests library to call FastAPI
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Dict, Any, Optional # Corrected import

# --- Database Configuration (for direct DB access if needed, but we'll use API) ---
DB_DRIVER_PATH = "/usr/local/opt/freetds/lib/libtdsodbc.so"
DB_HOST = "47.115.38.118"
DB_PORT = "9024"
DB_USER = "gw_reader"
DB_PASSWORD = "cZ1cM5nX5eX7"
DB_NAME = "GW_Course"

os.environ['ODBCINSTINI'] = '/usr/local/etc/odbcinst.ini'

DATABASE_URL = f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_HOST},{DB_PORT}/{DB_NAME}?driver={DB_DRIVER_PATH}"

# --- FastAPI Endpoint Configuration ---
FASTAPI_BASE_URL = "http://127.0.0.1:8001"

# List of tables to query (can be refined based on your feedback)
tables_to_query = [
    "Assess", "BigShot", "Channels", "ClassTeacher", "Consumer", "Course", 
    "FeedbackCourse", "FeedbackQuestion", "FeedbackQuestionInstance", "FeedbackQuestionOption",
    "FlowerTransferLog", "ForwardContent", "GwbLog", "MentorDataChangeLog", "MentorDataFields",
    "MentorDatas", "OrganizationEmployees", "OrganizationRoles", "Organizations", "RefundOrder",
    "RetrainingApply", "Scores", "StoredCard", "TranActivity", "TranActivityBuyer",
    "TranActivityOrder", "UserPropDefine", "UserPropInstance", "UserPropInstanceBZR",
    "UserPropOption", "UserServer", "UserShareRpItem", "UserSubscribe", "VerificationFormList",
    "UserStoredCard", "View_UserFollow", 
    "Advert", "Apply", "BankAccountLog", "banner", 
    "course_learning", "order_info", "UserWallet", "UserWalletLog" 
]

def get_table_data_from_api(table_name: str, limit: int = 5) -> Optional[List[Dict[str, Any]]]:
    """Fetches table data from the FastAPI endpoint."""
    url = f"{FASTAPI_BASE_URL}/data/{table_name}?limit={limit}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"  API 查询失败: {e}")
        return None

def format_data_as_markdown_table(data: List[Dict[str, Any]]) -> str:
    """Formats a list of dictionaries as a Markdown table."""
    if not data:
        return "| (无数据) |\n|---|"

    headers = list(data[0].keys())
    markdown_table = "|" + "|".join(headers) + "|\n"
    markdown_table += "|" + "|".join(["---"] * len(headers)) + "|\n"

    for row in data:
        row_values = [str(row.get(header, "NULL")) for header in headers]
        markdown_table += "|" + "|".join(row_values) + "|\n"
    return markdown_table

print("--- 查询结果 ---\n")

for table_name in tables_to_query:
    print(f"### 表名: {table_name}\n")
    table_data = get_table_data_from_api(table_name)
    if table_data is not None:
        print(format_data_as_markdown_table(table_data))
    print("\n" + "="*50 + "\n") # Separator for clarity