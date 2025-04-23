from llm.openrouter_client import openrouter_client

def generate_notes(model: str = "mistralai/mistral-7b-instruct:free", content: str="") -> str:
    
    response = openrouter_client.chat.completions.create(
        model=model, 
        messages=[
            {
                "role": "system",
                "content": """
                    You are a note generation assistant. 
                    You will be provided a text and you need to generate notes from it like a highschool student would note.
                    Response should only include notes without any commentary or interpretation.
                    Instead of special characters as markups, use HTML tags which are supported in Quill JS text editor.
                    Don't write long sentences, use short sentences or bullet points.
                    Don't add the title of the next in the notes. 
                    """
            },
            {
                "role": "user",
                "content": content
            }
        ]
    )
    
    return response.choices[0].message.content