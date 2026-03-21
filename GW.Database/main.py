import os
import json
from fastapi import FastAPI, HTTPException, Query
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel, Field, RootModel
from typing import List, Dict, Any, Optional
from datetime import datetime

# --- Database Configuration ---
# It's recommended to use environment variables for credentials in a real application
DB_DRIVER_PATH = "/usr/local/opt/freetds/lib/libtdsodbc.so"
DB_HOST = "47.115.38.118"
DB_PORT = "9024"
DB_USER = "gw_reader"
DB_PASSWORD = "cZ1cM5nX5eX7"
DB_NAME = "GW_Course"

os.environ['ODBCINSTINI'] = '/usr/local/etc/odbcinst.ini'

# Connection string
DATABASE_URL = f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_HOST},{DB_PORT}/{DB_NAME}?driver={DB_DRIVER_PATH}"

# --- FastAPI Application ---
app = FastAPI(
    title="Database Schema Viewer",
    description="An API to inspect and view the structure of a remote SQL Server database.",
    version="1.0.0",
)

# --- Global Data Dictionary (loaded from JSON) ---
data_dictionary = {}
DATA_DICTIONARY_PATH = "/Users/liuwei/SynologyDrive/0050Project/GW.Database/docs/data_dictionary.json"

# --- Database Engine ---
try:
    engine = create_engine(DATABASE_URL)
    # Test the connection
    with engine.connect() as connection:
        pass
except SQLAlchemyError as e:
    print(f"Error creating database engine: {e}")
    engine = None

# --- Pydantic Models for API Response ---
class ColumnInfo(BaseModel):
    name: str
    type: str
    nullable: bool
    default: Any = None
    primary_key: bool = False
    chinese_name: Optional[str] = None
    description: Optional[str] = None
    notes: Optional[str] = None

class TableInfo(BaseModel):
    name: str
    chinese_name: Optional[str] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    columns: List[ColumnInfo]

class SchemaInfo(BaseModel):
    tables: List[str]

class RowData(RootModel[Dict[str, Any]]):
    pass

# --- API Endpoints ---
@app.on_event("startup")
async def startup_event():
    global data_dictionary
    if engine is None:
        raise RuntimeError("Database connection could not be established. The application cannot start.")
    
    # Load data dictionary on startup
    try:
        with open(DATA_DICTIONARY_PATH, "r", encoding="utf-8") as f:
            data_dictionary = json.load(f)
        print(f"Data dictionary loaded successfully from {DATA_DICTIONARY_PATH}")
    except FileNotFoundError:
        print(f"Warning: Data dictionary file not found at {DATA_DICTIONARY_PATH}. Proceeding without it.")
    except json.JSONDecodeError as e:
        print(f"Error: Could not decode data dictionary JSON from {DATA_DICTIONARY_PATH}: {e}")

@app.get("/", tags=["Status"])
async def get_status():
    """Check the status of the API and database connection."""
    try:
        with engine.connect() as connection:
            return {"status": "ok", "database_connection": "successful"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=503, detail=f"Database connection failed: {e}")

@app.get("/schema", response_model=SchemaInfo, tags=["Schema"])
async def get_schema_overview():
    """
    Get a list of all table names in the public schema.
    """
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        return {"tables": tables}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Could not inspect database schema: {e}")

@app.get("/tables/{table_name}", response_model=TableInfo, tags=["Schema"])
async def get_table_details(table_name: str):
    """
    Get detailed information about a specific table, including its columns.
    """
    try:
        inspector = inspect(engine)
        if not inspector.has_table(table_name):
            raise HTTPException(status_code=404, detail=f"Table '{table_name}' not found.")

        # Get table info from data dictionary
        table_dict_info = data_dictionary.get(table_name, {})
        table_chinese_name = table_dict_info.get('chinese_name')
        table_description = table_dict_info.get('description')
        table_notes = table_dict_info.get('notes')

        columns = inspector.get_columns(table_name)
        
        pk_constraint = inspector.get_pk_constraint(table_name)
        primary_key_columns = pk_constraint.get('constrained_columns', [])

        column_details = []
        for col in columns:
            # Try to get additional info from data dictionary
            col_dict_info = next((c for c in table_dict_info.get('columns', []) if c['name'] == col['name']), {})

            column_info = ColumnInfo(
                name=col['name'],
                type=str(col['type']),
                nullable=col['nullable'],
                default=col.get('default'),
                primary_key=col['name'] in primary_key_columns,
                chinese_name=col_dict_info.get('chinese_name'),
                description=col_dict_info.get('description'),
                notes=col_dict_info.get('notes')
            )
            column_details.append(column_info)
            
        return TableInfo(
            name=table_name,
            chinese_name=table_chinese_name,
            description=table_description,
            notes=table_notes,
            columns=column_details
        )
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Could not retrieve details for table '{table_name}': {e}")

@app.get("/data/{table_name}", response_model=List[RowData], tags=["Data"])
async def get_table_data(
    table_name: str, 
    limit: int = Query(10, ge=1, le=100), # Limit to 10 rows by default, max 100
    status: Optional[int] = None, # New parameter for status
    city: Optional[str] = None, # New parameter for city
    exclude_test: bool = Query(False, description="Exclude records with '测试' in Info_Title or Type = 3"), # New parameter to exclude test records
    title_contains: Optional[str] = None, # New parameter to filter by title
    start_date_after: Optional[str] = None # New parameter to filter by start date
):
    """
    Get sample data from a specific table, with optional filtering by status, city, and excluding test records.
    """
    try:
        inspector = inspect(engine)
        if not inspector.has_table(table_name):
            raise HTTPException(status_code=404, detail=f"Table '{table_name}' not found.")

        with engine.connect() as connection:
            # Build the WHERE clause dynamically
            where_clauses = []
            if status is not None:
                where_clauses.append(f"Status = {status}")
            if city is not None:
                where_clauses.append(f"Info_Address LIKE N'%{city}%'") # Assuming Info_Address contains city

            if exclude_test and table_name == "TranActivity": # Only apply to TranActivity table
                where_clauses.append(f"Info_Title NOT LIKE N'%测试%'")
                where_clauses.append(f"Type != 3") # Assuming Type = 3 means '测试'
            
            if title_contains is not None:
                where_clauses.append(f"Info_Title LIKE N'%{title_contains}%'")

            if start_date_after is not None:
                # Assuming start_date_after is in 'YYYY-MM-DD' format
                where_clauses.append(f"ActivityStart >= '{start_date_after}'")


            where_clause_str = ""
            if where_clauses:
                where_clause_str = " WHERE " + " AND ".join(where_clauses)

            # Use text() for raw SQL and TOP clause for SQL Server
            query = text(f"SELECT TOP {limit} * FROM [{table_name}]{where_clause_str}")
            result = connection.execute(query)
            
            # Convert Row objects to dictionaries
            rows_as_dicts = [row._asdict() for row in result.fetchall()]
            return rows_as_dicts
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Could not retrieve data from table '{table_name}': {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    import uvicorn
    print("Starting server. Access the API docs at http://127.0.0.1:8001/docs")
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)