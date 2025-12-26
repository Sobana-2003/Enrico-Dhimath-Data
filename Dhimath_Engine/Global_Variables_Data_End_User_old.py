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
 
 
meta_data_folder = f"H:\\Python Code\\Stream_Lit_Apps\\Dhimath\\Master_Files"
 
 
user_id = "Prasanna"
 
global_session_variables = {
#Dhimath_Doc_variables
    "version" : "1.0",  
    "user_id" : "Prasanna",
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
    "db_conn_string": "postgresql://postgres:Post1234@localhost:5432/Dhimath",
    "db_schema": "dhimath_data",
    "views_created": [],
    "local_db_string": "postgresql://postgres:Post1234@localhost:5432/Dhimath",
    #Data Sheets
    "data_sheets_df": pd.DataFrame(),
    "data_sheets_table_name": "",
    "table_name": "",
    #Common
    "create_scripts_path": f"{meta_data_folder}\\{user_id}\\Create_Scripts\\",
    "table_metadata": f"{meta_data_folder}\\{user_id}\\Table_Metadata\\",
    "pandas_df" : pd.DataFrame(),
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
'category_values_dict' : "",
"sql_query": "",
"sql_output" : "[]",
"prompt_prefix" : "",
"prompt_prefix_1" : """
                You have access to the table metadata in the prompt. Utilise it to answer questions correctly.
                
                Use SELECT date_part('month', (SELECT current_timestamp)) to get the current month. 
                
                If this month is mentioned always the year is the current year.

                Do NOT use the column attrition_capacity.

                If it is mentioned as capacity always consider it as sum (allocated_capacity).

                If the user prompt has a value which is not part of the column names, look for those values from below columns 
                while constructing the SQL where clause with left part as one of these column names and right part as the value:
                    associate_service_area,
                    associate_group,
                    associate_department,
                    associate_section,
                    associate_top_section,
                    associate_business_unit,
                    associate_top_business_unit,
                    sector,
                    gb,
                    planning_gb.

                Following are the sectors:
                    BBE2773,
                    BBG3709,
                    BBI7169,
                    BBM6059,
                    Connec8358,
                    EIGROW6886,
                    GROW5447,
                    Integr7180,
                    Intern4385,
                    NULL9621,
                    OTHERS9975,
                    SDS1525
                    .

                Following are the project_service_areas:
                    BD4871,
                    GS5747,
                    MPS5457,
                    MS8750,
                    NULL9621,
                    SO1995,
                    SX8654,
                    TE-Cor9396
                    .

                Following are the project_sub_service_areas:
                    BD4871,
                    CVS1848,
                    GS5747,
                    ITRAMS7525,
                    MPS5457,
                    MS-ETT1003,
                    MS8750,
                    NULL9621,
                    PS7133,
                    RBEI_C6815,
                    SDS/GP5484,
                    SDS_CO4051,
                    SO1995,
                    SX8654,
                    TE-Cor9396,
                    VM3226
                    .

                To calculate the allocated %, use the calculation below only:
                    1. don't use the billed_capacity and end_capacity for this calculation.
                    2. Allocated % = sum(allocated_capacity)/(sum(allocated_capacity) + sum(vkm_capacity) + sum(ms_capacity) + sum(sl2_capacity))

                To calculate the billing utilization, use the calculation below only:
                    1. Billing Utilization % = sum(billed_capacity)/(sum(allocated_capacity) + sum(vkm_capacity) + sum(ms_capacity) + sum(sl2_capacity))



                """,
"prompt_suffix" : "",
"prompt_prefix_2": """
                You are a seasoned data analyst. You have access to only views so run only view compatible commands. 
                Search the custom table infomation and provide the necessary answers. 

                Give the Final answer as a sql statement only.

                Use SELECT date_part('month', (SELECT current_timestamp)) to get the current month. 

                If this month is mentioned always the year is the current year.
                
                dont use the column attrition_capacity.
                
                If it is mentioned as capacity always consider it as sum (allocated_capacity).

                If the user prompt has a value which is not part of the column names, look for those values from below columns 
                while constructing the SQL where clause with left part as one of these column names and right part as the value:
                    associate_service_area,
                    associate_group,
                    associate_department,
                    associate_section,
                    associate_top_section,
                    associate_business_unit,
                    associate_top_business_unit,
                    sector,
                    gb,
                    planning_gb.

                Following are the sectors:
                    BBE2773,
                    BBG3709,
                    BBI7169,
                    BBM6059,
                    Connec8358,
                    EIGROW6886,
                    GROW5447,
                    Integr7180,
                    Intern4385,
                    NULL9621,
                    OTHERS9975,
                    SDS1525
                    .

                Following are the project_service_areas:
                    BD4871,
                    GS5747,
                    MPS5457,
                    MS8750,
                    NULL9621,
                    SO1995,
                    SX8654,
                    TE-Cor9396
                    .

                Following are the project_sub_service_areas:
                    BD4871,
                    CVS1848,
                    GS5747,
                    ITRAMS7525,
                    MPS5457,
                    MS-ETT1003,
                    MS8750,
                    NULL9621,
                    PS7133,
                    RBEI_C6815,
                    SDS/GP5484,
                    SDS_CO4051,
                    SO1995,
                    SX8654,
                    TE-Cor9396,
                    VM3226
                    .

                To calculate the allocated %, use the calculation below only:
                    1. don't use the billed_capacity and end_capacity for this calculation.
                    2. Allocated % = sum(allocated_capacity)/(sum(allocated_capacity) + sum(vkm_capacity) + sum(ms_capacity) + sum(sl2_capacity))

                To calculate the billing utilization, use the calculation below only:
                    1. Billing Utilization % = sum(billed_capacity)/(sum(allocated_capacity) + sum(vkm_capacity) + sum(ms_capacity) + sum(sl2_capacity))

                 """,
"prompt_prefix_3": """
                You are a seasoned data analyst. 
                You have access to only views, so you must only generate queries that are compatible with these views. 
                Search the custom table metadata to find relevant information. 
                
                use SELECT date_part('month', (SELECT current_timestamp)) to get the current month. 
                
                if this month is mentioned always the year is the current year.
                
                dont use the column attrition_capacity.
                
                if it is capacity always refer to total allocated_capacity.

                If the user prompt has a value which is not part of the column names, look for those values from below columns 
                while constructing the SQL where clause with left part as one of these column names and right part as the value:
                    associate_service_area,
                    associate_group,
                    associate_department,
                    associate_section,
                    associate_top_section,
                    associate_business_unit,
                    associate_top_business_unit,
                    sector,
                    gb,
                    planning_gb,

                BBM6059 is a sector

                To calculate the allocated %, use the calculation below:
                 Allocated % = Sum (allocated_Capacity)/ Sum (allocated_capacity + unallocated_capacity + vkm_capacity + ms_capacity + sl2_capacity)

                Return your final response strictly as a PostgreSQL executable statement (without executing it), in the following format:

                ```sql
                [your PostgreSQL query here]
                ```

                Inference:

                [point 1]
                [point 2] 
                """,

"edited_prompt_prefix": "",

    # "prompt_suffix": """ 
    # Ensure your response is both accurate and comprehensive. 
    # Provide the final answer strictly as a PostgreSQL executable statement using the table metadata. 
    # Do not execute the statement; only present it in the following format:


    # SQL: [your PostgreSQL query here]

    # Inference:

    # [point 1]
    # [point 2] 

    # - In your inference, you may use DQL keywords such as LIMIT and OFFSET to illustrate further detail or reasoning about data retrieval.
    # - No fillers or any other information should be provided.
    # """,
    # "prompt_suffix": """
    #     Ensure your response is both accurate and comprehensive. 
    #     Provide the final answer strictly as a PostgreSQL executable statement using the table metadata.
    #     Present the query in the following format using SQL block syntax:

    #     ```sql
    #     [your PostgreSQL query here]
    #     ```

    #     Inference:

    #     [point 1]
    #     [point 2]

    #     - Use DQL keywords such as LIMIT and OFFSET to further illustrate data retrieval details.
    #     - Ensure the SQL block is formatted to match the following pattern for extraction:

    #     - Wrapped within ```sql``` syntax.
    #     - Includes schema prefixes for all table and join references using the `dhimath_data` schema.
    #     - Avoid providing fillers or additional information.
    # """,

# "prompt_suffix": """
#                     Ensure your responses are thorough, accurate, and directly address the question. 
#                     Give the Final answer as a sql statement only.
#                  """,
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
#Enrich
    "files_dir_path": f"{meta_data_folder}\\data_models\\{user_id}\\Enrich\\",
#Database Connection
    "db_conn" : "",
    "db_details" : {
            'db_type' : "PostgreSQL",
            # 'db_path' : "G:\\DuckDBData\\dhimath",
            'db_name' : 'Dhimath',
            'db_user' :'postgres',
            'db_password' : 'Post1234',
            'db_host' : 'localhost',
            'db_port' : '5432',
            'db_schema_name' : 'dhimath_doc',
            'db_schema_data': 'dhimath_data',
                  },
 
# UI Dropdown Values
    "list_of_llm_models" : [],
    "list_of_embedding_models" : [],
    # Used by Dhimath.Data
    "list_of_domain_tables":["Battery_Dataset","Solar","Wind"],

# Chart Types
    "chart_types" : ["Bar Chart", "Grouped Chart", "Line Chart", "Area Chart", "Scatter Chart", "Pie Chart"]
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
 