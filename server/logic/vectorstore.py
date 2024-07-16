from dataclasses import dataclass
from datasets import load_dataset, concatenate_datasets, Dataset

from langchain.schema import Document
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores.milvus import Milvus
import os

#CONSTANTS

#datasets= {}

#PRELOADED DS 
#dataset= load_dataset(DATA1)
#dataset= concatenate_datasets([dataset[x]for x in dataset.keys()])
#datasets['CIS Dept']= dataset
#dataset= load_dataset(DATA2)
#dataset= concatenate_datasets([dataset[x]for x in dataset.keys()])
#datasets['Instructor Ratings']= dataset

#Creating list of text documents
#docs = []
#for i in range(len(datasets['CIS Dept'])):

 #   page= f"""'Instructor': {str(datasets['CIS Dept']['name'][i])}
#'Title': {str(datasets['CIS Dept']['title'][i])}
#'Degree': {str(datasets['CIS Dept']['degree'][i])}
#'Description': {str(datasets['CIS Dept']['description'][i])}
#'Website': {str(datasets['CIS Dept']['website'][i])}
#---"""
    
#    docs.append(
#        Document(
#            page_content= page,
#       )  
#    )

#Creating a vectordb using Lanchain-Milvus

#@dataclass
#class Vectorstore:
#    vectordb = vectordb

from const import*
import faiss, torch, numpy, numpy.typing
from typing import Dict
from tqdm import tqdm
from transformers import DistilBertTokenizer, DistilBertModel

class TextIndexer():
    def __init__(self, data_fp:str, index_fp:str= 'index.faiss',)->None:
        self._embed_model= DistilBertModel.from_pretrained(BERT_MODEL)
        self._tokenizer= DistilBertTokenizer.from_pretrained(BERT_MODEL)

        self._ds= load_dataset(data_fp)
        self._ds= concatenate_datasets([self._ds[x]for x in self._ds.keys()])

        self.index= faiss.IndexFlatIP(BERT_DIM)

        if os.path.exists(index_fp):
            print(f"Loading existing index from {index_fp}")
            self.index= faiss.read_index(index_fp)

        #else:
            #print(f"Creating new index and saving to {index_fp}")
            #self.create_index()
            #faiss.write_index(index_fp)

    def get_document(self, batch: Dict):
        document=""

        for key in batch.keys():
            document+= f"{key}: {batch[key]}\n"
        
        return {'document': document}

    def get_text_embedding(self, batch: Dict):
        inputs= self._tokenizer(batch['document'], return_tensors='pt', padding= 'max_length', max_length= 512, truncation= True)

        #with torch.no_grad:
        text_embedding= self._embed_model(**inputs).last_hidden_state
        batch['document']= torch.nn.functional.normalize(text_embedding)

        return batch
    
    def transform(self):
        self._ds= self._ds.map(self.get_document, remove_columns=self._ds.column_names)
        self._ds= self._ds.map(self.get_text_embedding)

    def create_index(self):
        self.transform()


            

        