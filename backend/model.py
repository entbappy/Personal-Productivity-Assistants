import os
from dotenv import load_dotenv
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.chains.question_answering import load_qa_chain
import gdown


#Download .env file from gdrive
file_id = "1bWTsTptKjVsPiFxFQslIJwMcGwF2779h"
url = f"https://drive.google.com/uc?id={file_id}"
output = ".env"  # Change the filename as needed

gdown.download(url, output, quiet=False)


# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "db")

# Ensure API key is set
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API Key not found in .env")



# Load stored vector database
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
vector_db = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings)
retriever = vector_db.as_retriever()


# Use GPT-4 for answer generation
llm = ChatOpenAI(model_name="gpt-4", openai_api_key=OPENAI_API_KEY)

# Create Retrieval-Augmented Generation (RAG) Chain
# Load the QA Chain properly
qa_chain = load_qa_chain(
    llm=llm, 
    chain_type="stuff"
)

def get_response(query):
    docs = retriever.get_relevant_documents(query)
    return qa_chain.run(input_documents=docs, question=query)
