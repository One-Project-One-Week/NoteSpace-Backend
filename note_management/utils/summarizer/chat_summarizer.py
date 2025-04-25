from llm.together_client import together_client

def summarize_chat(model: str = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo", content : str = "") -> str:
    res = together_client.chat.completions.create(
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
                The provided list of messages starts from newest to oldest messages and includes roles and content in each dictionary.
                Retain the original flow of the dialogue, and ensure your summary reflects the full context accurately.
                If the provided list is empty, just reply with "No Chat History".
                """
            },
            {
                "role": "user",
                "content": content
            }
        ]
    )

    print(res.choices[0].message.content)