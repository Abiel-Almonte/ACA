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

VARCHAR_LIMIT= 64000
PROC= open('/proc/cpuinfo').read().count('processor\t')
NUM_PROC= int(PROC - 0.5*PROC)

TYPE= 'similarity'
TOP_K= 8
LAMBDA= 0.25
SBERT= 'all-MiniLM-L6-v2'
SEARCH_CONFIG= {'k': TOP_K, 'lambda_mult': LAMBDA}
SBERT_CONFIG= {'model_name': SBERT}
ef= HuggingFaceEmbeddings(**SBERT_CONFIG)

DATA= '/home/abiel/workspace/Data/KMIT-medium-dataset-ReAct.pq'
DB_CONFIG= {'embedding': ef, 'connection_args': CONNECTION_ARGS}

#PRELOADED DS 
dataset= load_dataset(DATA)
dataset= concatenate_datasets([dataset[x]for x in dataset.keys()])
#dataset= dataset.filter(lambda r:  0 < len(r['description']) <= VARCHAR_LIMIT)

#Creating list of langchain compatible documents
docs = list()
for i in range(len(dataset)):
    docs.append(
        Document(
            page_content= str(dataset['description'][i]),
            metadata= {
                'Name': str(dataset['product'][i]),
                'Benefits': str(dataset['benefits'][i]),
                'Limitations': str(dataset['limitations'][i]),
            }
        )  
    )


#Creating a vectordb using Lanchain-Milvus
vectordb= Milvus.from_documents(documents= docs, drop_old= True, **DB_CONFIG)
retriever= vectordb.as_retriever(search_type= TYPE, search_kwargs= SEARCH_CONFIG)

@dataclass
class KMIT_Database:
    retriever = retriever



