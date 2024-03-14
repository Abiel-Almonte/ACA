from dataclasses import dataclass
from datasets import load_dataset, concatenate_datasets

from langchain.schema import Document
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores.milvus import Milvus

#CONSTANTS 
HOST= 'localhost'
PORT= 19530
USER= 'root'
PASS= 'Milvus'
CONNECTION_ARGS= {'host': HOST, 'port': PORT, 'user': USER, 'password': PASS}

TYPE= 'similarity'
SBERT= 'all-MiniLM-L6-v2'
SEARCH_CONFIG= {'k': 6, 'lambda_mult': 0.25}
ef= HuggingFaceEmbeddings(SBERT)

DB_CONFIG= {'embedding': ef, 'connection_args': CONNECTION_ARGS, 'drop_old':True}

#PRELOADED DS 
dataset= load_dataset('./data')
dataset= concatenate_datasets([dataset[x]for x in dataset.keys()])

#Creating list of langchain compatible documents
docs = []
for i in range(len(dataset)):

    page= f"""'Name': {str(dataset['product'][i])}
'Description': {str(dataset['description'][i])}
'Benefits': {str(dataset['benefits'][i])}
'Limitations': {str(dataset['limitations'][i])}
---"""
    
    docs.append(
        Document(
            page_content= page,
        )  
    )

#Creating a vectordb using Lanchain-Milvus
vectordb= Milvus.from_documents(documents= docs, **DB_CONFIG)
retriever= vectordb.as_retriever(search_type= TYPE, search_kwargs= SEARCH_CONFIG)

@dataclass
class KMIT_Database:
    retriever = retriever



