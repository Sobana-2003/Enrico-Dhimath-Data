import pandas as pd
import os

from sqlalchemy import create_engine, sql, text

from .DB_operations import table_metadata, get_create_scripts

def save_create_scripts_to_files(global_session_vars):
    file_path = global_session_vars["create_scripts_path"]
    conn_string = global_session_vars["local_db_string"]
    db_schema = global_session_vars["db_schema"]
    tables = global_session_vars["tables_for_views"]
    create_scripts = get_create_scripts(tables, conn_string, db_schema)
    for table, script in create_scripts.items():
        file_name = f"{table}_create_script.txt"
        completed_file_path = os.path.join(file_path, file_name)
        with open(completed_file_path, 'w') as file:
            file.write(f"-- Create script for table {table}\n")
            file.write(script + "\n\n")
        return print(f"Create script for table {table} saved to {completed_file_path}")

def persist_sheets_in_db(global_session_vars):
    df = global_session_vars["data_sheets_df"]
    table_name = global_session_vars["data_sheets_table_name"].strip("")
    conn_string = global_session_vars["local_db_string"]
    engine = create_engine(conn_string)
    table_creation = df.to_sql(table_name.lower(), engine, schema="dhimath_data", index=False, if_exists='replace')
    with engine.connect() as conn:
            view_name = f"{table_name}_view"
            sql_query = sql.text(f"""CREATE or REPLACE VIEW "dhimath_data"."{view_name.lower()}" AS (SELECT * FROM "dhimath_data"."{str(table_name).lower()}")""")
            conn.execute(sql_query)
    conn.commit()
    conn.close()
    return table_creation

def write_metadata_to_file(global_session_vars):
    table_names = global_session_vars["tables_for_views"]
    conn_string = global_session_vars["local_db_string"]
    output_path = global_session_vars["table_metadata"]

    for table_name in table_names:
        file_path = os.path.join(output_path, f"{table_name}_view.txt")  
        df = table_metadata(conn_string, table_name)  
        
        with open(file_path, 'w') as f:
            f.write(f"Table Name: {table_name}\n")
            f.write("Columns:\n")
            for _, row in df.iterrows():
                f.write(f"- {row['column_name']} ({row['data_type']})\n")

    return print(f"Table metadata files saved successfully")

def persist_db_info(global_session_vars):
    db_name = global_session_vars["database_name"]
    conn_string = global_session_vars["db_conn_string"]
    db_schema = global_session_vars["db_schema"]
    view_name = global_session_vars["views_created"]
    db_info_csv = global_session_vars["db_list"]
    rows = []
    for view in view_name:
        rows.append({
            'Database_name': db_name,
            'Database_conn_string': conn_string,
            'Database_schema_name': db_schema,
            'View_name': view,
            'Valid': 'Y'
        })
    df = pd.DataFrame(rows)
    df.to_csv(db_info_csv, mode='a', header=False, index=False)
    return df

def persist_sheets_info(global_session_vars):
    sheet_name = f"{global_session_vars["data_sheets_table_name"]}"
    db_name = global_session_vars["db_details"]["db_name"]
    db_schema = global_session_vars["db_details"]["db_schema_data"]
    conn_string = global_session_vars["local_db_string"]
    sheets_info_csv = global_session_vars["data_sheets_list"]
    csv_line = {
                'Database_name': db_name,
                'Database_conn_string': conn_string,
                'Database_schema_name': db_schema,
                'View_name': sheet_name,
                'Valid': 'Y'
            }
    df = pd.DataFrame(csv_line, index=[0])
    df.to_csv(sheets_info_csv, mode='a', header=False, index=False)
    return df