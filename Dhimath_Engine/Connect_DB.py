import os
#import datatable as dt
import duckdb
import pandas as pd
#import pandas.io.sql as psql
import psycopg2 as pg
import json
from Dhimath_Engine import Global_Table_Structures as gbl_tbls
from Dhimath_Engine import Global_Variables as gbl_vars
from sqlalchemy import create_engine
# import streamlit as st

# db_details = {
# #PostGreSQL
#  "user" : 'postgres',
#  "password" : 'Post1234',
#  "host" : 'localhost',
#  "port" : '5432',
#  "database" : 'TrueMede',
#  "schema_name": 'truemede_app'
# }

def db_connect_sql_alchemy(db_details):
    connect = "postgresql+psycopg2://%s:%s@%s:%s/%s" %(
                db_details['db_user'],
                db_details['db_password'],
                db_details['db_host'],
                db_details['db_port'],
                db_details['db_name']
                 )
    conn = create_engine(connect)
    return conn


from datetime import datetime

#DuckDB
# db_path = "G:\\DuckDBData\\dhimath"
# db_schema_name = "Dhimath_LLM"

#PostGreSQL
# db_name = 'Dhimath'
# db_user = 'postgres'
# db_password = 'Post1234'
# db_host = 'localhost'
# db_port = '5432'

def db_connect(db_details):
    #print("Connecting to Database ", db_details['db_type'])
    if db_details['db_type'] == "Duck DB":
        db_conn = duckdb.connect(db_details['db_path'])
    elif db_details['db_type'] == "SQL Lite":
        #change the connection details below for SQL Lite.
        db_conn = duckdb.connect(db_details['db_path'])
    elif db_details['db_type'] == "PostGreSQL":
        db_conn = pg.connect(database=db_details["db_name"],
                        host=db_details["db_host"],
                        user=db_details["db_user"],
                        password=db_details["db_password"],
                        port=db_details["db_port"])
    return db_conn

def db_table_insert(db_details, db_table_name, db_row, db_return_column):
    if db_details['db_type'] == "Duck DB":
        row_id = db_table_insert_Duck_DB(db_details, db_table_name,db_row , db_return_column)
    elif db_details['db_type'] == "PostGreSQL":
        row_id = db_table_insert_PostGreSQL(db_details,db_table_name,db_row, db_return_column)
    return row_id


def db_table_insert_Duck_DB(db_details,db_table_name,db_row,db_return_column):
    db_conn = db_connect(db_details)
    df_row = pd.DataFrame.from_dict(db_row)
    #print(df_row)
    print("db_schema_name: ", db_details['db_schema_name'])
    db_conn.sql("INSERT INTO " + db_details['db_schema_name'] + "." + db_table_name + " BY NAME SELECT * FROM df_row")
    db_conn.commit()
    row_id = db_return_column 
    return row_id

def convert_from_dict_to_list(value):
    if isinstance(value, dict) or isinstance(value, list):
        return json.dumps(value)
    return value

def db_table_insert_PostGreSQL(db_details,db_table_name,db_row, db_return_column):
    db_conn = db_connect(db_details)
    df_row = pd.DataFrame.from_dict(db_row)
    db_cursor = db_conn.cursor()
    columns = ', '.join(df_row.columns)
    values = ', '.join(['%s'] * len(df_row.columns))
    insert_sql = f"INSERT INTO {db_details['db_schema_name']}.{db_table_name} ({columns}) VALUES ({values}) RETURNING {db_return_column};"
    rows_to_insert = [tuple(convert_from_dict_to_list(value) for value in row) for row in df_row.to_numpy()]
    #print(insert_sql)
    db_cursor.execute(insert_sql, rows_to_insert[0])
    row_id = db_cursor.fetchone()[0]
    #print(row_id)
    db_conn.commit()
    db_conn.close()
    return row_id

def db_table_get_sequence_id(db_details, db_table_name,db_column_name, db_user_id):
    db_conn = db_connect(db_details)
    cursor = db_conn.cursor()
    select_sql = "SELECT MAX("+ db_column_name + ") FROM "+ db_details['db_schema_name'] + "." + db_table_name + " WHERE User_ID = '" + db_user_id +"'"
    print(select_sql)
    cursor.execute(select_sql)    
    result_set = cursor.fetchall()
    sequence_id = result_set[0][0]
    db_conn.close()
    return sequence_id

def db_table_update(db_details, db_table_name,db_sequence_column_name,db_sequence_column_value, db_column_name, db_column_value, db_user_id):
    db_conn = db_connect(db_details)
    cursor = db_conn.cursor()
    update_sql = "UPDATE "+ db_details['db_schema_name'] + "." + db_table_name + f" SET {db_column_name} = '{db_column_value}'" + \
                    f" WHERE {db_sequence_column_name} = '{db_sequence_column_value}' AND user_id = '{db_user_id }'"
    print(update_sql)
    update_success = cursor.execute(update_sql)
    db_conn.commit()    
    db_conn.close()
    return update_success

def db_get_data_for_statistics(db_details, sql_Query):
    db_conn = db_connect_sql_alchemy(db_details)
    result_set_df = pd.read_sql_query(sql_Query, db_conn)
    # db_conn.close()
    return result_set_df

def db_get_data_for_enrich(db_details, sql_Query):
    db_conn = db_connect(db_details)
    result_set_df = pd.read_sql(sql_Query, db_conn)
    #db_conn.close()
    return result_set_df

def db_get_data(db_details, sql_Query):
    db_conn = db_connect_sql_alchemy(db_details)
    result_set_df = pd.read_sql_query(sql_Query, db_conn)
    #db_conn.close()
    result = result_set_df
    return result

def db_get_data_value(db_details, sql_Query):
    db_conn = db_connect_sql_alchemy(db_details)
    result_set_df = pd.read_sql_query(sql_Query, db_conn)
    #db_conn.close()
    result = result_set_df.iloc[0,0]
    return result

def get_knowledge_base_list(org_id):
    sql_Query = f"SELECT knowledge_base_id, knowledge_base_name  FROM dhimath_doc.knowledge_base" + \
                f" WHERE org_id = {org_id}  AND " + \
                f" marked_for_deletion = 'N'" + \
                f" order by knowledge_base_name"
    knowledge_base_df = db_get_data(gbl_vars.global_session_variables['db_details'], sql_Query) 
    return knowledge_base_df

def get_guided_learn_files_list(org_id):
    sql_Query = f"SELECT guided_file_name, number_of_pages, marked_for_deletion  FROM dhimath_doc.guided_learn_files" + \
                f" WHERE org_id = {org_id}  AND " + \
                f" marked_for_deletion = 'N'" + \
                f" order by guided_learn_files"
    guided_lean_files_df = db_get_data(gbl_vars.global_session_variables['db_details'], sql_Query) 
    return guided_lean_files_df


def get_knowledge_base_details():
    sql_Query = f"SELECT knowledge_base_id, knowledge_base_name, embedding_name, number_of_objects, marked_for_deletion  FROM dhimath_doc.knowledge_base" + \
                f" WHERE org_id = {gbl_tbls.knowledge_base['org_id']}" + \
                f" order by knowledge_base_name"
    knowledge_base_df = db_get_data(gbl_vars.global_session_variables['db_details'], sql_Query) 
    return knowledge_base_df    

def get_knowledge_base_documents_list(org_id,knowledge_base_id):
    sql_Query = f"SELECT knowledge_base_document_id, knowledge_base_file_name FROM dhimath_doc.knowledge_base_documents" + \
                f" WHERE org_id = {org_id}" + \
                f" AND knowledge_base_id = {knowledge_base_id}" + \
                f" order by knowledge_base_file_name"
    knowledge_base_documents_df = db_get_data(gbl_vars.global_session_variables['db_details'], sql_Query) 
    return knowledge_base_documents_df  

def update_number_of_docs_in_knowledge_base(kb_id):
    sql_Query = f"SELECT count(knowledge_base_id) FROM dhimath_doc.knowledge_base_documents" + \
                f" WHERE knowledge_base_id = {kb_id}"
    print(sql_Query)
    number_of_objects = db_get_data_value(gbl_vars.global_session_variables['db_details'], sql_Query)
    print("Number of Documents in the Knowledgebase: ", number_of_objects)
    update_success = db_table_update(gbl_vars.global_session_variables['db_details'],
                                    "knowledge_base",
                                    "knowledge_base_id",
                                    kb_id, 
                                    "number_of_objects",
                                    number_of_objects,
                                    gbl_vars.global_session_variables['user_id'])

def check_user(username, password):
    sql_Query = f"SELECT org_user_id, org_id FROM dhimath_doc.org_users where org_user_name = '{username}' and org_user_password = '{password}' and marked_for_deletion ='N'"
    user_df = db_get_data(gbl_vars.global_session_variables['db_details'],sql_Query)
    org_id = 0
    if user_df.empty != True:
        valid_user = True
        # st.write("Iam Here")
        # st.write(sql_Query)
        org_id = user_df['org_id'][0]
    else:
        valid_user = False

    return valid_user, org_id



def pg_create_engine(db_details):
    # print("Printing type of db details", type(db_details))
    connect = "postgresql+psycopg2://%s:%s@%s:%s/%s" %(
                db_details['db_user'],
                db_details['db_password'],
                db_details['db_host'],
                db_details['db_port'],
                db_details['db_name']
                 )
    pg_db_engine = create_engine(connect)
    return pg_db_engine

def create_and_load_table(df, db_schema, table_name, pg_db_engine):
    number_of_records = df.to_sql(       
                                    table_name, 
                                    con=pg_db_engine, 
                                    schema = db_schema,
                                    index=False, 
                                    if_exists='replace'
                                )
    return number_of_records

def df_insert_to_table(df, db_schema, table_name, pg_db_engine):
    number_of_records = df.to_sql(       
                                    table_name, 
                                    con=pg_db_engine, 
                                    schema = db_schema,
                                    index=False, 
                                    if_exists='append'
                                )
    return number_of_records

def db_get_data_for_chart(db_details, sql_query):
    db_conn = db_connect(db_details)
    result_set_df = pd.read_sql_query(sql_query, db_conn)
    db_conn.close()
    return result_set_df

def db_get_data_for_metric(db_details, sql_query):
    db_conn = db_connect(db_details)
    result_set_df = pd.read_sql_query(sql_query, db_conn)
    db_conn.close()
    return result_set_df.iloc[0]