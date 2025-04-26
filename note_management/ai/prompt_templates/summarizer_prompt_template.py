from langchain.prompts import PromptTemplate, FewShotPromptTemplate

examples = [
    {
        "notes": """
        What is Agentic AI?

        Agentic AI refers to systems that can autonomously perceive, plan, and act based on goals, context, and environment. Instead of just calling a single LLM for one task, agentic AIs can break down a problem, decide which tools to use, make decisions in sequence, and adapt based on outcomes.

        So it's kinda like giving your AI a mini brain that thinks, decides, and acts—sort of like an assistant who can actually handle multiple steps for you without you manually telling it every time.
        🧰 LangChain + LangGraph
        These two tools help make Agentic AI easier to build:

        LangChain (LC)
        A Python framework that helps connect LLMs with other tools (APIs, databases, file systems, etc.)

        It gives structure to prompt engineering and lets you build chains of actions (like calling a search tool, then feeding that into GPT, then summarizing it).

        Helps create agents with tool use (like a calculator, browser, memory, etc.).

        Example: You can define an agent that, when asked a question, checks a database, runs a calculation, and explains the result back to the user.

        LangGraph
        A newer addition (built on top of LangChain), which lets you define agent workflows as graphs.

        Unlike LangChain's basic chains (linear), LangGraph allows for branching, loops, and state transitions.

        Think of it like drawing a flowchart of how the AI should behave, and then letting it run through that automatically.

        It uses a graph of nodes (functions or decision points) and edges (conditions for transitions). Super useful when your AI needs to go back and forth, retry stuff, or loop until it's confident.

        🌐 Example Use Case (That I might try myself later 😅)
        Use Case: Research Assistant Agent
        Tools: LangChain for tool wrappers + LangGraph for managing flow

        Workflow:

        User asks a question.

        Agent searches the web (ToolNode).

        Extracts the relevant content (ParserNode).

        Summarizes the info using GPT (LLMNode).

        If confidence < 80%, it loops back to search again with refined query (via LangGraph state).

        Finally returns a summarized + cited response.

        🔥 Bonus: Can store past answers and learn over time using LangChain memory.

        📝 Why this is cool (from my POV)
        You get more than just a Q&A bot—it's like a mini worker that thinks.

        LangGraph makes it easier to manage state, loops, retries—so the agent can adapt instead of failing silently.

        Good way to practice system thinking + learn real-world applications of AI.
        """,
        "summary": """
        Agentic AI is a type of artificial intelligence that can make decisions and act independently, using tools and adapting its behavior based on goals and feedback. LangChain and LangGraph are two tools used to build such systems. LangChain helps create structured sequences of tasks using language models and external tools, while LangGraph adds advanced control by letting developers define workflows as graphs with loops and branches. These tools allow developers to build agents that can search for information, analyze results, and respond intelligently, making AI more useful and dynamic in real-world applications.

        Summarized Main Points:

        \n- Agentic AI means AI that can plan, decide, and act by itself based on goals and context.
        \n- LangChain is a Python tool that connects language models with tools like APIs, databases, and more.
        \n- LangChain helps create chains of tasks for agents to follow step-by-step.
        \n- LangGraph builds on LangChain by adding a graph system with branches, loops, and decision-making paths.
        \n- LangGraph lets developers design how the AI behaves in different situations with state transitions.
        \n- Example use case: an AI assistant that searches the web, summarizes results, and retries if confidence is low.
        \n- This assistant can be built using LangChain for tool use and LangGraph for workflow control.
        \n- LangGraph is useful for making AI agents smarter and able to adapt or repeat tasks if needed.
        \n- Developers can use LangChain memory to let the agent remember past interactions.
        """
    },
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
        Docker containers are self-contained packages that bundle applications with their dependencies, ensuring consistent operation across different environments. They work like standardized shipping containers for software, making deployment and scaling more efficient than traditional methods.

        Summarized Main Points:
        \n- Docker containers package applications with all necessary dependencies
        \n- A Dockerfile serves as a blueprint for building container images
        \n- Images are static templates, while containers are running instances
        \n- Docker Hub provides a platform for sharing container images
        \n- Containers offer better resource efficiency than virtual machines
        \n- Docker provides isolation between different applications
        \n- Common commands include building images, running containers, and managing container lifecycle
        \n- Docker simplifies deployment and ensures consistency across development and production
        """
    },
]

example_prompt = PromptTemplate.from_template(template="Notes: {notes}\nSummary: {summary}")

system_prompt = """
You are a note summarizer for the "Note Space" web app. 

Your job is to read user-written notes and generate a structured summary that includes:
1. A short abstract paragraph that gives a high-level overview of the topic.
2. A bullet-point summary highlighting the main points in simple language.

Guidelines:
1. Focus on key points and main ideas
2. Maintain key entities and their relationships
3. Include important details and context but keep it concise
4. Keep summarized points enough for a 16-year-old to understand
5. Preserve any critical dates, names, or numbers
6. Provide only the summary without any additional commentary or interpretation

Here are some examples:
"""

prompt_template = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix=system_prompt,
    suffix="Notes: {notes}\nSummary:\n- Abstract:\n- Summarized Main Points:",
    input_variables=["notes"],
    example_separator="\n\n"
)