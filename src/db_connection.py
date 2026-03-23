from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

class VectorDBConnection:

    _instance = None

    #overriding '__new__' in order to check in memory if 'cls._instance' already exists
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            #tranforms into embeddings
            cls._instance._embeddings = OpenAIEmbeddings(model='text-embedding-3-small')
            cls._instance._db = Chroma(persist_directory='./chroma_db', embedding_function=cls._instance._embeddings)
        return cls._instance
    
    def get_db(self):
        return self._db

"""
# Singleton Testing
s1 = VectorDBConnection()
s2 = VectorDBConnection()
print(s1 is s2)
s1.val = "Singleton Variable"
print(s2.val)"""