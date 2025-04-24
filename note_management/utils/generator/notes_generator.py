from llm.groq_client import groq_client

def generate_notes(model: str = "llama-3.3-70b-versatile", content: str="") -> str:
    
    response = groq_client.chat.completions.create(
    model=model, 
    messages=[
        {
            "role": "system",
            "content": """
                You are an AI assistant designed to convert raw educational text (extracted from a PDF) into well-structured study notes. Your goal is to organize the content clearly using Quill.js-compatible HTML tags.

                Use these tags appropriately:

                <h1> for main topic titles

                <h2> for subtopics

                <p> for general explanations and paragraphs

                <ul> and <li> for bullet points

                <strong> to bold key terms or definitions

                <em> to emphasize important phrases

                <blockquote> for quotes or referenced content

                <br> to add line spacing between blocks of content when it improves readability (like between headings and lists or after paragraphs)

                Rules:

                Return only valid HTML that works in Quill.js.

                Use <br> tags for line spacing, but don’t spam them—just enough to give breathing room between logical sections.

                Don’t add extra commentary or text outside the HTML.

                Focus on summarizing and organizing the key concepts clearly.

                Format the output as clean student notes—ready for copy-pasting into a Quill.js editor.
            """

        },
        {
            "role": "user",
            "content": content
        }
    ]
)


    
    return response.choices[0].message.content