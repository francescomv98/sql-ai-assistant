from langchain_openai import ChatOpenAI
from src.config.settings import settings

class OpenAIClient:
    def __init__(self):
        self.model = ChatOpenAI(
            model=settings.openai_model,
            api_key=settings.openai_api_key,
            temperature=0
        )

    def get_model(self) -> ChatOpenAI:
        return self.model