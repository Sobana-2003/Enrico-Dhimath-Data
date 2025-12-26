import os
import os
from dotenv import load_dotenv


from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
load_dotenv() 
def initalise_llm(llm_type: str = "Azure OpenAI"):
    if llm_type == "Azure OpenAI":
        llm = AzureChatOpenAI(
            azure_deployment="gpt-4o",
            api_key=os.environ.get("AZURE_OPENAI_KEY"),
            model="gpt-4o",
            api_version=os.environ.get("AZURE_OPENAI_VERSION"),
            azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
            temperature=0,
        )
        print("LLM initialized: Azure OpenAI")
        return llm
    return None

def qa_chain():
    llm = initalise_llm(llm_type="")
    prompt = PromptTemplate(
        input_variables=["question"],
        template="Please answer the following question: {question}."
    )
    qa = prompt | llm | StrOutputParser()
    return qa

def get_answer(question: str):
    qa = qa_chain()
    qa.invoke(question)
    return