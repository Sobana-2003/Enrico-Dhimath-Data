import pandas as pd
from . import Connect_DB as conn_DB

def get_emb_name(selected_kbs, global_session_variables):
    # usecols = ["Embedding_Name", "Knowledge_Base_Name"]
    # df = pd.read_csv(global_session_variables["kb_names_file_list"], usecols = usecols )
    sql_Query = f'SELECT embedding_name, knowledge_base_name FROM dhimath_doc.knowledge_base'
    df = conn_DB.db_get_data(global_session_variables['db_details'],sql_Query)
    emb_used = []
    #print(selected_kbs)
    for index, selected_kb in enumerate(selected_kbs):
        #print(index)
        #print(selected_kb)
        r_df = df[df['knowledge_base_name']==selected_kb]
        emb_used.append(r_df['embedding_name'].values[0])
        # print("Embedding Used : ", r_df['Emb_name'].values[0])
    #print ("Associated Embeddings")
    #print (emb_used)
    return emb_used

def load_all_global_variables(global_session_variables):
    # usecols = ["ID", "LLM_Name", "Valid", "Default"]
    # df = pd.read_csv(global_session_variables["llm_file_list"], usecols = usecols )
    # r_df = df[df['Valid']=="Y"]
    # r_df = r_df.sort_values(["Default","LLM_Name"], ascending=[False, True])
    
    sql_Query = "SELECT llm_emb_id, llm_emb_name, marked_for_deletion, llm_emb_default from dhimath_doc.llm_and_embeddings where llm_emb = 'LLM' order by llm_emb_default, llm_emb_name"
    r_df = conn_DB.db_get_data(global_session_variables['db_details'], sql_Query)
    global_session_variables["list_of_llm_models"] = r_df['llm_emb_name'].tolist()

    # usecols = ["ID", "Embedding_Name", "Valid"]
    # df = pd.read_csv(global_session_variables["emb_names_file_list"], usecols = usecols )
    # r_df = df[df['Valid']=="Y"]
    
    sql_Query = "SELECT llm_emb_id, llm_emb_name, marked_for_deletion, llm_emb_default from dhimath_doc.llm_and_embeddings where llm_emb = 'Embedding' order by llm_emb_default DESC, llm_emb_name"
    r_df = conn_DB.db_get_data(global_session_variables['db_details'], sql_Query)
    global_session_variables["list_of_embedding_models"] = r_df['llm_emb_name'].tolist()

    # usecols = ["Embedding_Name", "Knowledge_Base_Name", "Notes", "Valid"]
    # df = pd.read_csv(global_session_variables["kb_names_file_list"], usecols = usecols )
    # r_df = df[df['Valid']=="Y"]
    # r_df = r_df.sort_values("Knowledge_Base_Name")
    # global_session_variables["list_of_knowledge_bases"] = r_df["Knowledge_Base_Name"].tolist()


    # usecols = ["File_Name", "Number_of_Pages", "Valid"]
    # df = pd.read_csv(global_session_variables["guided_learn_file_list"], usecols = usecols )
    # r_df = df[df['Valid']=="Y"]
    # r_df = r_df.sort_values("File_Name")
    # global_session_variables["list_of_guided_learn_files"] = r_df["File_Name"].tolist()


    # print("Embedding Models")
    # print(List_of_Embedding_Models)

    # print("LLMs")
    # print(List_of_LLM_models)

    # print("Knowledge Bases")
    # print(List_of_Knowledge_Bases)

    return global_session_variables
