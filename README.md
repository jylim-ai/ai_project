# AI Agentic Job Seeker

## Overview

Smart Job Finder is a full-stack application designed to help job seekers automatically find and match jobs based on their resumes. It combines AI-powered resume parsing, semantic search, and a modern React frontend for a smooth user experience.

Key technologies:

Resume parsing: Extract skills, experience, and education from PDFs/DOCX

Job matching: Use keywords or FAISS embeddings to rank relevant jobs

RAG (Retrieval-Augmented Generation): Summarize jobs or suggest improvements

React frontend: Upload resumes, view job matches, and filter results

## Tech Stack

### Backend (Python):

FastAPI 

Pdfplumber → Resume parsing

Google AI → Extract skills, job titles, experience

FAISS → Semantic search of jobs 

BeautifulSoup → Job scraping

Frontend (React):

Upload resume

Display matched jobs


## Setup

Backend (Python)

AI server and client

```
cd ai_agent_project
python -m venv venv
venv\Scripts\activate
pip install -r dev-requirements.txt
cd ai_agent
python server.py
python client.py
```

Frontend (React)

```
cd ai_agent_project
npm install
npm start
```

## Environment Variables

Create a .env file in backend/ for API keys or paths:

```
GEMINI_API_KEY=your_openai_api_key
FINDWORK_API_KEY=f02d6ca7a69ceaff54c1ff64f591cdd61187c823
```

