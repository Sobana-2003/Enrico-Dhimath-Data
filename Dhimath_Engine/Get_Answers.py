from datetime import datetime

from .Global_Table_Structures import q_and_a_log
from .Connect_DB import db_table_insert, db_table_update, db_connect

def get_answer(question,qa_on, qa_off, restricted_scope_on, chat_history, process_step):
    metadata = []
    answer = ""
    #print("Chat History", chat_history)
    #print(knowledge_base)
    if restricted_scope_on and qa_on != None:
        result = qa_on.invoke({'question': question, 'chat_history': chat_history})
        answer = result["answer"]
        if hasattr(qa_on,'retriever'):
            #print("Retrieved Documents:")
            for doc in qa_on.retriever.invoke(question):
                #print(question)
                #print(doc)
                doc_metadata = doc.metadata
                if doc_metadata:
                    #print("Metadata:", doc_metadata)
                    metadata.append(doc_metadata)
        else:
            print("No metadata available.")
    else:
        #docs = knowledge_base.similarity_search(question)
        docs = []
        #print(docs)
        #print("4 : I am in Qa_off", datetime.now())
        #answer = qa_off.run(input_documents = docs, question = question)  
        answer = qa_off.invoke(question)  
        #print("5 :", datetime.now())


    return answer, metadata


def manual_input(global_session_vars):
    session_q_id = global_session_vars["session_q_id"]
    db_details = global_session_vars["db_details"]
    db_conn = global_session_vars["db_conn"]
    question = global_session_vars["question"]
    qa_on = global_session_vars["qa_on"]
    qa_off = global_session_vars["qa_off"]
    embedding_name = global_session_vars["embedding_name"]
    knowledge_base = global_session_vars["knowledge_base"]
    knowledge_base_name = global_session_vars["knowledge_base_name"]
    selected_llm = global_session_vars["selected_llm"]
    process_step = global_session_vars["process_step"]
    restricted_scope_on = global_session_vars["restricted_scope"]
    user_id = global_session_vars["user_id"]
    chat_history = global_session_vars["chat_history"]
    user_org = global_session_vars["user_org"]
    results = []
    logs = []
    start_time = datetime.now()
    #print(question)
    # print("2 :", datetime.now())
    # print("Knowledge Base")
    # print(knowledge_base)
    # # print("Q A")
    # print(qa)
    answer, metadata = get_answer(question, qa_on, qa_off, restricted_scope_on, chat_history, process_step)  
    # print("6 :", datetime.now())
    # print(answer)
    end_time = datetime.now()
    qa_exec_time = end_time - start_time

    q_and_a_log['session_q_id'] = [session_q_id]
    q_and_a_log['question'] = [question]
    q_and_a_log['edited_question'] = [question]
    q_and_a_log['answer'] = [answer]
    q_and_a_log['edited_answer'] = [answer]
    q_and_a_log['doc_references'] = [metadata]
    q_and_a_log['answer_correctness'] = ['Yes']
    q_and_a_log['process_step'] = [process_step]
    q_and_a_log['embedding_id'] = [embedding_name]
    q_and_a_log['embedding_name'] = [embedding_name]
    q_and_a_log['llm_id'] = [selected_llm]
    q_and_a_log['llm_name'] = [selected_llm]
    q_and_a_log['llm_parameters'] = ['']
    q_and_a_log['knowledge_base_id'] = ['']
    q_and_a_log['knowledge_base_name'] = [knowledge_base_name]
    q_and_a_log['knowledge_base_parameters'] = ['']
    q_and_a_log['response_start_time'] = [start_time]
    q_and_a_log['response_end_time'] = [end_time]
    q_and_a_log['answer_response_time'] = [qa_exec_time.total_seconds()]
    q_and_a_log['created_date'] = [datetime.now()]
    q_and_a_log['user_id'] = [user_id]
    q_and_a_log['user_org'] = [user_org]
    
    #print(q_and_a_log)
    question_id = db_table_insert(db_details,"q_and_a_log",q_and_a_log, "question_id")
    #print (question_id)

    # append_result(results, logs, user_input, answer, start_time, end_time, num_questions, num_answers, metadata)
    return answer, question_id, logs, qa_exec_time, metadata


def update_q_a_log(global_session_vars, db_column_name, db_column_value):
    db_details = global_session_vars["db_details"]
    db_conn = global_session_vars["db_conn"]
    user_id = global_session_vars["user_id"]
    question_id = global_session_vars["question_id"]
    if db_conn == "" or db_conn.closed != 0:
        db_conn = db_connect(global_session_vars['db_details'])
        global_session_vars['db_conn'] = db_conn
    db_table_update(db_details, db_conn, "q_and_a_log","question_id",question_id, db_column_name, db_column_value, user_id)   