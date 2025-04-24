from llm.openrouter_client import openrouter_client

def generate_notes(model: str = "mistralai/mistral-7b-instruct:free", content: str="") -> str:
    
    response = openrouter_client.chat.completions.create(
        model=model, 
        messages=[
            {
                "role": "system",
                "content": """
                    You are a note-taking assistant designed to help students summarize text into study notes.

                    Your task is to convert a given input into concise, clear notes, as a high school student might write. Follow these guidelines:

                    - Only output the notes—do not include any explanations, interpretations, or commentary.
                    - Format the notes using **HTML tags** supported by **Quill JS** (e.g., `<h1>`, `<p>`, `<strong>`, `<blockquote>`, `<ol>`, `<li>`).
                    - Use short, direct sentences or bullet points instead of long paragraphs.
                    - Do **not** include the title of the original content in the notes.
                    - Avoid any markup characters like `*` or `-`; use proper HTML structure.
                    - Only include important concise points and details.
                    - Keep it as concise as possible.
                    - Only reply with the formatted notes. Do not include anything else.

                    Example format:

                    <h1>Short Girls Are Better</h1>
                    <p><br></p>
                    <blockquote><strong>Why?</strong></blockquote>
                    <ol><li data-list="bullet">They're short</li><li data-list="bullet">They're not tall</li></ol>
                    <p><br></p>
                    <blockquote>How to choose?</blockquote>
                    <ol><li data-list="ordered">Less than <strong>5'2"</strong></li></ol>
                    <p><br></p>
                    """
            },
            {
                "role": "user",
                "content": content
            }
        ]
    )
    
    return response.choices[0].message.content