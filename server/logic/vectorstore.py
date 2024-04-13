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
DATA1= os.path.join(os.path.dirname(__file__), '../data/cis.pq')
DATA2= os.path.join(os.path.dirname(__file__), '../data/ir.pq')

datasets= {}

#PRELOADED DS 
dataset= load_dataset(DATA1)
dataset= concatenate_datasets([dataset[x]for x in dataset.keys()])
datasets['CIS Dept']= dataset
dataset= load_dataset(DATA2)
dataset= concatenate_datasets([dataset[x]for x in dataset.keys()])
datasets['Instructor Ratings']= dataset

#Creating list of text documents
docs = []
for i in range(len(datasets['CIS Dept'])):

    page= f"""'Instructor': {str(datasets['CIS Dept']['name'][i])}
'Title': {str(datasets['CIS Dept']['title'][i])}
'Degree': {str(datasets['CIS Dept']['degree'][i])}
'Description': {str(datasets['CIS Dept']['description'][i])}
'Website': {str(datasets['CIS Dept']['website'][i])}
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