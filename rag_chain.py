import os
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

load_dotenv()

def build_qa_chain(context_text):
    if not context_text.strip():
        raise ValueError("Context text is empty. Cannot build QA chain.")

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    splitter = CharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    docs = splitter.create_documents([context_text])
    db = FAISS.from_documents(docs, embeddings)

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.4,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    qa = RetrievalQA.from_chain_type(llm=llm, retriever=db.as_retriever())
    return qa
