import os
from sentence_transformers import SentenceTransformer

import faiss
import numpy as np

# support m3e embedding
def get_embedding(texts, embedding_type = 'base'):

    local_path = 'm3e-' + embedding_type
    if os.path.exists(local_path):
        embedding_model = SentenceTransformer(local_path)
    else:
        embedding_model = SentenceTransformer('moka-ai/m3e-' + embedding_type)

    embeddings = {}
    for key in texts.keys():
        embeddings[key] = embedding_model.encode(texts[key])

    return embeddings


# match nodes
def Faiss(document_embeddings, query_embeddings, topk, texts):

    nodes_info = {}

    for key in texts.keys():
        value_embedding = document_embeddings[key]
        value_text = texts[key]

        index = faiss.IndexFlatIP(value_embedding.shape[1])
        index.add(value_embedding)
        
        _, indices = index.search(np.array(query_embeddings["keywords"]), topk)

        nodes = set()
        for sublist in indices:
            for s in sublist:
                nodes.add(value_text[s])

        nodes_info[key] = nodes
    
    return nodes_info

