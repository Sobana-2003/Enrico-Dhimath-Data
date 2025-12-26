from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_config import db_credentials
import os
from utils.utils import get_category

def get_conn():
    engine = create_engine(f"{os.environ.get('POSTGRES_CONN')}", pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()

def get_conn_string(db_type:str):
    driver = db_credentials["sqlserver"]["driver"]
    host = db_credentials["sqlserver"]["host"]
    port = db_credentials["sqlserver"]["port"]
    db_name = db_credentials["sqlserver"]["database"]
    user = db_credentials["sqlserver"]["username"]
    password = db_credentials["sqlserver"]["password"]
    schema = "dbo"
    if db_type.lower() == "sqlserver":
        connection_string = (
            f"DRIVER={driver};"
            f"SERVER={host},{port};"
            f"DATABASE={db_name};"
            f"UID={user};"
            f"PWD={password};"
            f"Encrypt=yes;"
            f"TrustServerCertificate=yes;"
            f"Trusted_Connection=no;"
        )
        params = quote_plus(connection_string)
        conn_str = f"mssql+pyodbc:///?odbc_connect={params}"
    
    return conn_str,schema

def get_tables(conn_string: str, schema_name: str):
    query = ""
    print("I am getting tables for schema: ", schema_name)
    engine = create_engine(f"{conn_string}")
    print(" Table Conn string",conn_string)
    if "postgresql" in conn_string:
        query = f"""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = '{schema_name}' AND table_type = 'BASE TABLE'
            ORDER BY table_name;
            """
    elif "mysql" in conn_string:
        query = f"""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = '{schema_name}'
            ORDER BY table_name;
            """
    with engine.connect() as conn:
        result = conn.execute(text(query))
        tables = [row[0] for row in result.fetchall()]
    return tables

def get_columns(conn_string:str, schema:str, table:str):
    query = f"""SELECT column_name,data_type
               FROM information_schema.columns
               WHERE table_schema = '{schema}' AND table_name = '{table}'
               ORDER BY ordinal_position;
               """
    engine = create_engine(f"{conn_string}")
    with engine.connect() as conn:
        result = conn.execute(text(query))
        columns = [{"columnName": r[0], "dataType": r[1], "columnCategory": get_category(r[1])} for r in result.fetchall()]  
    return columns


def summarise_table(conn_string: str, schema: str, table_name: str):
    summary = []
    engine = create_engine(conn_string)
    with engine.connect() as conn:
        if "postgresql" in conn_string:
            result = conn.execute(text("""
                    SELECT column_name, data_type
                    FROM information_schema.columns
                    WHERE table_name = :table
                                """), {"table": table_name})
            columns = result.fetchall()
            for col_name, data_type in columns:
                if 'int' in data_type or 'decimal' in data_type or 'numeric' in data_type:
                    result = conn.execute(text(f"SELECT MIN({col_name}), MAX({col_name}) FROM {schema}.{table_name}"))
                    min_val, max_val = result.fetchone()
                elif 'char' in data_type or 'text' in data_type or 'varchar' in data_type:
                    result = conn.execute(text(f"SELECT MIN(LENGTH({col_name})), MAX(LENGTH({col_name})) FROM {schema}.{table_name}"))
                    min_val, max_val = result.fetchone()
                    min_val = f"{min_val}"
                    max_val = f"{max_val}"
                else:
                    min_val = max_val = "N/A"
                summary.append({
                    'Column_Name': col_name,
                    'Data_Type': data_type,
                    'Min_Value': min_val,
                    'Max_Value': max_val
                })
            result = conn.execute(text(f"SELECT COUNT(*) FROM {schema}.{table_name}"))
            num_rows = result.scalar()
            num_cols = len(columns)
        elif "mssql" in conn_string:
            result = conn.execute(text("""
                    SELECT column_name, data_type
                    FROM information_schema.columns
                    WHERE table_name = :table
                                """), {"table": table_name})
            columns = result.fetchall()
            for col_name, data_type in columns:
                if 'int' in data_type or 'decimal' in data_type or 'numeric' in data_type:
                    result = conn.execute(text(f"SELECT MIN({col_name}), MAX({col_name}) FROM [{schema}].[{table_name}]"))
                    min_val, max_val = result.fetchone()
                elif 'char' in data_type or 'text' in data_type or 'varchar' in data_type:
                    result = conn.execute(text(f"SELECT MIN(LEN([{col_name}])), MAX(LEN([{col_name}])) FROM [{schema}].[{table_name}]"))
                    min_val, max_val = result.fetchone()
                    min_val =  str(min_val) if min_val is not None else None
                    max_val =  str(min_val) if min_val is not None else None
                else:
                    min_val = max_val = "N/A"
                summary.append({
                    'Column_Name': col_name,
                    'Data_Type': data_type,
                    'Min_Value': min_val,
                    'Max_Value': max_val
                })
            result = conn.execute(text(f"SELECT COUNT(*) FROM {schema}.{table_name}"))
            num_rows = result.scalar()
            num_cols = len(columns)
    return summary, num_rows, num_cols
