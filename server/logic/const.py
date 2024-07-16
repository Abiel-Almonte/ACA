import os


HOST= 'localhost'
PORT= 19530
USER= 'root'
PASS= 'Milvus'
BERT_MODEL='distilbert/distilbert-base-uncased'
BERT_DIM= 768
CONNECTION_ARGS= {'host': HOST, 'port': PORT, 'user': USER, 'password': PASS}
DATA1= os.path.join(os.path.dirname(__file__), '../data/cis.pq')
DATA2= os.path.join(os.path.dirname(__file__), '../data/ir.pq')