from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_deepseek import ChatDeepSeek
from app.config import settings


def get_llm():
    if settings.ENVIRONMENT == "local":
        return ChatGroq(
            model="openai/gpt-oss-120b",
            api_key=settings.GROQ_API_KEY,
        )

    return ChatDeepSeek(
        model="deepseek-v4-flash",
        api_key=settings.DEEPSEEK_API_KEY,
        reasoning_effort="none"
    )
