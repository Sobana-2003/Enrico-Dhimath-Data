import streamlit as st
from Dhimath_Engine import File_Utilities as file_utils 
import pandas as pd


def process_file(file_types, existing_files_info, uploaded_files_path, user_id, process_file_clicked):
    upload_container = st.container(border=True)
    with upload_container:
        uploaded_file = st.file_uploader(":blue[Upload File(s)]", accept_multiple_files=False, type = file_types)
        file_c1, file_c2, file_c3 = st.columns([50,45,5]) 
        with file_c1:
            if uploaded_file:
                process_file_clicked = st.button("Process File(s)", type="primary", use_container_width = True)
                if process_file_clicked and uploaded_file:   
                    new_files = file_utils.save_uploaded_file(uploaded_files_path, uploaded_file, user_id)
                    new_files_info = file_utils.get_all_files_info(uploaded_files_path, new_files)
                    existing_files_info = pd.concat([existing_files_info, new_files_info]).drop_duplicates(subset="File Name").reset_index(drop=True)
    
                    upload_container.success(f"File uploaded")
        with file_c2:
            if len(existing_files_info)>0 or uploaded_file:
                clear_files = st.button("Clear Files",  use_container_width = True)
                if clear_files:
                    # st.write(uploaded_files_path)
                    # st.write(uploaded_files)
                    # st.write(st.session_state.session_vars['existing_files_info']['Full_file_name'])
                    existing_file_list=[]
                    for existing_file in st.session_state.session_vars['existing_files_info']['Full_file_name']:
                        existing_file_list.append(existing_file)
                    # st.write(existing_file_list)
                    file_utils.delete_uploaded_files(uploaded_files_path, uploaded_file, user_id)
                    file_utils.delete_existing_files(uploaded_files_path, existing_file_list, user_id)
                    existing_files_info = []
    return existing_files_info, uploaded_file, process_file_clicked