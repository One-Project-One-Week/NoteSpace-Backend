from langchain.prompts import PromptTemplate, FewShotPromptTemplate

examples = [
    {
        "notes": """
        Understanding Docker Containers

        Docker containers are lightweight, standalone packages that include everything needed to run a piece of software. Think of them like shipping containers for code - they keep your application and all its dependencies together in one place.

        Key Components:
        - Dockerfile: A recipe that tells Docker how to build your container
        - Image: A snapshot of your application and its environment
        - Container: A running instance of an image
        - Docker Hub: A repository for sharing Docker images

        Benefits:
        - Consistency across different environments
        - Easy deployment and scaling
        - Isolation between applications
        - Resource efficiency compared to virtual machines

        Common Commands:
        docker build -t myapp .    # Build an image
        docker run myapp          # Run a container
        docker ps                 # List running containers
        docker stop container_id  # Stop a container
        """,
        "summary": """
        - Docker containers are lightweight packages containing all software dependencies
        - Dockerfile defines how to build a container
        - Images are static snapshots of applications and their environments
        - Containers are running instances of Docker images
        - Docker Hub serves as a repository for sharing container images
        - Containers ensure consistency across different environments
        - Docker provides application isolation and resource efficiency
        - Key commands: build (docker build), run (docker run), list (docker ps), stop (docker stop)
        """
    },
    {
        "notes": """
        Understanding Git Version Control

        Git is a distributed version control system that helps track changes in source code during software development. It allows multiple developers to work on the same project simultaneously.

        Key Concepts:
        - Repository: A storage location for your project files and version history
        - Commit: A snapshot of changes made to files
        - Branch: A separate line of development
        - Merge: Combining changes from different branches

        Basic Commands:
        git init          # Initialize a new repository
        git add .         # Stage all changes
        git commit -m "message"  # Save changes with a description
        git push         # Upload changes to remote repository
        git pull         # Download changes from remote repository
        """,
        "summary": """
        - Git is a distributed version control system for tracking code changes
        - Repository stores project files and version history
        - Commits create snapshots of file changes
        - Branches enable parallel development paths
        - Merging combines changes from different branches
        - Key commands: init, add, commit, push, pull
        """
    },
]

example_prompt = PromptTemplate.from_template(
    template="Notes: {notes}\nSummary:\n{summary}"
)

system_prompt = """
You are a notes-summarizer of NoteSpace app.

Your job is to read user-written notes and return a bullet-point summary of key ideas only. 
Each point should clearly preserve important entities, their relationships, and necessary details, but without additional commentary or explanations.

Guidelines:
- Use clear and simple bullet points (start each with a dash `-`)
- No introductory or abstract paragraph — just bullet points
- Maintain key entities and how they relate to each other
- Include essential facts (names, numbers, tools, concepts, etc.)
- Avoid filler, interpretations, or restating definitions unless critical
- Keep it short, focused, and easy to understand

Examples are provided below.
"""

prompt_template = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix=system_prompt,
    suffix="Notes: {notes}\nSummary:",
    input_variables=["notes"],
    example_separator="\n\n"
)