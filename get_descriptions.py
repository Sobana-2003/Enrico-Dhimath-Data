
from db import get_conn, get_conn_string, summarise_table, get_columns, get_tables
import load_models as lm
import get_answers as ans

import pandas as pd

def generate_descriptions(db_type,dataset_name: str, domain_name: str, columns_list: list, sub_domain: str):
    # if prev_result.get("status") == "error":
    #     return prev_result
    db = get_conn()
    conn_string, schema = get_conn_string(db_type)
    summary, num_of_rows, num_cols = summarise_table(conn_string=conn_string, schema=schema, table_name=dataset_name)
    llm = lm.initalise_llm(llm_type="Azure OpenAI")
    for column in summary:
        desc = ans.get_descriptions(
            llm=llm,
            domain=domain_name,
            column_name=column["Column_Name"].lower(),
            columns_list=columns_list,
            sub_domain=sub_domain
        )
        values = {
            "column_short_description": desc.get("short_description", ""),
            # "column_long_description": desc.get("long_description", ""),
            # "column_min_value": None if column.get("Min_Value") == "N/A" else column.get("Min_Value"),
            # "column_max_value": None if column.get("Max_Value") == "N/A" else column.get("Max_Value"),
        }
        print(f"Updating descriptions for column: {column['Column_Name']}"
              f" Short Desc: {values['column_short_description']}")
            #   f" Long Desc: {values['column_long_description']}")
            #   f" Min Value: {values['column_min_value']}"
            #   f" Max Value: {values['column_max_value']}")
        keys = {
            "dataset_name": dataset_name,
            "dataset_column_name": column["Column_Name"].lower()
        }
        print(keys)
        # update_record(db=db, table="dataset_column_details", values=values, keys=keys, schema="dhimath_metadata")
    return {"status": "success", "message": "Descriptions updated", "count": len(summary)}


# def create_metadata(db_type):
#     conn_str, schema = get_conn_string(db_type=db_type)
#     tables_list = get_tables(conn_str, schema_name=schema)

#     rows = []

#     for table in tables_list:
#         columns = get_columns(conn_str, schema, table)
#         for col in columns:
#             rows.append({
#                 "Table/View Name": table,
#                 "Column Name": col["columnName"],
#                 "Data Type": col["dataType"],
#             })

#     df = pd.DataFrame(rows)
#     df.to_csv("Enrico_data.csv", index=False)

def create_metadata(db_type):
    conn_str, schema = get_conn_string(db_type=db_type)
    tables_list = get_tables(conn_str, schema_name=schema)
    print("hii")

    llm = lm.initalise_llm(llm_type="Azure OpenAI")
    print("llm:",llm)

    row = []

    for table in tables_list:
        columns = get_columns(conn_str, schema, table)
        columns_list = [c["columnName"].lower() for c in columns]

        for col in columns:
            print("hii")
            # desc = ans.get_descriptions(
            #     llm=llm,
            #     domain="Vendor Management",                     
            #     column_name=col["columnName"].lower(),
            #     columns_list=columns_list
            # )

            row.append({
                "Domain Name": "Vendor Management",
                "Table/View Name": table,
                "Column Name": col["columnName"],
                "Data Type": col["dataType"],
                # "Column Description": desc.get("short_description", "")
            })
            # generate_pdf_per_row(row)

            # print(
            #     f"{table}.{col['columnName']} -> "
            #     f"{desc.get('short_description', '')}"
            # )

    df = pd.DataFrame(row)
    df.to_csv("Enrico_data.csv", index=False)

    return {
        "tables": len(tables_list),
        "columns": len(row)
    }


if __name__ == "__main__":
    metadata = create_metadata(db_type="sqlserver")
    








# from db import get_conn, get_conn_string, summarise_table, get_columns, get_tables
# import load_models as lm
# import get_answers as ans
# from fpdf import FPDF
# import pandas as pd

# def generate_descriptions(db_type,dataset_name: str, domain_name: str, columns_list: list, sub_domain: str):
#     # if prev_result.get("status") == "error":
#     #     return prev_result
#     db = get_conn()
#     conn_string, schema = get_conn_string(db_type)
#     summary, num_of_rows, num_cols = summarise_table(conn_string=conn_string, schema=schema, table_name=dataset_name)
#     llm = lm.initalise_llm(llm_type="Azure OpenAI")
#     for column in summary:
#         desc = ans.get_descriptions(
#             llm=llm,
#             domain=domain_name,
#             column_name=column["Column_Name"].lower(),
#             columns_list=columns_list,
#             sub_domain=sub_domain
#         )
#         values = {
#             "column_short_description": desc.get("short_description", ""),
#             # "column_long_description": desc.get("long_description", ""),
#             # "column_min_value": None if column.get("Min_Value") == "N/A" else column.get("Min_Value"),
#             # "column_max_value": None if column.get("Max_Value") == "N/A" else column.get("Max_Value"),
#         }
#         print(f"Updating descriptions for column: {column['Column_Name']}"
#               f" Short Desc: {values['column_short_description']}")
#             #   f" Long Desc: {values['column_long_description']}")
#             #   f" Min Value: {values['column_min_value']}"
#             #   f" Max Value: {values['column_max_value']}")
#         keys = {
#             "dataset_name": dataset_name,
#             "dataset_column_name": column["Column_Name"].lower()
#         }
#         print(keys)
#         # update_record(db=db, table="dataset_column_details", values=values, keys=keys, schema="dhimath_metadata")
#     return {"status": "success", "message": "Descriptions updated", "count": len(summary)}


# import os

# def generate_pdf_per_row(row, output_dir="pdf_output"):
#     os.makedirs(output_dir, exist_ok=True)

#     file_name = f"{row['Domain Name']}_{row['Table/View Name']}_{row['Column Name']}.pdf"
#     # file_name = file_name.replace(" ", "_")
#     file_path = os.path.join(output_dir, file_name)

#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_auto_page_break(auto=True, margin=15)
#     pdf.set_font("Arial", size=12)

#     pdf.cell(0, 10, "Column Metadata", ln=True)
#     pdf.ln(5)

#     for key, value in row.items():
#         pdf.multi_cell(0, 8, f"{key}: {value}")
#         pdf.ln(2)

#     pdf.output(file_path)

# # def create_metadata(db_type):
# #     conn_str, schema = get_conn_string(db_type=db_type)
# #     tables_list = get_tables(conn_str, schema_name=schema)

# #     rows = []

# #     for table in tables_list:
# #         columns = get_columns(conn_str, schema, table)
# #         for col in columns:
# #             rows.append({
# #                 "Table/View Name": table,
# #                 "Column Name": col["columnName"],
# #                 "Data Type": col["dataType"],
# #             })

# #     df = pd.DataFrame(rows)
# #     df.to_csv("Enrico_data.csv", index=False)

# def create_metadata(db_type):
#     conn_str, schema = get_conn_string(db_type=db_type)
#     tables_list = get_tables(conn_str, schema_name=schema)
#     print("hii")

#     llm = lm.initalise_llm(llm_type="Azure OpenAI")
#     print("llm:",llm)

#     row = []

#     for table in tables_list:
#         columns = get_columns(conn_str, schema, table)
#         columns_list = [c["columnName"].lower() for c in columns]

#         for col in columns:
#             print("hii")
#             desc = ans.get_descriptions(
#                 llm=llm,
#                 domain="Vendor Management",                     
#                 column_name=col["columnName"].lower(),
#                 columns_list=columns_list
#             )

#             row.append({
#                 "Domain Name": "Vendor Management",
#                 "Table/View Name": table,
#                 "Column Name": col["columnName"],
#                 "Data Type": col["dataType"],
#                 "Column Description": desc.get("short_description", "")
#             })
#             generate_pdf_per_row(row)

#             # print(
#             #     f"{table}.{col['columnName']} -> "
#             #     f"{desc.get('short_description', '')}"
#             # )

#     df = pd.DataFrame(row)
#     df.to_csv("Enrico_data.csv", index=False)

#     return {
#         "tables": len(tables_list),
#         "columns": len(row)
#     }


# if __name__ == "__main__":
#     metadata = create_metadata(db_type="sqlserver")
    
