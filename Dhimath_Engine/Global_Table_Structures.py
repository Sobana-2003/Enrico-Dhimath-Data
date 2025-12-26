from datetime import datetime 

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
'user_id' : ["Prasanna"],
'user_org' : ["GreyWiz"]
}

knowledge_base = {
#'knowledge_base_id' : [0],
'org_id' : [0],
'knowledge_base_name' : [0],
'knowledge_base_path' : [""],
'embedding_id' : [0],
'embedding_name' : [""],
'embedding_layers' : [0],
'number_of_objects' : [0],
'vector_db_type' : ["FAISS"],
'marked_for_deletion' : ["N"],
'created_date' : [datetime.now()],
'updated_date' : [datetime.now()],
'user_id' : [""],
'user_org' : [""]
}

knowledge_base_documents = {
#'knowledge_base_document_id' : [0],
'org_id' : [0],
'knowledge_base_id' : [0],
'knowledge_base_name' : [""],
'knowledge_base_file_name' : [""],
'source_type' : ["Document"],
'process_step' : [""],
'file_size_in_pages' : [0],
'file_size_in_bytes' : [0],
'number_of_chunks' : [0],
'number_of_tables' : [0],
'number_of_images' : [0],
'document_language' : ["English"],
'file_type' : ["PDF"],
'chunk_size' : [0],
'chunk_overlap' : [0],
'text_splitter_type' : [""],
'notes' : [""],
'document_merge_order' : [0],
'marked_for_deletion' : [""],
'doc_loading_time_in_secs' : [0.0],
'doc_processing_time_in_secs' : [0.0],
'created_date' : [datetime.now()],
'user_id' : [""],
'user_org' : [""],
}



document_info = {
#'document_id' : [0],
'knowledge_base_name' : [""],
'knowledge_base_path' : [""],
'embedding_name' : [""],
'llm_name' : [""],
'image_file_path' : [""],
'image_name' : [""],
'pdf_page_number' : [0],
'pdf_file_path' : [""],
'pdf_file_name' : [""],
'image_description_from_llm' : [""],
'text_content' : [""],
'text_summary' : [""],
'table_content' : [""],
'table_summary' : [""],
'image_summary_execution_time' : [0],
'text_summary_execution_time' : [0],
'table_summary_execution_time' : [0],
'document_meta_data' : [0],
'created_date' : [datetime.now()],
'user_id' : [""],
'user_org' : [""],
}


org = {
#'org_id' : [0],
'org_name' : [""],
'credit_type' : [0],
'credits_purchased' : [0],
'credits_used' : [0],
'credits_balance' : [0],
'number_of_users' : [0],
'number_of_knowledge_bases' : [0],
'number_of_roles' : [0],
'marked_for_deletion' : ["N"],
'created_date' : [datetime.now()],
'user_id' : [""],
'user_org' : [""],
}


org_roles = {
#'org_role_id' : [0],
'org_id' : [0],
'org_role_name' : [0],
'marked_for_deletion' : ["N"],
'created_date' : [datetime.now()],
'user_id' : [""],
'user_org' : [""],
}


org_users = {
#'org_user_id' : [0],
'org_id' : [0],
'org_user_name' : [""],
'org_user_password':[""],
'org_user_department' : [""],
'org_user_location' : [""],
'marked_for_deletion' : ["N"],
'created_date' : [datetime.now()],
'user_id' : [""],
'user_org' : [""],
}


org_roles_users = {
#'org_roles_users_id' : [0],
'org_id' : [0],
'org_role_id' : [""],
'org_user_id' : [""],
'org_role_user_access_level' : [""],
'marked_for_deletion' : ["N"],
'created_date' : [datetime.now()],
'user_id' : [""],
'user_org' : [""],
}

knowledge_base_roles_access = {
#'knowledge_base_role_access_id' : [0],
'org_id' : [0],
'org_role_id' : [""],
'knowledge_base_id' : [""],
'knowedge_base_role_access_level' : [""],
'marked_for_deletion' : ["N"],
'created_date' : [datetime.now()],
'user_id' : [""],
'user_org' : [""],
}

llm_and_embeddings = {
#'llm_emb_id' : [0],
'org_id' : [0],
'llm_emb' : [""],
'llm_emb_name' : [""],
'llm_emb_type' : [""],
'deployment_name' : [""],
'api_key' : [""],
'api_version' : [""],
'llm_emb_gguf_path' : [""],
'llm_emb_gguf_name' : [""],
'marked_for_deletion' : ["N"],
'created_date' : [datetime.now()],
'user_id' : [""],
'user_org' : [""]
}

guided_learn_files = {
#'guided_learn_file_id' : [0],
'org_id' : [0],
'org_user_id' : [""],
'guided_file_path' : [""],
'guided_file_name' : [""],
'number_of_pages' : [0],
'marked_for_deletion' : [""],
'created_date' : [datetime.now()],
'user_id' : [""],
'user_org' : [""],
}
