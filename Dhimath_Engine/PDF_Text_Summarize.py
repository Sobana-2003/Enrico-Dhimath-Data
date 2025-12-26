from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Generate summaries of text elements



def generate_text_summaries(model, texts, tables, summarize_texts=False):
    """
    Summarize text elements
    texts: List of str
    tables: List of str
    summarize_texts: Bool to summarize texts
    """

    # Prompt
    prompt_text = """You are an assistant tasked with summarizing tables and text for retrieval. \
    These summaries will be embedded and used to retrieve the raw text or table elements. \
    Give a concise summary of the table or text that is well optimized for retrieval. Table or text: {element} """
    prompt = ChatPromptTemplate.from_template(prompt_text)

    # Text summary chain
    # model = ChatOpenAI(temperature=0, model="gpt-4")

    summarize_chain = {"element": lambda x: x} | prompt | model | StrOutputParser()

    # Initialize empty summaries
    text_summaries = []
    table_summaries = []

    # Apply to text if texts are provided and summarization is requested
    if texts and summarize_texts:
        for i in len(texts):
            text,page_num = texts[i]
            text_summaries = ([summarize_chain.batch(text, {"max_concurrency": 5}), page_num])
    elif texts:
        text_summaries = texts

    # Apply to tables if tables are provided
    if tables:
        for i in len(tables):
            table,page_num = tables[i]
            #print(table)
            #print(page_num)
            table_summaries.append([summarize_chain.batch(table, {"max_concurrency": 5}),page_num])

    return text_summaries, table_summaries