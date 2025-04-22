from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

openrouter_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY")
)