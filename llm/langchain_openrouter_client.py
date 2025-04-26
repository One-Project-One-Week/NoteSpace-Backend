from langchain_openai import ChatOpenAI
from pydantic import Field, SecretStr
from typing import Optional
from dotenv import load_dotenv
import os


load_dotenv()

class ChatOpenRouter(ChatOpenAI):
    
    openai_api_key: Optional[SecretStr] = Field(
        alias="api_key",
        default_factory=os.environ.get("OPENROUTER_API_KEY"),
    )
    
    @property
    def lc_secrets(self) -> dict[str, str]:
        return {"openai_api_key": "OPENROUTER_API_KEY"}

    def __init__(self,
                 openai_api_key: Optional[str] = None,
                 **kwargs):
        openai_api_key = (
            openai_api_key or os.environ.get("OPENROUTER_API_KEY")
        )
        super().__init__(
            base_url="https://openrouter.ai/api/v1",
            openai_api_key=openai_api_key,
            **kwargs
        )

openrouter_client = ChatOpenRouter(
    model_name="mistralai/mistral-7b-instruct:free",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
    temperature=0.0,
    max_retries=4
)