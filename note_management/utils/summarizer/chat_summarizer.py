from llm.openrouter_client import openrouter_client
import os
from dotenv import load_dotenv

load_dotenv()

def summarize_chat(model: str = os.environ.get("OPENROUTER_MODEL"), content : list = [] ) -> str:
    res = openrouter_client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system", 
                "content": """
                You are a bot whose only job is to distill the list of chat messages between a user and an assistant, 
                which user will provide, into a single summary message with these requirements:
                - Covers the entire conversation in chronological order (from oldest to newest),
                - Includes as many specific details as possible,
                - Avoids omitting important facts or decisions made during the conversation.
                The provided list of messages starts from newest to oldest messages.
                Retain the original flow of the dialogue, and ensure your summary is just a short mini paragraph to describe the convesation.
                **If the provided list is empty, just reply with "No Chat History".**
                """
            },
            {
                "role": "user",
                "content": str(content)
            }
        ]
    )

    return res.choices[0].message.content