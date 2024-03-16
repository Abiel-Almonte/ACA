from dataclasses import dataclass
from datasets import load_dataset, concatenate_datasets

from langchain.schema import Document
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores.milvus import Milvus
import os

#CONSTANTS 
HOST= 'localhost'
PORT= 19530
USER= 'root'
PASS= 'Milvus'
CONNECTION_ARGS= {'host': HOST, 'port': PORT, 'user': USER, 'password': PASS}
EF= HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
DB_CONFIG= {'embedding': EF, 'connection_args': CONNECTION_ARGS, 'drop_old':True}
DATA= os.path.join(os.path.dirname(__file__), '../data.pq')


#PRELOADED DS 
dataset= load_dataset(DATA)
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

@dataclass
class Vectorstore:
    vectordb = vectordb