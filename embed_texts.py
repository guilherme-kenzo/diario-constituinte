from sentence_transformers import SentenceTransformer

def load_model():
    return SentenceTransformer("sentence-transformers/distiluse-base-multilingual-cased")

def load_tokenizer():
   return SentenceTransformer("sentence-transformers/distiluse-base-multilingual-cased") 


