import tabula
import PyPDF2
import os
import pandas as pd 
import os, zipfile, xml.dom.minidom, sys, getopt

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from striprtf.striprtf import rtf_to_text, rtf_to_text
from docx2pdf import convert

def get_pdf_info(file_name):
    fp = open(file_name, 'rb')
    parser = PDFParser(fp)
    pdf_info = PDFDocument(parser)
    # print("PDF Info")
    # print(pdf_info.info)  # The "Info" metadata

    # tables = tabula.read_pdf(file_name,multiple_tables=True,pages='all',encoding='utf-8')
    # print("Table Info")
    # print(tables.count)

    pdfReader = PyPDF2.PdfReader(file_name)
    text_count = len(pdfReader.pages)
    count_type = "Pages"
    total_pages = str(text_count) + " " +count_type

    # print ("Number of Pages:", total_pages)
    # # Open document
    # pdf_document = ap.Document(file_name)
    # # Get document information
    # doc_info = pdf_document.info
    # # Show document information
    # print("Author :", doc_info.author)
    # print("Creation Date :", doc_info.creation_date)
    # print("Keywords :", doc_info.keywords)
    # print("Modify Date :", doc_info.mod_date)
    # print("Subject :", doc_info.subject)
    # print("Title :", doc_info.title)
    fp.close()
    return (pdf_info.info, total_pages, text_count, count_type)

def get_rtf_info(file_name):
    with open(file_name) as infile:
        content = infile.read()
        text = rtf_to_text(content) 
        # print(text)
        text_count = len(text)
        count_type = "Chars"
        total_chars = str(text_count) + " " + count_type
    infile.close() 
    return ("", total_chars, text_count, count_type)

def get_docx_info(file_name):
    document = zipfile.ZipFile(file_name)
    dxml = document.read('docProps/app.xml')
    docXml = xml.dom.minidom.parseString(dxml)
    page_count = docXml.getElementsByTagName('Pages')[0].childNodes[0].nodeValue
    #print("Word Page count: " + total_pages)
    text_count = page_count
    count_type = "Pages"
    total_pages = str(text_count) + " " + count_type
    return (docXml, total_pages, text_count, count_type)

# def get_docx_info(file_name):
#     try:
#         document = zipfile.ZipFile(file_name)

#         # Some docx files do not even have app.xml
#         if 'docProps/app.xml' not in document.namelist():
#             return ("", "0 Pages", 0, "Pages")

#         dxml = document.read('docProps/app.xml')
#         docXml = xml.dom.minidom.parseString(dxml)

#         pages_nodes = docXml.getElementsByTagName('Pages')

#         if pages_nodes and pages_nodes[0].childNodes:
#             page_count = int(pages_nodes[0].childNodes[0].nodeValue)
#         else:
#             # DOCX does not reliably store page count
#             page_count = 0

#         count_type = "Pages"
#         total_pages = f"{page_count} {count_type}"

#         return (docXml, total_pages, page_count, count_type)

#     except Exception as e:
#         print(f"Error reading DOCX info for {file_name}: {e}")
#         return ("", "0 Pages", 0, "Pages")


def get_txt_info(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        content = file.read()
        text_count = len(content)
        count_type = "Chars"
        total_chars = str(text_count) + " " + count_type
    file.close()
    return ("", "", "", total_chars)

# def get_xls_info(file_name):
#     total_chars = 0
#     return ("", total_chars)
def get_xls_info(file_name):
    text_count = 0
    count_type = "Cells"
    total_chars = str(text_count) + " " + count_type
    return ("", total_chars, text_count, count_type)


def get_csv_info(file_name):
    df = pd.read_csv(file_name)
    number_of_rows = len(df)
    number_of_columns = len(df.columns)
    total_chars = 0
    return (number_of_rows,number_of_columns,"", total_chars)


def get_all_files_info(folder_path, selected_files):
    filenames = os.listdir(folder_path)
    df = pd.DataFrame()
    
    if selected_files != '':
        filenames = selected_files

    for file in filenames:
        file_name_with_path = folder_path + "\\"+ file
        # print(str(filename[-3:]))
        if (len(file)-3) > 50:
            partial_file_name = file[:50]+"..." + file[-3:]
        else:
            partial_file_name = file
            
        if file.endswith(".pdf"):
            pdf_info, total_pages, text_count, count_type = get_pdf_info(file_name_with_path)
            df_row = {'folder_path': folder_path, 'File Name':partial_file_name, 'Full_file_name':file, 'file_info':pdf_info, 'Pages / Chars': total_pages, 'Count':text_count, "Count Type":count_type }
            df = df._append(df_row, ignore_index=True)
        elif file.endswith(".rtf"):
            rtf_info, total_pages, text_count, count_type = get_rtf_info(file_name_with_path)
            df_row = {'folder_path': folder_path, 'File Name':partial_file_name, 'Full_file_name':file, 'file_info':rtf_info, 'Pages / Chars': total_pages, 'Count':text_count, "Count Type":count_type  }
            df = df._append(df_row, ignore_index=True)
        elif file.endswith(".docx") or file.endswith(".doc"):
            docx_info, total_pages, text_count, count_type = get_docx_info(file_name_with_path)
            df_row = {'folder_path': folder_path, 'File Name': partial_file_name, 'Full_file_name': file, 'file_info': docx_info, 'Pages / Chars': total_pages, 'Count':text_count, "Count Type":count_type }
            df = df._append(df_row, ignore_index=True)
        elif file.endswith(".txt"):
            txt_info, total_chars, text_count, count_type = get_txt_info(file_name_with_path)
            df_row = {'folder_path': folder_path, 'File Name': partial_file_name, 'Full_file_name': file, 'file_info': txt_info, 'Pages / Chars': total_chars, 'Count':text_count, "Count Type":count_type}
            df = df._append(df_row, ignore_index=True)
        elif file.endswith(".xls"):
            txt_info, total_chars, text_count, count_type = get_xls_info(file_name_with_path)
            df_row = {'folder_path': folder_path, 'File Name': partial_file_name, 'Full_file_name': file, 'file_info': txt_info, 'Pages / Chars': total_chars, 'Count':text_count, "Count Type":count_type}
            df = df._append(df_row, ignore_index=True)
        elif file.endswith(".csv"):
            number_of_rows, number_of_columns, text_count, count_type = get_csv_info(file_name_with_path)
            df_row = {'folder_path': folder_path, 'File Name': partial_file_name, 'Full_file_name': file, 'Number of Rows': number_of_rows, 'Number of Columns': number_of_columns, 'Count':text_count, "Count Type":count_type}
            df = df._append(df_row, ignore_index=True)



    #selected_filename = st.selectbox('Select a file', filenames)
    return df



def convert_docx_to_pdf(user_dir):
    convert(user_dir)

# file_path = 'F:\\To Read'
# df = get_all_pdfs_info(file_path)
# print(df)