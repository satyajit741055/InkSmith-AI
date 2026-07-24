from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from app.config import settings 


llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key = settings.OPENAI_API_KEY
)

# llm = ChatGroq(
#     model="llama-3.1-8b-instant",
#     api_key = settings.GROQ_API_KEY 
# )
