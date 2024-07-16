from const import *
import faiss, torch, numpy as np, numpy.typing
from typing import Dict, Any, List
from tqdm import tqdm
from transformers import DistilBertTokenizer, DistilBertModel
from torch.utils.data import DataLoader
from datasets import load_dataset, concatenate_datasets

device: str= 'cuda'

class TextIndexer():
    def __init__(self, data_fp:str, index_fp:str= 'index.faiss', batch_size: int= 8)->None:
        self._embed_model= DistilBertModel.from_pretrained(BERT_MODEL).to(device).eval()
        self._tokenizer= DistilBertTokenizer.from_pretrained(BERT_MODEL)
        self._batch_size= batch_size

        self._ds= load_dataset(data_fp)
        self._ds= concatenate_datasets([self._ds[x]for x in self._ds.keys()])

        self.index= faiss.IndexFlatIP(BERT_DIM)

        if os.path.exists(index_fp):
            print(f"Loading existing index from {index_fp}")
            self.index= faiss.read_index(index_fp)

        else:
            print(f"Creating new index and saving to {index_fp}")
            self.create_index()
            faiss.write_index(self.index, index_fp)

    def get_document(self, batch: Dict[str, Any])->Dict[str, List[str]]:
        batch_size = len(next(iter(batch.values())))
        document= ["\n".join(f"{key}: {value[i]}" for key, value in batch.items()) for i in range(batch_size)]
        return {'document': document}

    def get_text_embedding(self, batch: Dict[str, Any])->numpy.typing.NDArray:
        inputs= self._tokenizer(
            batch['document'],
            return_tensors='pt',
            padding='max_length',
            max_length= 512, 
            truncation= True
        )
        inputs= {k: v.to(device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs= self._embed_model(**inputs)

        text_embedding, _= outputs.last_hidden_state.max(dim=1)
        normalized_embedding = torch.nn.functional.normalize(text_embedding, p=2, dim=1)
        return normalized_embedding.cpu().numpy().astype(np.float32)
    
    def transform(self)->None:
        self._ds= self._ds.map(
            self.get_document,
            batched=True,
            batch_size=self._batch_size,
            remove_columns=self._ds.column_names, 
            desc="Creating documents"
        )

        self._ds= self._ds.map(
            lambda batch: {'embedding': self.get_text_embedding(batch)}, 
            batched=True,
            batch_size=self._batch_size, 
            desc="Generating embeddings"
        )

    def create_index(self)->None:
        self.transform()

        dataloader= DataLoader(self._ds, drop_last=True)

        embeddings= []
        for batch in tqdm(dataloader, desc="Creating index"):
            embeddings.append(numpy.stack(batch['embedding']).flatten())

        embeddings= np.vstack(embeddings, dtype='float32').astype('float32')
        self.index.add(embeddings)

    def search(self, query:str, k:int= 1, **kwargs)->List[Dict[str,str]]:
        query= {'document': [query]}
        query_embedding= self.get_text_embedding(query)

        _, idxs= self.index.search(query_embedding, k=k)
        results= [{"document": self._ds["document"][idx]} for idx in idxs[0]]
        return results
    
    def __call__(self, query: str, **kwargs)->List[Dict[str,str]]:
        return self.search(query, **kwargs)

            

        