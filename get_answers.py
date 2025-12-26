from langchain_core.prompts import PromptTemplate
from typing_extensions import Annotated, TypedDict

class Domainify(TypedDict):
    domain: Annotated[str, "The domain where the dataset belongs to"]
    column_name: Annotated[str, "The name of the column"]
    min_value: Annotated[str, "Minimum value in the column"]
    max_value: Annotated[str, "Maximum value in the column"]
    data_type: Annotated[str, "Data type of the column"]
    short_description: Annotated[str, "Short description of the column"]
    long_description: Annotated[str, "Longer description of the column"]

def get_descriptions(llm, domain: str, column_name: str, columns_list: list[dict],sub_domain: str):
   
    # template = (
    #     "Generate both a short description "
    #     "and a comprehensive long description for the {column_name} in the context of the domain {domain} and {sub_domain}."
    #     "Use the complete list of available columns {columns_list} as contextual reference to understand how {column_name} relates to, differs from, or complements other fields in the dataset."
    #     "The short description should capture the essential meaning in a brief and clear manner, while the long "
    #     "description should provide a detailed and thorough explanation, covering all relevant aspects and context. "
    #     "Ensure that both descriptions are meaningful, accurate, and directly related to the content of the 'column_name'. "
    #     "Pay close attention to any nuances or specific details mentioned in the knowledge base to maintain accuracy and relevance."
    # )
    template = (
        """Generate a short description for the {column_name} in the context of the domain {domain}.
        Use the complete list of available columns {columns_list} as contextual reference to understand how {column_name} relates to, differs from, or complements other fields in the dataset.
        The short description should capture the essential meaning in a brief and clear manner 
        Ensure that descriptions are meaningful, accurate, and directly related to the content of the 'column_name'. 
        Pay close attention to any nuances or specific details mentioned in the knowledge base to maintain accuracy and relevance.
    """)
   
    prompt = PromptTemplate.from_template(template)
    filled_prompt = prompt.invoke({"domain": domain, "column_name": column_name, "columns_list": columns_list,"sub_domain": sub_domain})
    structured_llm = llm.with_structured_output(Domainify)
    result = structured_llm.invoke(filled_prompt)
    return result

class FormulaePrompt(TypedDict):
    # formula: Annotated[str, "INPUT FORMULA GIVEN TO YOU!"]
    sql: Annotated[str, "Generated SQL query based on the formula"]

def get_formulae(llm, formula: str, table_info: str, dialect: str):
    template = (
    """
    You are given a plain English business formula: "{formula}"

    Your task is to convert this into a syntactically correct SQL query based on the schema you must utitlise the table names and more correctly.
    {table_info}

    Use the {dialect} SQL dialect for your output.

    You must return the output as a dictionary with the following structure:
    {{
    "formula": "<repeat the input formula>",
    "sql": "<generated SQL query>"
    }}
    """
    )

    prompt = PromptTemplate.from_template(template)
    filled_prompt = prompt.invoke({
        "formula": formula,
        "table_info": table_info,
        "dialect": dialect
    })
    structured_llm = llm.with_structured_output(FormulaePrompt)
    result = structured_llm.invoke(filled_prompt)
    return result