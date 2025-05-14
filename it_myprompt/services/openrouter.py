from langchain_openai import ChatOpenAI

from it_myprompt.settings import Settings

settings = Settings()


async def get_llm():
    llm = ChatOpenAI(
        api_key=settings.OPENROUTER_API_KEY,
        model_name=settings.OPENROUTER_MODEL,
        base_url=settings.OPENROUTER_API_URL,
    )
    yield llm
