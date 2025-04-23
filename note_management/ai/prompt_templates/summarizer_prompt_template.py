from langchain.prompts import PromptTemplate, FewShotPromptTemplate

examples = [
    {
        "notes": """
        Meeting Notes - Project Planning
        Date: 2024-04-22
        Attendees: John, Sarah, Mike
        
        Key Points:
        - Project deadline extended to June 15
        - New feature requirements discussed
        - Budget approved for additional resources
        - Next meeting scheduled for May 1st
        """,
        "summary": "The project planning meeting on April 22nd involved John, Sarah, and Mike. Key decisions included extending the deadline to June 15, discussing new feature requirements, approving additional budget, and scheduling the next meeting for May 1st."
    },
    {
        "notes": """
        Research Notes - AI Integration
        Topics Covered:
        1. Machine Learning Models
           - Supervised vs Unsupervised
           - Deep Learning applications
        2. Data Requirements
           - Minimum 1000 samples needed
           - Data preprocessing steps
        3. Implementation Timeline
           - Phase 1: 2 weeks
           - Phase 2: 3 weeks
        """,
        "summary": "Research notes cover AI integration topics including machine learning models (supervised/unsupervised learning and deep learning applications), data requirements (1000+ samples and preprocessing), and a 5-week implementation timeline split into two phases."
    },
    {
        "notes": """
        Daily Journal - April 21
        Morning:
        - Completed code review
        - Fixed bug in authentication
        Afternoon:
        - Team standup meeting
        - Started new feature implementation
        Evening:
        - Documentation updates
        - Planning for tomorrow
        """,
        "summary": "April 21st journal entry details a productive day including code review, bug fixes, team standup, new feature work, documentation updates, and planning for the next day."
    }
]

example_prompt = PromptTemplate.from_template(template="Notes: {notes}\nSummary: {summary}")

system_prompt = """
You are a note summarizer for the "Note Space" web app. Your job is to provide concise, accurate, and detailed summaries of the provided notes.

Guidelines:
1. Focus on key points and main ideas
2. Maintain key entities and their relationships
3. Include important details and context
4. Keep the summary simple enough for a 16-year-old to understand
5. Preserve any critical dates, names, or numbers
6. Provide only the summary without any additional commentary or interpretation

Here are some examples:
"""

prompt_template = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix=system_prompt,
    suffix="Notes: {notes}\nSummary:",
)