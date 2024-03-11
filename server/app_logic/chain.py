from langchain.schema.output_parser import StrOutputParser
from langchain_core.messages import get_buffer_string
from langchain_core.prompts import format_document
from langchain.prompts import PromptTemplate
from operator import itemgetter

from .database import KMIT_Database

kmit_data= KMIT_Database()

template= """[INST]You are an AI assistant that helps people find information. User will you give you a question. Your task is to answer as faithfully as you can
Do Not provide Context to interact with the Human if not Needed:

Context:
{context}

Chat History:
{chat_history}

Question: 
{question}[\INST]"""

prompt_rag= PromptTemplate.from_template(template)

DEFAULT_DOCUMENT_PROMPT = PromptTemplate.from_template(template="{page_content}")
class Logic():
    def __init__(self, llm):
        #chain
        self.chain= (
            { 
                'context': itemgetter('question') | kmit_data.retriever | self._combine_documents,
                'chat_history': lambda x: get_buffer_string(x['chat_history']),
                'question': itemgetter('question')
            }
            | prompt_rag
            | llm
            | StrOutputParser()
        )
        
        self.retriever= kmit_data.retriever

    def _combine_documents(self, docs, document_prompt=DEFAULT_DOCUMENT_PROMPT, document_separator="\n\n"):
        doc_strings = [format_document(doc, document_prompt) for doc in docs]
        return document_separator.join(doc_strings)