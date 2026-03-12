import asyncio
import os
import pathlib
import httpx
import json
from dotenv import load_dotenv
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp import ClientSession
from pydantic import BaseModel, Field
from typing import List
from google import genai
from google.genai import types
from fastapi import FastAPI
from langchain.agents import create_agent
from langchain.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_core.prompts import ChatPromptTemplate


from langchain_core.output_parsers import PydanticOutputParser
from job_parser import extract_jobs
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()  # Loads variables from .env

# -------- CONFIG --------
MODEL = "gemini-2.5-flash"
# ------------------------

# gemini_key = os.getenv("GEMINI_API_KEY")
# client = genai.Client(api_key=gemini_key)












app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SYSTEM_PROMPT = """
You are an AI agent that matches jobs to a candidate's resume.

Responsibilities:
1. Parse Resume
2. Summarize Resume
3. Compare each job's required skills, experience against the candidate's resume by semantic search.
4. Search the top 5 suitable jobs.
5. For each selected job, output a dictionary containing:
   - job_title
   - company
   - URL
6. Final top 5 selected job output MUST be:
   - A list of dictionaries
   - No explanations
   - No markdown
   - No extra text
   - No JSON string, only dict format
7. You may call external tools when necessary, but avoid unnecessary tool usage.

Rules:
- Scoring must be consistent and explainable.
- Output must be structured and machine-readable.
- Do not invent job requirements not present in the job description.
"""





messages = {}

model = ChatGoogleGenerativeAI(
    model=MODEL
)

client = MultiServerMCPClient(
    {
        "job-ai-agent": {
            "transport": "stdio",
            "command": "python",
            "args": ["server.py"],
        }
    }
)

class SkillsOutput(BaseModel):
    name: str
    skills: List[str]
    work: List[str]
    education: List[str]
    

async def run_agent(user_input: str):

    async with client.session("job-ai-agent") as session:
        tools = await load_mcp_tools(session)

        await extract_jobs()

        messages["messages"] = user_input

        # ---- Load MCP tools ----
        tools_response = await client.get_tools()
        print(tools_response)

        agent = create_agent(
            model, 
            tools=tools,
            system_prompt=SYSTEM_PROMPT)

        
        response = await agent.ainvoke(messages)

        msg = response
        print(messages)
        print(msg)

            # ---- Final answer ----
        for message in reversed(msg["messages"]):
            # Use a tuple for multiple types
            if isinstance(message, (AIMessage, ToolMessage)):
                try:
                    # 1. GET the raw string first
                    raw_text = message.content[0]['text']
                    
                    # 2. CLEAN the string (Replace Python's 'None' with JSON's 'null')
                    json_ready_text = raw_text.replace("None", "null")
                    
                    # 3. PARSE the cleaned string
                    jobs = json.loads(json_ready_text)
                    
                    print("\n🤖 Agent Response:\n")
                    print(jobs)
                    
                    # 4. LOOP through the parsed list
                    for i, job in enumerate(jobs, 1):
                        print(f"\n🔹 Job {i}")
                        # Use .get() to avoid KeyError if a key is missing
                        print(f"Title           : {job.get('title') or job.get('job_title', 'N/A')}")
                        print(f"Company         : {job.get('company', 'N/A')}")
                        print(f"Employment Type : {job.get('employment_type', 'N/A')}")
                        print(f"URL             : {job.get('url') or job.get('URL', 'N/A')}")
                        print("-" * 50)

                    return jobs
                    
                    
                except (json.JSONDecodeError, KeyError, IndexError) as e:
                    # Skip messages that don't contain the job JSON
                    continue

@app.post("/match_resume")
async def main(file: UploadFile = File(...)):
    # Save uploaded file temporarily
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())
    temp_name = file.filename
    jobs_result = await run_agent(f"temp_{temp_name}")
    return {"jobs_result": jobs_result}


