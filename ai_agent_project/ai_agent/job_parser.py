import os
import re
from bs4 import BeautifulSoup
from langchain_community.vectorstores import FAISS
from google import genai
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
import requests
from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env
findwork_key = os.getenv("FINDWORK_API_KEY")

async def extract_jobs():
    









    res = requests.get(f"https://findwork.dev/api/jobs/?search=Meta&source=hn", headers={
        "Authorization": f"Token {findwork_key}"
    })
    data = res.json()

    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001"
    )

    texts = [BeautifulSoup(job["text"], "html.parser").get_text(separator="\n").strip() for job in data.get("results", [])]
    metadatas = [
        {
            "title": job["role"],
            "company": job["company_name"],
            "employment_type": job["employment_type"],
            "url": job["url"],
        }
        for job in data.get("results", [])
    ]
    



    vectorstore = FAISS.from_texts(texts=texts, embedding=embeddings, metadatas=metadatas)
    vectorstore.save_local("job_embeddings")
    print("✅ Job embeddings saved.")
    