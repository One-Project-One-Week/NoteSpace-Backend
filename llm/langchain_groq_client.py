from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

groq_client = ChatGroq(
    model=os.environ.get("GROQ_MODEL"),
    temperature=0.0,
    max_retries=2,
    api_key=os.environ.get("GROQ_API_KEY")
)