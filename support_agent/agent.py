"""
The support agent.

This is the starter version: a friendly assistant with no business and no rules yet.
In Session 1 you give it a job.
"""

import os

from dotenv import load_dotenv
from google.adk.agents import Agent

# Read the settings in the .env file (your Gemini key and the model name).
# The key is never written in code.
load_dotenv()

# The model name is set in ONE place: GEMINI_MODEL in the .env file.
MODEL = os.environ["GEMINI_MODEL"]

# The instruction is the agent's job description. It tells the model how to behave.
INSTRUCTION = """
You are Kavya, the customer-support assistant for DemoKart.
DemoKart is an online shop in India that sells electronics, home and kitchen items, clothing and footwear.
Customers know you as Kavya from DemoKart.
You are warm, polite and professional, and you use simple English.
At the start of a conversation, greet the customer as DemoKart's support assistant and ask how you can help.
"""

# root_agent is the agent that ADK runs.
root_agent = Agent(
    name="support_agent",
    model=MODEL,
    description="Kavya, the customer-support assistant for DemoKart, an online shop in India.",
    instruction=INSTRUCTION,
)
