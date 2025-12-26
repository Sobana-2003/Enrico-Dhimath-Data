import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
 
load_dotenv()
 
label = "Dhimath"

meta_data_folder = f"H:\\Python Code\\Stream_Lit_Apps\\Dhimath\\Master_Files"
 
 
user_id = "Prasanna"
 
global_session_variables = {
#Dhimath_XLR_variables
    "version" : "1.0",  
    "user_id" : "Prasanna",
    "user_org" : "GreyWiz",
    "tab" : "tab1",
    "process_step" : "",
    "source_type" : "",
    "selected_tool_option" : "",
    "valid_user": False,
#Load Excel
    #this is the base file path in which all the files references are made
    "files_path": f"{meta_data_folder}\\",
    #All the documents loaded is moved to this target path
    "target_path": f"{meta_data_folder}\\Kb_Docs\\",
    "user_files_path": "",  
    "uploaded_files_path" : "",
    "existing_files_info" : pd.DataFrame(),
    "uploaded_xls_files_path" : "",
    "uploaded_file_name": "",
    "xls_file_name": "",
    "uploaded_file_sheets": [],
    "xls_sheet_df": pd.DataFrame(),
    "cleansed_df": pd.DataFrame(),
    "target_df": pd.DataFrame(),
    "process_clicked" : False,
    "skip_clicked" : False,
    "save_clicked" : False,
    "selected_sheet": "",
    'file_sheet_id' : 0,
#Cleanse
    "selected_process_table": "",

#Map
    "selected_cleansed_table": "",

#Dedupe
    "contacts_df": pd.DataFrame(),
    "selected_columns_to_dedup": ['company_name','contact_name', 'contact_phone_number', 'contact_email_address'],
#Connect Souce
    #Database
    "database_name": "",
    "tables_from_db": [], # Tables from the database
    "tables_for_views": [], # Tables to create views
    "db_conn_string": "",
    "db_schema": "",
    "views_created": [],
    "local_db_string": "postgresql://postgres:Post1234@localhost:5432/Dhimath",
    #Data Sheets
    "data_sheets_df": pd.DataFrame(),
    "data_sheets_table_name": "",
    "table_name": "",
    #Common
    "create_scripts_path": f"{meta_data_folder}\\{user_id}\\Create_Scripts\\",
    "table_metadata": f"{meta_data_folder}\\{user_id}\\Table_Metadata\\",
# #Domainify

#Database Connection
    "db_conn" : "",
    "db_details" : {
            'db_type' : "PostGreSQL",
            # 'db_path' : "G:\\DuckDBData\\dhimath",
            'db_name' : 'Systech',
            'db_user' :'postgres',
            'db_password' : 'Post1234',
            'db_host' : 'localhost',
            'db_port' : '5432',
            'db_schema_name': 'systech_metadata'
                  },
    'db_schema_raw_files' : 'systech_raw',
    'db_schema_cleanse_files': 'systech_cleanse',
    'db_schema_data': 'systech_data',
    'pg_db_engine':"",
 
    }
 
 
 
#---- Capturing Data for Insights and traceability in Database ---------

uploaded_file_log = {
# 'file_id' : [0],
'org_id' : [0],
'file_name' : [""],
'file_upload_path' : [""],
'file_type' : [""],
'loaded_date' : [datetime.now()],
'loaded_by' : [""],
'assigned_date' : [datetime.now()],
'assigned_to' : [""],
'marked_for_deletion' : ["N"],
'user_id' : [""],
'user_org' : [""],
}

uploaded_file_sheet_log = {
# 'file_sheet_id' : [0],
'org_id' : [0],
'file_id' : [0],
'file_name' : [""],
'sheet_name' : [""],
'loaded_table_name' : [""],
'number_of_columns' : [0],
'number_of_rows' : [0],
'corrected_number_of_columns' : [0],
'corrected_number_of_rows' : [0],
'column_from' : [""],
'column_to' : [""],
'row_from' : [0],
'row_to' : [0],
'header_y_n' : [False],
'processed_y_n' : [False],
'processed_by' : [""],
'processed_date' : [datetime.now()],
'cleansed_y_n' : [False],
'cleansed_by' : [""],
'cleansed_date' : [datetime.now()],
'mapped_y_n' : [False],
'mapped_by' : [""],
'mapped_date' : [datetime.now()],
'created_date' : [datetime.now()],
'marked_for_deletion' : ["N"],
'skipped_reason' : [""],
'user_id' : [""],
'user_org' : [""],
}


dedup_run_log = {
# 'dedup_run_id' : [0],
'org_id' : [0],
'source_schema_name' : [""],
'source_table_name' : [""],
'number_of_columns' : [0],
'target_schema_name' : [""],
'target_table_name' : [""],
'columns_selected_for_dedup' : [""],
'number_of_rows_before_dedup' : [0],
'number_of_rows_after_dedup' : [0],
'dedup_run_date' : [datetime.now()],
'user_id' : [""],
'user_org' : [""],
}


source_to_target_mapping = {
# 'source_to_target_mapping_id' : [0],
'org_id' : [0],
'file_id' : [0],
'file_sheet_id' : [0],
'file_name' : [""],
'file_sheet_name' : [""],
'source_schema_name' : [""],
'source_table_name' : [""],
'target_schema_name' : [""],
'target_table_name' : [""],
'source_column_name' : [""],
'source_column_type' : [""],
'target_column_name' : [""],
'target_column_type' : [""],
'created_date' : [datetime.now()],
'created_by' : [""],
'updated_date' : [datetime.now()],
'updated_by' : [""],
'user_org' : [""],
}
