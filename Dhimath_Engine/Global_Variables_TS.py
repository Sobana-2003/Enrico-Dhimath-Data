import pandas as pd
from dotenv import load_dotenv
from datetime import datetime

 
load_dotenv()
 
label = "Dhimath"
 
user_id = "Prasanna"
 
global_session_variables = {
#Dhimath_TS_variables
    "version" : "2.0",  
    "user_id" : "Prasanna",
    "user_org" : "GreyWiz",
    "tab" : "tab1",
    "process_step" : "",
    "source_type" : "",
    "selected_tool_option" : "",
    "data_org_path": "",
    "data_file_path": "",
    "df": pd.DataFrame(),
    "org_data" : pd.DataFrame(),
    "grp_data" : pd.DataFrame(),
    "data": pd.DataFrame(),
    "index_col": 0,
    "target_cols": [],
    "analysis_type": "",
    "cond":True,
    "grp_target_cols" : [],
    "grp_target": [],
    "pred_cols" : [],
    "levels_" : [],
    "split_var" : []

}