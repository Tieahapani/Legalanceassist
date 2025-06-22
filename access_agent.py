import os
from config import GOOGLE_API_KEY
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.genai import types
import asyncio

APP_NAME = "legalance_app"
USER_ID = "user123"
SESSION_ID = "abc123"

# Create Gemini agent with Google Search
root_agent = Agent(
    name="search_agent",
    model="gemini-2.0-flash",
    description="Agent that uses Google Search to fetch immigration-related information.",
    instruction="You are an expert at finding immigration-related info using Google Search. Return the best snippet possible.",
    tools=[google_search]
)

session_service = InMemorySessionService()

async def create_session():
    await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)

asyncio.run(create_session())

runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)

def search_with_gemini(query):
    content = types.Content(role='user', parts=[types.Part(text=query)])
    events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)

    for event in events:
        if event.is_final_response():
            parts = event.content.parts 
            text = parts[0].text 
            link = "https://www.google.com/search?q=" + query.replace(" ", "+")
            return text, link 

    return "Sorry, no information found."  # ✅ Moved outside loop
