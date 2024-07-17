import os

BERT_MODEL='distilbert/distilbert-base-uncased'
BERT_DIM= 768
DATA1= os.path.join(os.path.dirname(__file__), '../data/cis.pq')
DATA2= os.path.join(os.path.dirname(__file__), '../data/ir.pq')