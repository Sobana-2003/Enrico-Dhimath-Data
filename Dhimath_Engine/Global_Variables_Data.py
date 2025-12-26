import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
 
load_dotenv()
 
label = "Dhimath"
 
List_of_Vector_DB_types = ["FAISS",
                      "Chroma"]
 
List_of_text_splitter_types = ["Recursive Character",
                               "Character",
                               "NLTK(TBD)",
                               "Spacy(TBD)"]
 
temperature_list = [item/100 for item in range(0, 100, 5)]
search_iteration_list = [item for item in range(1,9,1)]
 
 
meta_data_folder = f"D:\\Dhimath\\dhimath-doc-streamlit-main\\Dhimath_Files"
 
 
user_id = "Sobana"
 
global_session_variables = {
#Dhimath_Doc_variables
    "version" : "1.0",  
    "user_id" : "Sobana",
    "user_org" : "GreyWiz",
    "tab" : "tab1",
    "process_step" : "",
    "source_type" : "",
    "selected_tool_option" : "",
#vector DB:
    "knowledge_base_path" : f"{meta_data_folder}\\Kb\\",
    #vectordb - vector_db_path + \\ + knowledge_base_name
    "vectordb": "",
    "vector_store_db" : "",
#llm,
    "selected_llm" : "",
    "selected_temp" : 0.0,
    "selected_s_kwargs" : 1,
    "llm" : "",
    "llm_file": "",
    "llm_path": f"{meta_data_folder}\\LLM_Models\\",
    "llm_parameters": {
            "streaming": True,
            "temperature": 0.3,
            "top_p": 1,
            "verbose": True,
            "n_ctx": 4096,
            "n_gpu_layers": -1,
            "search_kwargs": 2
        },
#Embedding
    "selected_emb": [],
    "embedding_name" : "",
    "emb_file": "",
    "emb_path": f"{meta_data_folder}\\LLM_Models\\Embedding_Models",
#Knowledge Base    
    "selected_kb" : [],
    "selected_kb_file": "",
    "knowledge_base" : "",
    "knowledge_base_name": "",
    "knowledge_base_name_0": "",
    "knowledge_base_parameters": {
            "chunk_size": 1000,
            "chunk_overlap": 0
              },
#Retrieval_models
    "qa_on" : "",
    "qa_off": "",
    "qa_exec_time" : 0,
    "retrieval_function" : "",
#Auto Learn
    #this is the base file path in which all the files references are made
    "kb_name": "",
    "files_path": f"{meta_data_folder}\\",
    #All the documents loaded is moved to this target path.. The documents to show in Quiz me / Chainlit will refer to this path
    "target_path": f"{meta_data_folder}\\Kb_Docs\\",
    "user_files_path": "",  
    "uploaded_files_path" : "",
#Quiz Me
    "question_id" : 0,
    "session_q_id" : 0,
    "question" : "",
    "edited_question": "",
    "answer" : "",
    "edited_answer":"",
    "metadata" : "",
    "restricted_scope" : True,
    "chat_history":[],
    "qa_exec_time":0,
#Dhimath_Data Variables
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
#Domainify
    "dataframe": pd.DataFrame(), ## Has been named as df as it is a common name which can be used in other places as well
    "domain_name": "",
    "summarised_df": pd.DataFrame(),
    "domainify_file_path": f"{meta_data_folder}\\{user_id}\\Domainify\\",
#Analyses
    "analyses_df": pd.DataFrame(columns=[
            'ID', 'Analyses', 'Edited_Analyses',  
            'Sql', 'Edited_Sql'
        ]),
    "analyses_files_path": f"{meta_data_folder}\\{user_id}\\Analyses\\",
#Quiz Data
"graph_df": pd.DataFrame(),
"sql_query": "",
"prompt_prefix": """
                    You are a seasoned data analyst. You have access to only views, so run only view compatible commands.
                    Search the table infomation given below and provide the necessary answers.
                 """,
"edited_prompt_prefix": "",
"prompt_suffix": """
                    Ensure your responses are thorough, accurate, and directly address the question.
                    Give the Final answer as a sql statement only.
                 """,
"edited_prompt_suffix" : "",
"graphs_prompt_prefix": """
                    You are a seasoned data analyst. You have access to only views so run only view compatible commands.
                    Search the custom table infomation and provide the necessary answers.
                    Give the Final answer as a sql statement only.
                   
                 """,
# "prompt_prefix": """Transform the following natural language requests into valid SQL queries. Assume a database with the following tables and columns exists:""",
"edited_graphs_prompt_prefix": "",
"graphs_prompt_suffix": """
                    Ensure your responses are thorough, accurate, and directly address the question.
                    Give the Final answer as a sql statement only.
                 """,
"edited_graphs_prompt_suffix" : "",
# "prompt_suffix": """""",
"data_file_df": pd.DataFrame(),
"agent_executor": "",
"data_file_answer": {},
"db_object": "",
#Coach
    "num_questions" : 10,
    "auto_qa_df": pd.DataFrame(columns=[
            'ID', 'Question', 'Edited_Questions',  
            'Answers', 'Edited_Answers' , 'Metadata'
        ]),
#Rules
    "rules_df_answers": pd.DataFrame(),
    "prompt_to_map_columns": "",
    "pandas_agent": "",
    "rules_data_file_df": pd.DataFrame(),
    "rules_df": pd.DataFrame(columns=[
            'ID', 'Rules', 'Equations',  
            'Answers','Edited_Answers', 'Metadata'
        ]),
#Enrich
    # "files_dir_path": f"{meta_data_folder}\\data_models\\{user_id}\\Enrich\\",
    "files_dir_path": f"{meta_data_folder}\\data",
#Database Connection
    "db_conn" : "",
    "db_details" : {
            'db_type' : "PostGreSQL",
            # 'db_path' : "G:\\DuckDBData\\dhimath",
            'db_name' : 'Dhimath',
            'db_user' :'postgres',
            'db_password' : 'sobana',
            'db_host' : 'localhost',
            'db_port' : '5432',
            'db_schema_name' : 'dhimath_doc',
            'db_schema_data': 'dhimath_data',
                  },
 
# UI Dropdown Values
    "list_of_llm_models" : [],
    "list_of_embedding_models" : [],
    "list_of_knowledge_bases" : [],
    "list_of_guided_learn_files" : [],
    # Used by Dhimath.Data
    "list_of_domains":["Battery","Solar","Wind"],
    "list_of_domain_tables":["Battery_Dataset","Solar","Wind"],
 
# List_of_CSV_Files
    "kb_names_file_list": f"{meta_data_folder}\\Config_Files\\kb_info.csv",
    "emb_names_file_list": f"{meta_data_folder}\\Config_Files\\List_of_Embeddings.csv",
    "llm_file_list" : f"{meta_data_folder}\\Config_Files\\List_of_LLMs.csv",
    "guided_learn_file_list" :f"{meta_data_folder}\\Config_Files\\List_of_Guided_Learn_Files.csv",
    "db_list": f"{meta_data_folder}\\Config_Files\\DB_info.csv",
    "data_sheets_list": f"{meta_data_folder}\\Config_Files\\DataSheets_info.csv",
    "description_list": f"{meta_data_folder}\\Config_Files\\Descriptions_info.csv",
    "create_scripts_list": f"{meta_data_folder}\\Config_Files\\Create_Scripts_info.csv",
    "analyses_list": f"{meta_data_folder}\\Config_Files\\Analyses_info.csv",
    }
 
 
 
 
#---- Capturing Data for Insights in Database ---------
 
q_and_a_log = {
#'Question_ID' : [0],  # commented as this is auto increment in the database
'session_q_id' : [0],
'question' : [""],
'edited_question' : [""],
'answer' : [""],
'edited_answer' : [""],
'doc_references' : [""],
'answer_correctness' : ['Yes'],
'process_step' : [""],
'embedding_id' : [""],
'embedding_name' : [""],
'llm_id' : [""],
'llm_name' : [""],
'llm_parameters' : [""],
'knowledge_base_id' : [""],
'knowledge_base_name' : [""],
'knowledge_base_parameters' : [""],
'response_start_time' : [datetime.now()],
'response_end_time' : [datetime.now()],
'answer_response_time' : [0.0],
'created_date' : [datetime.now()],
'user_id' : ["Prasanna"],
'user_org':["GreyWiz"]
}
 
 
auto_learn_log = {
#'Auto_Learn_Run_ID' : [0], # commented as this is auto increment in the database
'knowledge_base_id' : [0],
'knowledge_base_name' : [],
'embedding_id' : [0],
'embedding_name' : [],
'process_step' : ['Auto Learn'],
'number_of_docs_processed' : [0],
'run_start_time' : [datetime.now()],
'run_end_time' : [datetime.now()],
'doc_loading_time_in_secs' : [0.0],
'doc_processing_time_in_secs' : [0.0],
'embedding_load_time_in_secs' : [0.0],
'text_emb_creation_time_in_secs' : [0.0],
'knowledge_base_creation_time' : [0.0],
'auto_Learn_total_exec_time_in_secs' : [0.0],
'created_date' : [datetime.now()],
'user_id' : ["Sobana"],
'user_org' : ["GreyWiz"]
}
 