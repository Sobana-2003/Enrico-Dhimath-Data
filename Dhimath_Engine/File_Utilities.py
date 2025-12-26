import pandas as pd
import psutil
import os
import json
import shutil
from .Files_Reader import get_all_files_info

def get_sys_specs():
    sys_specs = {
        "cpu": {
            "cpu_count": psutil.cpu_count(),
            "cpu_freq": psutil.cpu_freq().max if psutil.cpu_freq() else None,
            "cpu_load_avg": psutil.cpu_percent(interval=1)
        },
        "ram": {
            "total_ram": psutil.virtual_memory().total,
            "available_ram": psutil.virtual_memory().available
        },
    }
    return json.dumps(sys_specs)

def get_file_size(file_path):
    return os.path.getsize(file_path) if os.path.exists(file_path) else 0

# def file_info(data, file_info_csv_path):
#     if os.path.exists(file_info_csv_path):
#         df = pd.read_csv(file_info_csv_path)
#     else:
#         df = pd.DataFrame(columns=["File_ID", "File_name", "File_dir_name", "File_path", "Emb_name", "Vector_parameters",
#                                    "PDF_processing_time", "Emb_load_time", "Text_emb_creation_time",
#                                    "Vector_store_time", "System_specs", "File_size"])
#     if data['File_name'] in df['File_name'].values:
#         file_id = df[df['File_name'] == data['File_name']]['File_ID'].values[0]
#     else:
#         if df.empty:
#             file_id = 'F001'
#         else:
#             last_id = df['File_ID'].str.extract('F(\d+)').astype(int).max()[0]
#             file_id = f'F{last_id + 1:03d}'
#     data['File_ID'] = file_id
#     new_row = pd.DataFrame([data], columns=df.columns)
#     df = pd.concat([df, new_row], ignore_index=True)
#     df.to_csv(file_info_csv_path, index=False)

def run_logs(data, run_logs_path):
    if not os.path.exists(run_logs_path):
        df = pd.DataFrame(columns=["Timestamp", "Start_time", "End_time", "Execution Time", "Process_step",
                                   "Embedding_ID", "Model_ID", "No of Q's asked", "No of A's asked",
                                   "Vector_Parameters", "LLM_Parameters", "Run_ID"])
    else:
        df = pd.read_csv(run_logs_path)
    new_row = pd.DataFrame([data], columns=df.columns)
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(run_logs_path, index=False)

def output_logs(data, output_logs_path):
    if not os.path.exists(output_logs_path):
        df = pd.DataFrame(columns=["Timestamp", "Start_time", "End_time", "Execution Time", "Process_step",
                                   "Embedding_ID", "Model_ID", "No of Q's asked", "No of A's asked",
                                   "Vector_Parameters", "LLM_Parameters", "Run_ID", "Question", "Answer",
                                   "References"])
    else:
        df = pd.read_csv(output_logs_path)
    new_row = pd.DataFrame([data], columns=df.columns)
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(output_logs_path, index=False)

def move_files_to_target_directory(source_dir, target_dir):
    #print("Target Directory: ", target_dir)
    #print("Source Directory: ", source_dir)
    os.makedirs(target_dir, exist_ok=True)
    file_names = os.listdir(source_dir)
    for file_name in file_names:
        source_file_path = os.path.join(source_dir, file_name)
        target_file_path = os.path.join(target_dir, file_name)
        #print (source_file_path)
        #print (target_file_path)
        shutil.move(source_file_path, target_file_path)

def save_uploaded_file(user_dir, uploaded_file, user_id):
    # print("Saving file to: ", user_dir)
    os.makedirs(user_dir, exist_ok=True)
    saved_files = []
    file_path = os.path.join(user_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        f.close()   
    saved_files.append(uploaded_file.name)
    return saved_files

def load_existing_files_info(user_dir):
    if os.path.exists(user_dir):
        files_info_df = get_all_files_info(user_dir,"")
    else:
        files_info_df = pd.DataFrame(columns=["File Name", "Pages / Chars", "Count", "Count Type"])
    return  files_info_df


def create_user_directories(files_path, user_id):
    user_files_path = files_path + user_id
    os.makedirs(user_files_path, exist_ok=True)

    uploaded_files_path = user_files_path+f"\\Uploaded_Files\\"
    os.makedirs(uploaded_files_path, exist_ok=True)
    
    pdf_path = user_files_path+f"\\PDF_Pages\\"
    os.makedirs(pdf_path, exist_ok=True)
    
    image_file_path = user_files_path+f"\\PDF_Images\\"
    os.makedirs(image_file_path, exist_ok=True)
    
    return user_files_path, uploaded_files_path,pdf_path, image_file_path


def save_uploaded_files(user_dir, uploaded_files, user_id):
    os.makedirs(user_dir, exist_ok=True)
    saved_files = []
    for uploaded_file in uploaded_files:
        file_path = os.path.join(user_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            f.close()
        saved_files.append(uploaded_file.name)
    #convert_docx_to_pdf(user_dir)
    return saved_files

def delete_uploaded_files(user_dir, uploaded_files, user_id):
    for uploaded_file in uploaded_files:
        delete_file = os.path.join(user_dir, uploaded_file.name)
        #print("Deleting File", delete_file)
        if os.path.isfile(delete_file):
            os.remove(delete_file)
    return

def delete_existing_files(user_dir, existing_files, user_id):
    for uploaded_file in existing_files:
        delete_file = os.path.join(user_dir, uploaded_file)
        #print("Deleting File", delete_file)
        if os.path.isfile(delete_file):
            os.remove(delete_file)
    return

def delete_uploaded_file(user_dir, uploaded_files, user_id):
    #print(uploaded_files)
    if uploaded_files:
        delete_file = os.path.join(user_dir, uploaded_files.name)
        #print("Deleting File", delete_file)
        if os.path.isfile(delete_file):
            os.remove(delete_file)
    return

def delete_existing_file(user_dir, uploaded_files, user_id):
    #print([uploaded_files[0]][0])
    if uploaded_files:
        delete_file = os.path.join(user_dir, [uploaded_files[0]][0])
        #print("Deleting File", delete_file)
        if os.path.isfile(delete_file):
            os.remove(delete_file)
    return


def load_existing_files_info(user_dir):
    # user_dir = f"H:\\Python Code\\Stream_Lit_Apps\\Dhimath_App\\{user_id}\\Data"
    if os.path.exists(user_dir):
        files_info_df = get_all_files_info(user_dir,"")
    else:
        files_info_df = pd.DataFrame(columns=["File Name", "Pages / Chars", "Count", "Count Type"])
    return  files_info_df


def save_q_a_dataframe_to_file(q_and_a_df, global_session_vars):
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
    
    with open(file_name, 'w', encoding="utf-8") as f:
        f.write(formatted_text)
    
    #print(f"FAQ file saved at: {file_name}")
    return (file_name_path, file_name)

def save_dataframe_to_file(df, global_session_vars): 
    df_to_dict = df.to_dict('index')
    formatted_data = []  
    #print(len(df_to_dict))
    for i in range(len(df_to_dict)):
        formatted_data.append(df_to_dict[i])
    #print(formatted_data)
 
    file_name_path = os.path.join(global_session_vars["files_dir_path"], global_session_vars["knowledge_base_name"])
    print("path:",file_name_path)
    os.makedirs(file_name_path, exist_ok=True)
    file_name = os.path.join(file_name_path, f"{global_session_vars['knowledge_base_name']}.txt")
    
    with open(file_name, 'w', encoding="utf-8") as f:
        f.write(json.dumps(formatted_data))
    
    #print(f"Data file saved as a dictionary: {file_name}")
    return (file_name_path, file_name)

# def save_dataframe_to_file(q_and_a_df,global_session_vars):
#     # Used in Enrich.py
#     # print(q_and_a_df)
#     q_and_a_df['question_text'] = 'Question'
#     q_and_a_df['answer_text'] = 'Answer'
#     q_df = q_and_a_df[["question_id", "question_text", "question"]]
#     q_df = q_df.rename(columns={"question_text": "Q/A", "question": "Question/Answer"})
#     a_df = q_and_a_df[["question_id", "answer_text", "answer"]]
#     a_df = a_df.rename(columns={"answer_text": "Q/A", "answer": "Question/Answer"})
#     merged_df = q_df._append(a_df)
#     merged_df = merged_df.sort_values(["question_id", "Q/A"], ascending=[True, False])
#     # open('./temp.txt', 'w', encoding='utf-8').write(merged_df.to_string(header=False, index=False))
#     # df_string = merged_df.to_string(header=False, index=False, path_or_buf='.//temp.txt')
#     # print(f"Hellooooooooooooo{df_string}")
#     # file_name_path = global_session_vars["files_dir_path"]+ "//" + global_session_vars["knowledge_base_name"]
#     # isExist = os.path.exists(file_name_path)
#     # if not isExist:
#     #     # Create a new directory because it does not exist
#     #     os.makedirs(file_name_path, exist_ok=True)
#     # file_name = file_name_path + '//' + global_session_vars["knowledge_base_name"] + ".txt"
#     file_name_path = os.path.join(global_session_vars["files_dir_path"], global_session_vars["knowledge_base_name"])
#     os.makedirs(file_name_path, exist_ok=True)
#     file_name = os.path.join(file_name_path, f"{global_session_vars['knowledge_base_name']}.txt")
#     print(file_name)
#     with open(file_name, 'a', encoding="utf-8") as f:
#         f.write(merged_df.to_string(header=False, index=False))
#     f.close()
#     print(f"I am here {file_name_path}, {file_name}")
#     return (file_name_path, file_name)
