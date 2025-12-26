import os
import io
import PyPDF2
import json
import uuid
import pandas as pd


from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import AzureChatOpenAI
#from langchain_community.vectorstores import Chroma
from langchain_community.vectorstores import FAISS
#from langchain_openai import OpenAIEmbeddings 
from langchain_openai import AzureOpenAIEmbeddings
#from langchain_community.embeddings import JinaEmbeddings
#from langchain_core.runnables import RunnableLambda, RunnablePassthrough
#from PIL import Image
#from langchain_openai import AzureChatOpenAI
#from langchain_openai import ChatOpenAI
from langchain_text_splitters import CharacterTextSplitter
from unstructured.partition.pdf import partition_pdf # This may become paid...
from datetime import datetime
from langchain_core.documents import Document
from .PDF_Image_Summarize import *
from .Global_Table_Structures import knowledge_base_documents, guided_learn_files
from .Connect_DB import db_table_insert


def extract_pdf_elements(path, fname):
    """
    Extract images, tables, and chunk text from a PDF file.
    path: File path, which is used to dump images (.jpg)
    fname: File name
    """
    return partition_pdf(
        filename=path + fname,
        extract_images_in_pdf=False,
        infer_table_structure=True,
        chunking_strategy="by_title",
        max_characters=4000,
        new_after_n_chars=3800,
        combine_text_under_n_chars=2000,
        image_output_dir_path=path,
    )

# Categorize elements by type
def categorize_elements(raw_pdf_elements, number_of_pdf_pages):
    """
    Categorize extracted elements from a PDF into tables and texts.
    raw_pdf_elements: List of unstructured.documents.elements
    """
    tables = [""]*number_of_pdf_pages
    texts = [""]*number_of_pdf_pages
    for element, page_num in raw_pdf_elements:
        #print("Page_num: ",page_num)
        dict = element.metadata.to_dict()
        if "unstructured.documents.elements.Table" in str(type(element)):
            table_row = [str(element),page_num]
            tables[page_num-1] = tables[page_num-1] + f"\n" + str(element)

        elif "unstructured.documents.elements.CompositeElement" in str(type(element)):
            text_row = [str(element),page_num]
            texts[page_num-1] = texts[page_num-1] + f"\n" + str(element)

    #print("In Composite Element")
    #print (texts)
    #print("In Tables")
    #print (tables)

    return texts, tables


# def multi_modal_rag_chain(model, retriever):
#     """
#     Multi-modal RAG chain
#     """

#     # RAG pipeline
#     chain = (
#         {
#             "context": retriever | RunnableLambda(split_image_text_types),
#             "question": RunnablePassthrough(),
#         }
#         | RunnableLambda(img_prompt_func)
#         | model
#         | StrOutputParser()
#     )

    # return chain


def save_images(images, temp_image_path):
    i = 1
    for img in images:
        img_file = temp_image_path + "img" + str(i) + ".PNG"
        img.save(img_file,format = 'PNG')
        i += 1

# def add_documents(fname, retriever, doc_summaries, doc_contents):
#     id_key = "doc_id"
#     doc_ids = [str(uuid.uuid4()) for _ in doc_contents]
#     summary_docs = [
#         Document(page_content=s, metadata={id_key: doc_ids[i],
#                                            "Source": fname,
#                                            "Page #": s})
#         for i, s in enumerate(doc_summaries)
#     ]
#     retriever.vectorstore.add_documents(summary_docs)
#     retriever.add_documents(summary_docs)
#     retriever.docstore.mset(list(zip(doc_ids, doc_contents)))

#     # Add texts, tables, and images
#     # Check that text_summaries is not empty before adding
#     return retriever

def add_documents_to_vector_store(fname, vector_store, doc_summaries):
    # print("Adding Document Summaries")
    #print(doc_summaries[0])
    #print(doc_summaries[1])
    summary_docs = [
        Document(page_content=s, metadata={"Source": fname,
                                           "Page #": p})
                                    for s, p in [doc_summaries]]
    vector_store.add_documents(summary_docs)

    # Add texts, tables, and images
    # Check that text_summaries is not empty before adding
    return vector_store

def save_image_summaries(image_summaries, image_summary_file_path,pdf_name):
    #print(type(images))
    image_summary_file = pd.DataFrame()
    image_summary_file = image_summaries.copy()
    summary_file_name = image_summary_file_path + f"{pdf_name}_Image_summary.txt"
    image_summary_file.to_csv(summary_file_name, sep='|',  encoding='utf-8', index=False, header=True)

def generate_text_summaries(model, texts, tables, summarize_texts=False):
    """
    Summarize text elements
    texts: List of str
    tables: List of str
    summarize_texts: Bool to summarize texts
    """

    # Prompt
    prompt_text = """You are an assistant tasked with summarizing tables and text for retrieval. \
    These summaries will be embedded and used to retrieve the raw text or table elements. \
    Give a concise summary of the table or text that is well optimized for retrieval. Table or text: {element} """
    prompt = ChatPromptTemplate.from_template(prompt_text)

    # Text summary chain
    # model = ChatOpenAI(temperature=0, model="gpt-4")

    summarize_chain = {"element": lambda x: x} | prompt | model | StrOutputParser()

    # Initialize empty summaries
    text_summaries = []
    table_summaries = []

    # Apply to text if texts are provided and summarization is requested
    if texts and summarize_texts:
        for i in range(len(texts)):
            #print(texts[i])
            text, page_num = texts[i]
            text_summaries.append([summarize_chain.batch(text, {"max_concurrency": 5}), page_num])
    elif texts:
        text_summaries = texts

    # Apply to tables if tables are provided
    if tables:
        for i in range(len(tables)):
            table,page_num = tables[i]
            #print(table)
            #print(page_num)
            table_summaries.append([summarize_chain.batch(table, {"max_concurrency": 5}),page_num])

    return text_summaries, table_summaries


def split_pdf_to_memory(pdf_path):
    pdf_pages = []
    if os.path.isfile(pdf_path):
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page_num in range(len(pdf_reader.pages)):
                pdf_writer = PyPDF2.PdfWriter()
                pdf_writer.add_page(pdf_reader.pages[page_num])
                pdf_page_stream = io.BytesIO()
                pdf_writer.write(pdf_page_stream)
                pdf_page_stream.seek(0)
                pdf_pages.append(pdf_page_stream)
    
    #print(f"The PDF has been split into {len(pdf_pages)} pages.")
    return pdf_pages

# The vectorstore to use to index the summaries
# fpath = "G:\\PDFs\\Stellantis\\"
# fname = "2024 Employee Insurance Benefits Manual.pdf"
# pdf_path = fpath+fname



# model = AzureChatOpenAI(
#         azure_deployment="GPT4o",
#         api_key="da151a3ed5194c77880111ff94c40d4b",
#         model="gpt-4o",
#         api_version="2024-02-01",
#         azure_endpoint="https://icubeai.openai.azure.com/",
#         temperature=0,
#         max_tokens=1024
#     )

# model = ChatOpenAI(temperature=0, model="gpt-4")
def get_text_table_content(global_session_vars):
    #uploaded_files_path = global_session_vars["uploaded_files_path"]
    pdf_path = global_session_vars["pdf_path"]
    pdf_name = global_session_vars["pdf_name"]
    pdf_file_path = global_session_vars["uploaded_files_path"] + pdf_name    
    temp_pdf_path = pdf_path+pdf_name[:-4]+f"\\"

    # print("pdf_file_path   :", pdf_file_path)
    # print("pdf_file_path 1   :",pdf_file_path_1)
    global_session_vars["temp_pdf_path"] = temp_pdf_path

    os.makedirs(temp_pdf_path, exist_ok=True)
    # Get elements
    #print("Get elements")
    st_time = datetime.now()
    #print(st_time)
    raw_pdf_elmnts = []
    pdf_pages = split_pdf_to_memory(pdf_file_path)
    global_session_vars['pdf_pages'] = pdf_pages

    for i, pdf_page in enumerate(pdf_pages):
        with open(f'{temp_pdf_path}{pdf_name[:-4]}_Page_{i+1}.pdf', 'wb') as output_pdf:
            output_pdf.write(pdf_page.read())
            #print(f"Saving File {temp_pdf_path}{pdf_name[:-4]}_Page_{i+1}.pdf")

    raw_pdf_elements = []
    for i, pdf_page in enumerate(pdf_pages):
        raw_pdf = extract_pdf_elements(temp_pdf_path, f"{pdf_name[:-4]}_page_{i+1}.pdf")
        for j in range (len(raw_pdf)):
            raw_pdf_elements.append([raw_pdf[j],i+1])
    #print(raw_pdf_elements)
    # raw_pdf_elements = flatten_extend(raw_pdf_elmnts)
    exec_time = datetime.now() - st_time
    #print(exec_time.total_seconds())

    #print("Get text, tables")
    st_time = datetime.now()
    #print(st_time)
    #texts, tables, loading_time = doc_loading(fpath)
    number_of_pdf_pages = len(pdf_pages)
    #print("Number of PDF Pages", number_of_pdf_pages)
    texts, tables = categorize_elements(raw_pdf_elements, number_of_pdf_pages)
    #print("Total texts: ",len(texts))
    #print("Total Tables:", len(tables))
    exec_time = datetime.now() - st_time
    #print(exec_time.total_seconds())
    return texts, tables

def build_image_summary(model, global_session_vars):
    #pdf_path = global_session_vars["pdf_path"]
    pdf_name = global_session_vars["pdf_name"]
    pdf_file_path = global_session_vars["uploaded_files_path"] + pdf_name
    global_session_vars["pdf_file_path"]=pdf_file_path
    
    image_file_path = global_session_vars["image_file_path"]
    temp_image_path = image_file_path+pdf_name[:-4]+f"\\"
    os.makedirs(temp_image_path, exist_ok=True)

    global_session_vars["temp_image_path"] = temp_image_path
    

    prompt = global_session_vars["prompt"]
    #print("Extract Images from PDF")
    st_time = datetime.now()
    #print(st_time)
    images = extract_images_from_pdf(pdf_file_path)
    global_session_vars["number_of_pages"] = len(images)
    #print("Total Images: ",len(images))
    exec_time = datetime.now() - st_time
    #print(exec_time.total_seconds())
    #print("Temp image Path: ", temp_image_path)
    save_images(images, temp_image_path)

    # Convert images to base64 encoding
    #print("Convert images to base64 encoding")
    st_time = datetime.now()
    #print(st_time)

    images_base64 = [image_to_base64(img) for img in images]
    #print(type(images_base64))
    #print("Total Images: ",len(images_base64))
    exec_time = datetime.now() - st_time
    #print(exec_time.total_seconds())

    #Image summaries
    #print("Image summaries")
    st_time = datetime.now()
    #print(st_time)
    image_summary = generate_img_summaries(model, prompt, images_base64)
    #print(type(image_summary))
    #print("Total Images: ",len(image_summary))
    exec_time = datetime.now() - st_time
    #print(exec_time.total_seconds())
    save_image_summaries(image_summary, temp_image_path, pdf_name[:-4])
    global_session_vars["image_summary"] =  image_summary

    return global_session_vars

def build_text_table_summary(model, global_session_vars):
    texts = global_session_vars["texts"]
    tables = global_session_vars["tables"]
    #print("Character Text Splitter")
    st_time = datetime.now()
    #print(st_time)
    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=4000, chunk_overlap=0
    )
    texts_to_use = [row[0] for row in texts] #getting the first colum

    #print(texts_to_use)
    joined_texts = " ".join(texts_to_use)

    texts_4k_token = text_splitter.split_text(joined_texts)
    #print("Total 4k Text Tokens: ",len(texts_4k_token))
    exec_time = datetime.now() - st_time
    #print(exec_time.total_seconds())

    # Adding 0 as the page number for all the 4k texts. If the answer comes from this chunk, then the page # is set to 0
    texts_4k_with_page_num =[]
    for i in range(len(texts_4k_token)):
        texts_4k_with_page_num.append([texts_4k_token[i],0])

    # Get text, table summaries
    #print("Text and Table summaries")
    st_time = datetime.now()
    #print(st_time)
    text_summaries, table_summaries = generate_text_summaries(
        model, texts_4k_with_page_num, tables, summarize_texts=True
    )
    #print("Total Text Summaries: ",len(text_summaries))
    #print("Total Table Summaries: ",len(table_summaries))
    exec_time = datetime.now() - st_time
    #print(exec_time.total_seconds())
    global_session_vars['text_summary'] = text_summaries    
    global_session_vars['table_summary'] = table_summaries
    return global_session_vars

def build_multimodal_content(global_session_vars):
    model = AzureChatOpenAI(
                    azure_deployment="DhimathAzureOpenAIGPT4o",
                    api_key="196f748a06e6429a95a7c06e0e89bf30",
                    model="gpt-4o",
                    api_version="2024-02-01",
                    azure_endpoint="https://dhimathazureopenaieastus.openai.azure.com/",
                    temperature=0,
                    max_tokens=4096
                )
    text_table_selected = global_session_vars["text_table_selected"]
    #table_selected = global_session_vars["table_selected"]
    slide_summary_selected = global_session_vars["slide_summary_selected"]
    text_table_summary_selected = global_session_vars["text_table_summary_selected"]
    #table_summary_selected = global_session_vars["table_summary_selected"]
    texts =[]
    tables=[]
    image_summary = []
    text_summary = []
    table_summary = []
    if text_table_selected == True:
        global_session_vars['texts'], global_session_vars['tables'] = get_text_table_content(global_session_vars)
    if slide_summary_selected == True:
        global_session_vars = build_image_summary(model, global_session_vars)
    if text_table_summary_selected == True:
        global_session_vars = build_text_table_summary(model, global_session_vars)
    return global_session_vars

def create_multimodal_knowledge_base(global_session_vars):
    texts = global_session_vars['texts']
    tables = global_session_vars['tables']
    text_summary  = global_session_vars['text_summary']
    table_summary  = global_session_vars['table_summary']
    image_summary_df = global_session_vars['image_summary']
    #print("Image Summary df")
    #print(type(image_summary_df))
    image_summary = image_summary_df.values.tolist()
    # print("Image Summary List")
    # print(image_summary)
    pdf_file_path = global_session_vars['pdf_file_path']
    pdf_pages = global_session_vars['pdf_pages']
    pdf_name = global_session_vars['pdf_name']
    number_of_pages = global_session_vars['number_of_pages']
    #print(f"Number of Pages = {number_of_pages}")
    #print("Loading Embedding")
    #load_dotenv()
    start_time = datetime.now()
    # you can pas jina_api_key, if none is passed it will be taken from `JINA_API_TOKEN` environment variable
    #embeddings = JinaEmbeddings(jina_api_key='jina_06548c5e7f2d471b9f2d892b3ab2fab1RIScD8mlFUchecjRbFk1-HXVmq8M', model_name='jina-clip-v1')
    #embeddings = AzureOpenAIEmbeddings(azure_deployment="Dhimath_Text_Embedding",
    #                                         openai_api_version="2023-12-01-preview",
    #                                         )

    embeddings = AzureOpenAIEmbeddings(azure_deployment="DhimathAzureOpenAITextEmbedding3Large",
                            api_key="196f748a06e6429a95a7c06e0e89bf30",
                            model="text-embedding-3-large",
                            #api_version="2023-12-01-preview",
                            azure_endpoint="https://dhimathazureopenaieastus.openai.azure.com/",
                            )

    exec_time = datetime.now() - start_time
    #print(exec_time.total_seconds())

    #print("Embedding-created")

    #print("Saving  Faiss")
    st_time = datetime.now()
    #print(st_time)
    vector_store = FAISS.from_texts([f"{pdf_file_path}\n"], embeddings)
    for i in range(number_of_pages):
        #print(i)
        if texts:
            #print("Texts:")
            #print(texts[i])
            add_documents_to_vector_store(pdf_name, vector_store, [texts[i],i+1])
        # Check that image_summaries is not empty before adding
        if tables:
            #print("Tables:")
            #print(tables)
            add_documents_to_vector_store(pdf_name, vector_store, [tables[i],i+1])
        if image_summary:
            # print("Image Summary:")
            # print(i)
            image_summary[i][0] = f"File Name:  {pdf_name}\nPage Number: {i+1}\n" + image_summary[i][0]
            # print(image_summary[i])
            add_documents_to_vector_store(pdf_name, vector_store, image_summary[i])
        

    if text_summary:
        add_documents_to_vector_store(pdf_name, vector_store, text_summary)
    # # Check that table_summaries is not empty before adding
    if table_summary:
        add_documents_to_vector_store(pdf_name, vector_store, table_summary)


    vectordb = global_session_vars['vectordb']

    vector_store.save_local(vectordb)
    #print(exec_time.total_seconds())
    end_time = datetime.now()

    guided_learn_exec_time = end_time - start_time

    #sys_specs_json = get_sys_specs()
    
    knowledge_base_parameters = json.dumps(global_session_vars["knowledge_base_parameters"])

    guided_learn_files['org_id'] = [global_session_vars['org_id']]
    guided_learn_files['org_user_id'] = [global_session_vars['user_id']]
    guided_learn_files['guided_file_path'] = [global_session_vars['image_file_path']]
    # guided_learn_files['guided_file_name'] = [global_session_vars['pdf_name'].strip('.pdf')]
    guided_learn_files['guided_file_name'] = [global_session_vars['pdf_name'][:-4]]
    guided_learn_files['number_of_pages'] = [global_session_vars['number_of_pages']]
    guided_learn_files['marked_for_deletion'] = ["N"]
    guided_learn_files['created_date'] = [datetime.now()]
    guided_learn_files['user_id'] =  [global_session_vars['user_id']]
    guided_learn_files['user_org'] = [global_session_vars['user_org']]

    # guided_file_name = f".\\Dhimath_doc\\List_of_Guided_Learn_Files.csv"
    # guided_csv_line = {
    #              'File_Name': [global_session_vars['pdf_name'].strip('.pdf')],
    #              'Number_of_Pages': [global_session_vars['number_of_pages']],
    #              'Valid': ['Y'],
    #             #  'user_id': [global_session_vars["user_id"]]
    # }
    # gl_df = pd.DataFrame(guided_csv_line)
    # gl_df.to_csv(guided_file_name, mode='a', index=False, header=False)

    guided_learn_file_id = db_table_insert(global_session_vars['db_details'],"guided_learn_files",guided_learn_files,'guided_learn_file_id')


    # kb_file_name = ".\\Dhimath_doc\\KB_info.csv"
    kb_file_name = ".\\Dhimath_Doc\\KB_info.csv"
    kb_csv_line = {
                'Embedding Name' : [global_session_vars["embedding_name"]], 
                'Knowledge Base' : [global_session_vars["knowledge_base_name"]],
                'Notes': [global_session_vars["knowledge_base_name"]],
                'Valid': ['Y']
                }
    #print ("The selected Embedding and the Knowledge Base Name are:")
    #print (csv_line)
    kb_df = pd.DataFrame(kb_csv_line)
    kb_df.to_csv(kb_file_name, mode='a', index=False, header=False)

    save_guided_learn_kb_documents_details(global_session_vars)

    return vector_store

# # Create retriever
# retriever_multi_vector_img = create_multi_vector_retriever(
#     vectorstore,
#     text_summaries,
#     texts_4k_token,
#     table_summaries,
#     tables,
#     image_summaries,
#     images_base64,
# )


# Create RAG chain
# chain_multimodal_rag = multi_modal_rag_chain(retriever_multi_vector_img)


# # Check retrieval
# query = "Explain briefly about benefits summary"
# docs = retriever_multi_vector_img.invoke(query, limit=6)

# # We get 4 docs
# len(docs)
# print(docs)


# #Check retrieval
# query = "List the documents needed for making a claim"
# # docs = retriever_multi_vector_img.invoke(query, limit=6)

# # # We get 4 docs
# # len(docs)
# docs = chain_multimodal_rag.invoke(query)

# print(docs)

def save_guided_learn_kb_documents_details(global_session_vars):
    db_conn = global_session_vars["db_conn"] 
    db_details = global_session_vars["db_details"]
    #knowledge_base_documents['knowledge_base_document_id'] 
    knowledge_base_documents['knowledge_base_id'] = [global_session_vars['knowledge_base_id']]
    knowledge_base_documents['knowledge_base_name'] = [global_session_vars['knowledge_base_name']]
    knowledge_base_documents['knowledge_base_file_name'] = [global_session_vars['pdf_name']]
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
    knowledge_base_documents['file_type'] = [global_session_vars['pdf_name'][-3:]]
    knowledge_base_documents['marked_for_deletion'] = ["N"]
    knowledge_base_documents['doc_loading_time_in_secs'] = [0]
    knowledge_base_documents['doc_processing_time_in_secs'] = [0]
    knowledge_base_documents['created_date'] = [datetime.now()]
    knowledge_base_documents['user_id'] = global_session_vars['user_id']
    knowledge_base_documents['user_org'] = global_session_vars['user_org']

    knowledge_base_document_id = db_table_insert(db_details,"knowledge_base_documents",knowledge_base_documents,'knowledge_base_document_id')



    return knowledge_base_document_id