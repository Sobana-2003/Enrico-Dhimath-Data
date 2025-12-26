
import pandas as pd
import load_models as lm
import get_answers as ans
from fpdf import FPDF
import os
from dotenv import load_dotenv
load_dotenv() 

def generate_pdf_per_table(table_df, base_output_dir="pdf"):

    domain_name = table_df.iloc[0]["Domain Name"]
    sub_domain = table_df.iloc[0]["Sub Domain Name"]
    table_name = table_df.iloc[0]["Table/View Name"]

    output_dir = os.path.join(base_output_dir, sub_domain)
    os.makedirs(output_dir, exist_ok=True)

    file_name = f"{domain_name}_{sub_domain}_{table_name}.pdf"
    file_path = os.path.join(output_dir, file_name)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for _, row in table_df.iterrows():
        pdf.add_page()
        pdf.set_font("Arial", size=10)

        pdf.multi_cell(0, 6, f"Domain Name: {row['Domain Name']}")
        pdf.multi_cell(0, 6, f"Sub Domain Name: {row['Sub Domain Name']}")
        pdf.multi_cell(0, 6, f"Table/View Name: {row['Table/View Name']}")
        pdf.multi_cell(0, 6, f"Column Name: {row['Column Name']}")
        pdf.multi_cell(0, 6, f"Column Data Type: {row['Data Type']}")
        pdf.multi_cell(0, 6, f"Short Description: {row['Short Description']}")

    pdf.output(file_path)

def generate_descriptions_from_csv(output_dir="pdf", domain_name="Vendor Management"):
    csv_file_path = os.getenv("CSV_FILE_PATH")
    file_path = os.path.join(csv_file_path, "Resource Management.csv")
    df = pd.read_csv(file_path)
    if df.empty:
        return

    llm = lm.initalise_llm(llm_type="Azure OpenAI")
    rows = []
    for table_name, table_df in df.groupby("Table/View Name"):
        columns_list = table_df["Column Name"].str.lower().tolist()

        enriched_rows = []

        for _, row in table_df.iterrows():
            row_dict = row.to_dict()
            print(f"Generating description for {row_dict['Column Name']} in table {table_name}")

            description = ans.get_descriptions(
                llm=llm,
                domain=domain_name,
                column_name=row_dict["Column Name"].lower(),
                columns_list=columns_list,
                sub_domain=row_dict.get("Sub Domain Name", "")
            )

            row_dict["Short Description"] = description.get("short_description", "")
            enriched_rows.append(row_dict)
            rows.append(row_dict)

        enriched_df = pd.DataFrame(enriched_rows)
        # generate_pdf_per_table(enriched_df, base_output_dir=output_dir)

    final_df = pd.DataFrame(rows)
    final_df.to_csv(file_path, index=False)

if __name__ == "__main__":
    generate_descriptions_from_csv()





# import pandas as pd
# import load_models as lm
# import get_answers as ans
# from fpdf import FPDF
# import os

# def generate_pdf_per_table(table_df, base_output_dir="pdf"):

#     domain_name = table_df.iloc[0]["Domain Name"]
#     sub_domain = table_df.iloc[0]["Sub Domain Name"]
#     table_name = table_df.iloc[0]["Table/View Name"]

#     output_dir = os.path.join(base_output_dir, sub_domain)
#     os.makedirs(output_dir, exist_ok=True)

#     file_name = f"{domain_name}_{sub_domain}_{table_name}.pdf"
#     file_path = os.path.join(output_dir, file_name)

#     pdf = FPDF()
#     pdf.set_auto_page_break(auto=True, margin=15)

#     for _, row in table_df.iterrows():
#         pdf.add_page()
#         pdf.set_font("Arial", size=10)

#         pdf.multi_cell(0, 6, f"Domain Name: {row['Domain Name']}")
#         pdf.multi_cell(0, 6, f"Sub Domain Name: {row['Sub Domain Name']}")
#         pdf.multi_cell(0, 6, f"Table/View Name: {row['Table/View Name']}")
#         pdf.multi_cell(0, 6, f"Column Name: {row['Column Name']}")
#         pdf.multi_cell(0, 6, f"Column Data Type: {row['Data Type']}")
#         pdf.multi_cell(0, 6, f"Short Description: {row['Short Description']}")

#     pdf.output(file_path)


# def generate_descriptions_from_csv(csv_file_path, output_dir="pdf", domain_name="Vendor Management"):
#     df = pd.read_csv(csv_file_path)
#     if df.empty:
#         return

#     llm = lm.initalise_llm(llm_type="Azure OpenAI")

#     for table_name, table_df in df.groupby("Table/View Name"):
#         columns_list = table_df["Column Name"].str.lower().tolist()

#         enriched_rows = []

#         for _, row in table_df.iterrows():
#             row_dict = row.to_dict()
#             print(f"Generating description for {row_dict['Column Name']} in table {table_name}")

#             description = ans.get_descriptions(
#                 llm=llm,
#                 domain=domain_name,
#                 column_name=row_dict["Column Name"].lower(),
#                 columns_list=columns_list,
#                 sub_domain=row_dict.get("Sub Domain Name", "")
#             )

#             row_dict["Short Description"] = description.get("short_description", "")
#             enriched_rows.append(row_dict)

#         enriched_df = pd.DataFrame(enriched_rows)
#         generate_pdf_per_table(enriched_df, base_output_dir=output_dir)


# if __name__ == "__main__":
#     generate_descriptions_from_csv(csv_file_path="Financial Operations.csv")
