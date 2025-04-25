from langchain_together import ChatTogether
import os
from dotenv import load_dotenv

load_dotenv()

together_client = ChatTogether(
    model=os.environ.get("TOGETHER_MODEL"),
    temperature=0.4,
    max_retries=2,
    api_key=os.environ.get("TOGETHER_API_KEY")
)