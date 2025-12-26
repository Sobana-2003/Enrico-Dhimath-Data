import pandas as pd
from dotenv import load_dotenv
from datetime import datetime

# print("loading start time:", datetime.now())
load_dotenv()

List_of_Vector_DB_types = ["FAISS",
                      "Chroma"]

List_of_text_splitter_types = ["Recursive Character",
                               "Character",
                               "NLTK(TBD)",
                               "Spacy(TBD)"]

temperature_list = [item/100 for item in range(0, 100, 5)]
search_iteration_list = [item for item in range(1,1000,1)]

meta_data_folder = f"D:\\Dhimath\\dhimath-doc-streamlit-main\\Dhimath_Files"
csv_dir = f"{meta_data_folder}\\Dhimath_Doc\\QA_Files\\"

user_id = ""

global_session_variables = {
#Dhimath_Doc_variables
    "version" : "2.0",
    "user_name" : "Prasanna",
    "user_id" : "Prasanna",
    "user_password" : "",
    "org_id" : "",
    "org_role_id": "",
    "user_org" : "GreyWiz",
    # "tab" : "tab1",
    "process_step" : "",
    "selected_tool_option" : "",
    "valid_user": False,
#vector DB:
    "knowledge_base_path" : f"{meta_data_folder}\\VectorDB\\",
    #vectordb - vector_db_path + \\ + knowledge_base_name
    "vectordb": "",
    "vector_store_db" : "",
#llm,
    "selected_llm" : "",
    "selected_temp" : 0.0,
    "selected_s_kwargs" : 1,
    "llm" : "",
    "llm_file": "",
    "llm_path": "D:\\Dhimath\\Local_models\\",
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
    "emb_path": "D:\\LLM Models\\",
#Knowledge Base    
    "selected_kb" : [],
    "selected_kb_file": "",
    "knowledge_base" : "",
    "knowledge_base_name": "",
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
    "target_path": f"{meta_data_folder}\\Knowledge_base_documents\\",
    "user_files_path": "",  
    "uploaded_files_path" : "", 
#Guided Learn
    "pdf_name": "",
    "pdf_page": "",
    "pdf_pages": "",
    #the PDF is split by page and saved as separate document pdf file to get the page # for texts and tables.
    "pdf_path": f"{meta_data_folder}\\{user_id}\\PDF_Pages\\",
    #This stores the pdf_path + pdf_name contactenated
    "pdf_file_path" : "",
    #the PDF is split by page and saved as separate image to get the page level image summary.
    "image_file_path" : f"{meta_data_folder}\\{user_id}\\PDF_Images\\",
    "number_of_pages" : 1,
    "temp_pdf_path": "",
    "temp_image_path" :"",
    "texts":[],
    "tables":[],
    "image_summary":pd.DataFrame(columns=['Slide_Summary','Slide_Number']),
    "text_summary":[],
    "table_summary":[],
    "text_table_selected": True,
    # "table_selected": True,
    "slide_summary_selected" : True,
    "text_table_summary_selected" : False,
    #"table_summary_selected" : False,
    "prompt" : """You are an assistant tasked with elaborating the text contents of the images for retrieval. \
    These detailed text contents will be embedded and used to retrieve the raw image. \
    Give details of the image that is well optimized for retrieval.""",
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
#Coach
    "num_questions" : 10,
    "auto_qa_df": pd.DataFrame(columns=[
            'ID', 'Question', 'Edited_Questions',  
            'Answers', 'Edited_Answers' , 'Metadata'
        ]),
 
#Enrich
    "enrich_files_path": f"{meta_data_folder}\\{user_id}\\Enrich\\",

#Manage KBs:
    "doc_save_clicked" : False,
    "doc_valid" : "N",
    "doc_id" : None,
    "kb_id" : None,
    "kb_name" : "",
    "kb_search_clicked" : False,
    "kb_save_clicked" : False,
    "kb_valid": "N",
    "idx": 0,
    "d_idx" : 0,    
#Tools
    "kb_file_clicked" : False,
#Database Connection
    "db_conn" : "",
    "db_details" : {
            'db_type' : "PostGreSQL",
            'db_path' : "G:\\DuckDBData\\dhimath",
            'db_name' : 'Dhimath_Streamlit',
            'db_user' :'postgres',
            'db_password' : 'sobana',
            'db_host' : 'localhost',
            'db_port' : '5432',
            'db_schema_name' : 'dhimath_doc'
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
    "kb_names_file_list": f"{meta_data_folder}\\{user_id}\\kb_info.csv",
    "emb_names_file_list": f"{meta_data_folder}\\{user_id}\\List_of_Embeddings.csv",
    "llm_file_list" : f"{meta_data_folder}\\{user_id}\\List_of_LLMs.csv",
    "guided_learn_file_list" :f"{meta_data_folder}\\{user_id}\\List_of_Guided_Learn_Files.csv"
    }

# print("loading End time:", datetime.now())