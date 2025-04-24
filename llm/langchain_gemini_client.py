from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()

genai_client = ChatGoogleGenerativeAI(
    model=os.environ.get("GOOGLE_MODEL"),
    temperature=0.0,
    max_retries=2,
    api_key=os.environ.get("GOOGLE_API_KEY")
)