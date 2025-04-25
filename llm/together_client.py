from together import Together
import os
from dotenv import load_dotenv

load_dotenv()

together_client = Together(
    api_key=os.environ.get("TOGETHER_API_KEY")
)