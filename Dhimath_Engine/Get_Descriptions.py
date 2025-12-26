from .Get_Answers import manual_input
import pandas as pd
import streamlit as st

def summarize_csv(file_path):
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)
    #print(df.head())
    # Get column names
    column_names = df.columns
    # Data summary
    summary = []
    # Iterate over each column
    for col in column_names:
        data_type = df[col].dtype  # Get the data type of the column   
        if pd.api.types.is_numeric_dtype(df[col]):
            min_value = df[col].min()  # Get min value if numeric
            max_value = df[col].max()  # Get max value if numeric
        else:
            max_len = 0
            min_len = 0
            min_value = f"Len : {min_len}"
            max_value = f"Len : {max_len}"   
        summary.append({
            'Column Name': col,
            'Data Type': data_type,
            'Min Value': min_value,
            'Max Value': max_value
        })
    # Convert to DataFrame for better readability
    summary_df = pd.DataFrame(summary)
    number_of_rows = len(df)
    number_of_columns = len(df.columns)
    return summary_df, number_of_rows, number_of_columns

def summarise_df(global_session_vars):
    df = global_session_vars["dataframe"]
    column_names = df.columns
    summary = []
    for col in column_names:
        data_type = df[col].dtype    
        if pd.api.types.is_numeric_dtype(df[col]):
            min_value = df[col].min()  
            max_value = df[col].max()
        else:
            max_len = 0
            min_len = 0
            min_value = f"Len : {min_len}"
            max_value = f"Len : {max_len}"   
        summary.append({
            'Column_Name': col,
            'Data_Type': data_type,
            'Min_Value': min_value,
            'Max_Value': max_value
        })
    summary_df = pd.DataFrame(summary)
    number_of_rows = len(df)
    number_of_columns = len(df.columns)
    return summary_df, number_of_rows, number_of_columns

def parse_answer(answer):
    parts = answer.split('\n\n')
    short_desc = parts[0] if len(parts) > 0 else ""
    short_desc = short_desc.replace("Short description:", "")
    long_desc = parts[1] if len (parts) > 1 else ""
    long_desc = long_desc.replace("Long description:", "")
    return short_desc, long_desc

def download_descriptions(df):
    content = ""
    for _, row in df.iterrows():
        content += f"Column_Name: {row['Column_Name']}\n"
        content += f"Data_Type: {row.get('Data_Type', 'N/A')}\n"
        content += f"Min Value: {row['Min Value']}\n"
        content += f"Max Value: {row['Max Value']}\n"
        content += f"Short Description: {row['Short Description']}\n"
        content += f"Long Description: {row['Long Description']}\n\n"
    return content

def process_row_and_generate_descriptions(column_name, domain_name, global_session_vars):
    # st.session_state.session_vars["question"] = \
    # f"Please analyze the provided knowledge base and generate both a concise short description " + \
    # f"and a comprehensive long description for the '{column_name}'. The short description " + \
    # f"should capture the essential meaning in a brief and clear manner, while the long " + \
    # f"description should provide a detailed and thorough explanation, covering all relevant " + \
    # f"aspects and context. Ensure that both descriptions are meaningful, accurate, and directly " + \
    # f"related to the content of the '{column_name}'. Pay close attention to any nuances or " + \
    # f"specific details mentioned in the knowledge base to maintain accuracy and relevance."
    global_session_vars["question"] = \
    f"Generate both a concise short description " + \
    f"and a comprehensive long description for the '{column_name}' in the context of the domain {domain_name}. The short description " + \
    f"should capture the essential meaning in a brief and clear manner, while the long " + \
    f"description should provide a detailed and thorough explanation, covering all relevant " + \
    f"aspects and context. Ensure that both descriptions are meaningful, accurate, and directly " + \
    f"related to the content of the '{column_name}'. Pay close attention to any nuances or " + \
    f"specific details mentioned in the knowledge base to maintain accuracy and relevance."
    answer = ""
    answer, question_ID, _, qa_exec_time, metadata = manual_input(global_session_vars)
    short_desc, long_desc = parse_answer(answer)
    return short_desc, long_desc


def process_df_and_generate_descriptions(df, domain_name, global_session_vars):
    for index, row in df.iterrows():
        short_desc, long_desc =process_row_and_generate_descriptions(row, domain_name, global_session_vars)
     
    return df

def process_csv_and_generate_descriptions(file_path, file, global_session_vars):
    # try:
    file_with_path = f"{file_path}\\{file}"
    df, number_of_rows, number_of_columns = summarize_csv(file_with_path)
    process_df_and_generate_descriptions(df,global_session_vars)
    # except Exception as e:
    #     st.error(f"Error reading CSV file: {e}")
    #     return None
    return df