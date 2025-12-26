import fitz  #pip install pymupdf
import json
import os
import pandas as pd

from datetime import datetime
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import LlamaCppEmbeddings, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import UnstructuredRTFLoader

from .Load_LLM_Embeddings import Load_embedding_model_Azure_OpenAI
from .Global_Table_Structures import auto_learn_log, knowledge_base, knowledge_base_documents
from .Connect_DB import  db_table_insert, db_table_update

def save_dataframe_to_file(q_and_a_df,global_session_vars):
    # Used in Enrich.py
    q_and_a_df = q_and_a_df.sort_values("question_id")
    
    formatted_data = []
    
    for _, row in q_and_a_df.iterrows():
        formatted_data.append(f"{row['question_id']}. Question: {row['question']}\n")
        # formatted_data.append(f"Answer: {row['answer']}\n\n")
        formatted_data.append(f"   Answer:   {row['answer']}\n\n")
    
    formatted_text = ''.join(formatted_data)
    
    file_name_path = os.path.join(global_session_vars["files_dir_path"], global_session_vars["knowledge_base_name"])
    os.makedirs(file_name_path, exist_ok=True)
    file_name = os.path.join(file_name_path, f"{global_session_vars['knowledge_base_name']}.txt")
    
    with open(file_name, 'w', encoding="utf-8") as txt_file:
        txt_file.write(formatted_text)
    
    #print(f"FAQ file saved at: {file_name}")
    return (file_name_path, file_name)

def text_extraction_in_reading_order(file_path):
    
    doc = fitz.open(file_path)
    extracted_text = []
    pdf_tables = []
    pdf_page_count = len(doc)
    
    for page_num in range(pdf_page_count):
        if page_num == 0:
            prev_page = ""
            curr_page = doc[page_num]
            prev_page_para = ""
            curr_text = curr_page.get_text("text")
            next_page_para = ""
            if pdf_page_count == page_num + 1:
                next_page = ""
            else:
                next_page = doc[page_num+1]
                if len(curr_text) > 0:
                    curr_page_last_char = curr_text.strip()[-1]
                else:
                    curr_page_last_char = ""
                #print(f"Current Page Number - {page_num}")
                #print(f"Last Character in Current Page - {curr_page_last_char}")
                if len(next_page.get_text("blocks")) > 0 and curr_page_last_char != '.' :
                    next_page_blocks = [x[4] for x in  next_page.get_text("blocks")]
                    next_page_para = next_page_blocks[0]
            text = prev_page_para + curr_text + next_page_para
        if page_num > 0 and page_num < pdf_page_count-1:
            prev_page = doc[page_num-1]
            prev_text = prev_page.get_text("text")
            curr_page = doc[page_num]
            next_page = doc[page_num+1]
            prev_page_para = ""
            if len(prev_text) > 0:
                prev_page_last_char = prev_text.strip()[-1]
            else:
                prev_page_last_char = ""
            #print(f"Previous Page Number - {page_num-1}")
            #print(f"Last Character in Previous Page - {prev_page_last_char}")
            if len(prev_page.get_text("blocks"))> 0 and prev_page_last_char != '.':
                prev_page_blocks = [x[4] for x in  prev_page.get_text("blocks")]
                prev_page_para = prev_page_blocks[-1]
            curr_text = curr_page.get_text("text")
            next_page_para = ""
            if len(curr_text) > 0 :
                curr_page_last_char = curr_text.strip()[-1]
            else:
                curr_page_last_char = ""
            #print(f"Current Page Number - {page_num}")
            #print(f"Last Character in Current Page - {curr_page_last_char}")
            if len(next_page.get_text("blocks")) > 0 and curr_page_last_char != '.':
                next_page_blocks = [x[4] for x in  next_page.get_text("blocks")]
                next_page_para = next_page_blocks[0]
            text = prev_page_para + curr_text + next_page_para
        if page_num != 0 and page_num == pdf_page_count-1:
            prev_page = doc[page_num-1]
            prev_text = prev_page.get_text("text")
            curr_page = doc[page_num]
            next_page = ""
            prev_page_para = ""
            if len(prev_text) > 0:
                prev_page_last_char = prev_text.strip()[-1]
            else:
                prev_page_last_char = ""
            #print(f"Previous Page Number - {page_num-1}")
            #print(f"Last Character in Previous Page - {prev_page_last_char}")
            if len(prev_page.get_text("blocks"))> 0 and prev_page_last_char != '.':
                prev_page_blocks = [x[4] for x in  prev_page.get_text("blocks")]
                prev_page_para = prev_page_blocks[-1]
            curr_text = curr_page.get_text("text")
            next_page_para = ""
            text = prev_page_para + curr_text + next_page_para

        #text = ''.join(c for c in text if c.isprintable())
        
        extracted_text.append((text, os.path.basename(file_path), page_num + 1))
 
        page_tables = curr_page.get_text("dict")["blocks"]
        for block in page_tables:
            if "lines" in block:
                pdf_table_data = []
                for line in block["lines"]:
                    row_data = []
                    for span in line["spans"]:
                        row_data.append(span["text"])
                    if row_data:
                        pdf_table_data.append(row_data)
                if pdf_table_data:
                    pdf_tables.append(pd.DataFrame(pdf_table_data))
    doc.close()
    return extracted_text, pdf_tables

def doc_loading(files_dir_path, file):
    documents = []
    file_tables = []
    start_time = datetime.now()
    # print ("PDF Directory Path :", pdf_dir_path)
    # loader = PyPDFDirectoryLoader(pdf_dir_path)
    # data = loader.load_and_split()
    
    # for file in os.listdir(files_dir_path):
    file_name = files_dir_path + f"\\" +file
    #print("Reading :", file_name)
    if file.endswith(".pdf"):
        pdf_text, pdf_tables = text_extraction_in_reading_order(file_name)
        documents.extend(pdf_text)
        file_tables.extend(pdf_tables)
        files_loaded = True
    elif file.endswith('.docx') or file.endswith('.doc'):
        #print("{file} is processed as a pdf. Hence this is ignored")
        loader = Docx2txtLoader(file_name)
        loaded_docs = loader.load_and_split()
        for doc in loaded_docs:
            documents.append((doc.page_content, file, 1))  
        files_loaded = True
    elif file.endswith('.txt'):
        loader = TextLoader(file_name)
        loaded_docs = loader.load_and_split()
        for doc in loaded_docs:
            documents.append((doc.page_content, file, 1))  
        files_loaded = True
    elif file.endswith('.rtf'):
        loader = UnstructuredRTFLoader(file_name, mode="elements", strategy="fast")
        loaded_docs = loader.load_and_split()
        for doc in loaded_docs:
            documents.append((doc.page_content, file, 1))  
        files_loaded = True
    
    doc_loading_time = datetime.now() - start_time

    return documents, file_tables, doc_loading_time

def df_check(df):
    if df is not None and isinstance(df, pd.DataFrame):
        print("Processing DataFrame passed to the function.")
    else:
        df = None
    return df

def doc_processing(documents, knowledge_base_parameters):
    start_time = datetime.now()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=knowledge_base_parameters["chunk_size"],
        chunk_overlap=knowledge_base_parameters["chunk_overlap"]
    )
    text_chunks = []

    for doc in documents:
        if isinstance(doc, tuple):
            page_text, filename, page_no = doc
            chunks = text_splitter.split_text(page_text)
            for chunk in chunks:
                text_chunks.append((chunk, filename, page_no))
        else:
            chunks = text_splitter.split_text(doc.page_content)
            text_chunks.extend(chunks)
    
    doc_processing_time = datetime.now() - start_time
    return text_chunks, doc_processing_time

# def df_processing(df, df_name):
#     text_chunks = []
#     current_chunk = {}
#     count = 0
#     for idx, row in df.iterrows():
#         row_dict = dict(row)
#         # print(row_dict)
#         for key, value in row_dict.items():
#             current_chunk['TABLE NAME'] = f"{df_name}"
#             current_chunk[key] = f"{current_chunk['TABLE NAME']}\n\n {value}"
#             count += 1
#             if count == 5:  
#                 text_chunks.append(current_chunk)
#                 current_chunk = {}
#                 count = 0
#     if current_chunk:
#         text_chunks.append(current_chunk)
#     text_chunks = list(str(chunk) for chunk in text_chunks)
#     return text_chunks

def df_processing(df, df_name,):
    text_chunks = []
    for index, row in df.iterrows():
        chunk = {col: row[col] for col in df.columns}
        ## Table is used for Domainify has to be generalised to any dataframe ##
        formatted_chunk = f"Table: {df_name}\n" + f"\\n".join([f"{key}: {value}\n" for key, value in chunk.items()])
        text_chunks.append(formatted_chunk)
    return text_chunks

def load_embedding_model(emb_file,embedding_name):
    print ("Loading Embedding Model :", embedding_name)
    start_time = datetime.now()
    if  embedding_name in ["OpenAI"]:
        embeddings = OpenAIEmbeddings()
    elif  embedding_name in ["Azure OpenAI"]:
        embeddings = Load_embedding_model_Azure_OpenAI()
        #print ("Azure Open AI Embeddings successfully loaded")
        #print (type(embeddings))
    else:
        embeddings = LlamaCppEmbeddings(model_path=emb_file, verbose=False, n_gpu_layers=-1)
    emb_load_time = datetime.now() - start_time
    return embeddings, emb_load_time

def text_embeddings_creation(text_chunks, embeddings):
    start_time = datetime.now()
    text_embeddings = []

    for chunk, filename, page_no in text_chunks:
        # Add more details of the file in the Chunk 0.. This has to be implemented
        file_name_chunk = f"File Name -- {filename}\\n" + chunk
        embedded_doc = embeddings.embed_documents([file_name_chunk])
        #print(embedded_doc[0])
        metadata = {"Source": f"{filename}", "Page #": f"{page_no}"}
        #text_embeddings.append((f"{filename}, embedded_doc[0] , metadata))
        text_embeddings.append((file_name_chunk, embedded_doc[0], metadata))
    
    text_emb_creation_time = datetime.now() - start_time
    return text_embeddings, text_emb_creation_time

def create_vector_store(vectordb, embeddings, text_embeddings):
    vector_db_creation_status = ""
    vector_store_db = ""
    start_time = datetime.now()
    metadatas = [metadata for _, _, metadata in text_embeddings]
    texts_and_embeddings = [(text, embedding) for text, embedding, _ in text_embeddings]
    if len(texts_and_embeddings) > 0:
        vector_store_db = FAISS.from_embeddings(texts_and_embeddings, embeddings,metadatas)
        vector_store_db.save_local(vectordb)
        vector_db_creation_status = "Success"
    else:
        print("Vector Database not created as the text is empty")
        vector_db_creation_status = "Failure"
   #print("Vector Db Location", vectordb)
    vector_store_time = datetime.now() - start_time
    return vector_store_db, vector_store_time, vector_db_creation_status

def create_vector_store_df(vectordb, text_chunks, embeddings):
    vector_store_db = ""
    vector_store_db = FAISS.from_texts(text_chunks, embeddings)
    vector_store_db.save_local(vectordb)
    vector_store_creation_status = "Success"
    return vector_store_db, vector_store_creation_status

def create_knowledge_base(global_session_vars):  
    user_id = global_session_vars["user_id"]
    user_org = global_session_vars["user_org"]
    db_details = global_session_vars["db_details"]
    process_step = global_session_vars["process_step"]
    start_time = datetime.now()
    file = global_session_vars["file"]
 
    if process_step in ["Auto Learn"]:
        documents, file_tables, doc_loading_time = doc_loading(global_session_vars["uploaded_files_path"], file)
        text_chunks, doc_processing_time = doc_processing(documents, global_session_vars["knowledge_base_parameters"])
        embed, emb_load_time = load_embedding_model(global_session_vars["emb_file"],global_session_vars["embedding_name"])
        text_embeddings, text_emb_creation_time = text_embeddings_creation(text_chunks, embed)
        print(f"Creating the Vector Store : {global_session_vars["vectordb"]}")
        vector_store_db, knowledge_base_creation_time, vector_store_creation_status = create_vector_store(global_session_vars["vectordb"], embed, text_embeddings)
    elif process_step in ["Enrich"]:
        documents, file_tables, doc_loading_time = doc_loading(global_session_vars["files_dir_path"],file)
        text_chunks, doc_processing_time = doc_processing(documents, global_session_vars["knowledge_base_parameters"])
        embed, emb_load_time = load_embedding_model(global_session_vars["emb_file"],global_session_vars["embedding_name"])
        text_embeddings, text_emb_creation_time = text_embeddings_creation(text_chunks, embed)
        vector_store_db, knowledge_base_creation_time, vector_store_creation_status = create_vector_store(global_session_vars["vectordb"], embed, text_embeddings)
    elif process_step in ["Domainify"]:
        # df = df_check(global_session_vars["domainify_df"])
        # text_chunks = df_processing(df, global_session_vars["domainify_file_name"])
        # embed, emb_load_time = load_embedding_model(global_session_vars["emb_file"],global_session_vars["embedding_name"])
        # vector_store_db = create_vector_store_df(global_session_vars["vectordb"], text_chunks, embed)
        print("I'm in df processing")
        df = df_check(global_session_vars["dataframe"])
        text_chunks = df_processing(df, global_session_vars["table_name"])
        embed, emb_load_time = load_embedding_model(global_session_vars["emb_file"],global_session_vars["embedding_name"])
        vector_store_db = create_vector_store_df(global_session_vars["vectordb"], text_chunks, embed)
        vector_store_creation_status = ""

    if vector_store_creation_status == "Success":
        knowledge_base_document_id = save_kb_documents_details(global_session_vars)

    return vector_store_db, vector_store_creation_status

def save_kb_details(global_session_vars):
    db_conn = global_session_vars["db_conn"]    
    user_id = global_session_vars["user_id"]
    user_org = global_session_vars["user_org"]
    db_details = global_session_vars["db_details"]
    
    kb_file_name = global_session_vars["kb_names_file_list"]
    csv_line = {
                'Embedding Name' : [global_session_vars["embedding_name"]], 
                'Knowledge Base' : [global_session_vars["knowledge_base_name"]],
                'Notes' : [global_session_vars["notes"]],
                'Valid': ['Y']
                }
    #print ("The selected Embedding and the Knowledge Base Name are:")
    #print (csv_line)
    df = pd.DataFrame(csv_line)
    df.to_csv(kb_file_name, mode='a', index=False, header=False)
    return None

# if __name__ == "__main__":
#     create_KB()


def save_kb_documents_details(global_session_vars):
    db_conn = global_session_vars["db_conn"] 
    db_details = global_session_vars["db_details"]
    #knowledge_base_documents['knowledge_base_document_id'] 
    knowledge_base_documents['knowledge_base_id'] = [global_session_vars['knowledge_base_id']]
    knowledge_base_documents['knowledge_base_name'] = [global_session_vars['knowledge_base_name']]
    knowledge_base_documents['knowledge_base_file_name'] = [global_session_vars['file']]
    knowledge_base_documents['process_step'] = [global_session_vars['process_step']]
    # knowledge_base_documents['file_size_in_pages'] = global_session_vars['file_size_in_pages']
    # knowledge_base_documents['file_size_in_bytes'] = global_session_vars['file_size_in_bytes']
    # knowledge_base_documents['number_of_chunks'] = global_session_vars['number_of_chunks']
    # knowledge_base_documents['number_of_tables'] = global_session_vars['number_of_tables']
    # knowledge_base_documents['number_of_images'] =  global_session_vars['number_of_images']
    # knowledge_base_documents['document_language'] = global_session_vars['document_language']
    knowledge_base_documents['file_size_in_pages'] = [0]
    knowledge_base_documents['file_size_in_bytes'] = [0]
    knowledge_base_documents['number_of_chunks'] = [0]
    knowledge_base_documents['number_of_tables'] = [0]
    knowledge_base_documents['number_of_images'] =  [0]
    knowledge_base_documents['document_language'] = ['English']
    knowledge_base_documents['file_type'] = [global_session_vars['file'][-3:]]
    knowledge_base_documents['marked_for_deletion'] = ["N"]
    knowledge_base_documents['doc_loading_time_in_secs'] = [0]
    knowledge_base_documents['doc_processing_time_in_secs'] = [0]
    knowledge_base_documents['created_date'] = [datetime.now()]
    knowledge_base_documents['user_id'] = global_session_vars['user_id']
    knowledge_base_documents['user_org'] = global_session_vars['user_org']

    knowledge_base_document_id = db_table_insert(db_details,"knowledge_base_documents",knowledge_base_documents,'knowledge_base_document_id')



    return knowledge_base_document_id

    # text_chunks, doc_processing_time = doc_processing(documents, df, global_session_vars["knowledge_base_parameters"])

# def create_knowledge_base(global_session_vars):
#     process_step = global_session_vars["process_step"]
#     source_selected = global_session_vars["source_selected"]
#     start_time = datetime.now()
#     file = global_session_vars["file"]
#     embed = global_session_vars["embed"]

#     if process_step == "Auto Learn":
#         if source_selected == "Documents":
#             documents, file_tables, doc_loading_time = doc_loading(global_session_vars["uploaded_files_path"], file)
#         elif source_selected == "Data Sheets":
#             documents, file_tables, doc_loading_time = doc_loading(global_session_vars["files_dir_path"], file)    
#     elif process_step == "Enrich":
#         documents, file_tables, doc_loading_time = doc_loading(global_session_vars["files_dir_path"], file)

#     text_chunks, doc_processing_time = doc_processing(documents,global_session_vars["knowledge_base_parameters"])
#     text_embeddings, text_emb_creation_time = text_embeddings_creation(text_chunks, embed)
#     vector_store_db, knowledge_base_creation_time = create_vector_store(global_session_vars["vectordb"], embed, text_embeddings)
    
#     end_time = datetime.now()

#     auto_learn_exec_time = end_time - start_time



    #sys_specs_json = get_sys_specs()
    
    knowledge_base_parameters = json.dumps(global_session_vars["knowledge_base_parameters"])


  
    #auto_learn_log['Auto_Learn_Run_ID'] =
    # auto_learn_log['knowledge_base_id'] = [0]
    # auto_learn_log['knowledge_base_name'] = [global_session_vars["knowledge_base_name"]]
    # auto_learn_log['embedding_id'] = [0]
    # auto_learn_log['embedding_name'] = [global_session_vars["embedding_name"]]
    # auto_learn_log['process_step'] = ['Auto Learn']
    # auto_learn_log['number_of_docs_processed'] = [1]
    # auto_learn_log['run_end_time'] = [end_time]
    # auto_learn_log['process_step'] = ['Auto Learn']
    # auto_learn_log['doc_loading_time_in_secs'] = [doc_loading_time.total_seconds()]
    # auto_learn_log['doc_processing_time_in_secs'] = [doc_processing_time.total_seconds()]
    # auto_learn_log['embedding_load_time_in_secs'] = [emb_load_time.total_seconds()]
    # auto_learn_log['text_emb_creation_time_in_secs'] = [text_emb_creation_time.total_seconds()]
    # auto_learn_log['knowledge_base_creation_time'] = [knowledge_base_creation_time.total_seconds()]
    # auto_learn_log['auto_Learn_total_exec_time_in_secs'] = [auto_learn_exec_time.total_seconds()]
    # auto_learn_log['created_date'] = [datetime.now()]
    # auto_learn_log['user_id'] = [user_id]
    # auto_learn_log['user_org'] = [user_org]

    # print("DB Connection -> Before Inserting Auto Learn Log: ",db_conn , "---")

    # if db_conn == "" or db_conn.closed != 0:
    #     db_conn = db_connect(global_session_vars['db_details'])
    #     global_session_vars['db_conn'] = db_conn
 
    # auto_learn_run_id = db_table_insert(db_details, db_conn,"auto_learn_log",auto_learn_log,'auto_learn_run_id')
    