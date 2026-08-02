from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from app.config import settings


llm_groq = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=settings.GROQ_API_KEY,
)

# llm_groq = ChatOpenAI(
#     model="gpt-4.1-nano-2025-04-14",
#     api_key=settings.OPENAI_API_KEY,
# )


