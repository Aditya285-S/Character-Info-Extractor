import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_mistralai import MistralAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv


load_dotenv()
GROQ_API_KEY = os.environ.get('GROQ_API')
MISTRAL_API = os.environ.get('MISTRAL_API')
DB_FAISS_PATH = 'vectorstore\db_faiss'

def compute_embeddings():
    text_loader_kwargs = {"autodetect_encoding": True}
    loader = DirectoryLoader(
        'Dataset/', 
        glob="*.txt",
        loader_cls = TextLoader,
        loader_kwargs=text_loader_kwargs,
        silent_errors=True
    )
    
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    # There is 429: To many requests error is occuring for MistralAIEmbeddings class
    
    # embedding = MistralAIEmbeddings(
    #     model="mistral-embed", 
    #     api_key=MISTRAL_API,
    #     max_retries = 3,
    #     wait_time = 10,
    #     max_concurrent_requests = 1024
    # )

    embedding = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

    vectorstore = FAISS.from_documents(
        documents = texts,
        embedding = embedding
    )
    
    vectorstore.save_local(DB_FAISS_PATH)
    print("Succesfully created embedding")


if __name__ == "__main__":
    compute_embeddings()