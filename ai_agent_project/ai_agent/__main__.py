# TODO: Update the main function to your needs or remove it.
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import requests
import pandas as pd
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
from google import genai
from bs4 import BeautifulSoup


load_dotenv()  # Loads variables from .env

gemini_key = os.getenv("GEMINI_API_KEY")
if not gemini_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables!")


# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client(api_key=gemini_key)

findwork_key = os.getenv("FINDWORK_API_KEY")



response2 = requests.get("https://findwork.dev/api/jobs/?search=Meta", headers={
    "Authorization": f"Token {findwork_key}"
})



def main() -> None:
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

    vectorstore = FAISS.load_local(
        "job_embeddings",
        embeddings,
        allow_dangerous_deserialization=True
    )

    print("FAISS loaded:", vectorstore.index.ntotal)

    results = vectorstore.similarity_search("Results-driven Software Engineer with over five years of experience building scalable web applications, backend systems, and cloud-based solutions. Proficient in Python, JavaScript, Java, React, Node.js, FastAPI, Django, PostgreSQL, AWS, Docker, and Kubernetes. At ABC Technologies, designed and implemented REST APIs serving over one million monthly users and optimized system performance by 35%. Also experienced in building responsive frontend features and integrating APIs. Holds AWS Certified Solutions Architect and Google Professional Cloud Developer certifications, seeking challenging Software Engineer roles.", k=5)

    return [
        {
            "title": r.metadata.get("title", ""),
            "company": r.metadata.get("company", ""),
            "employment_type": r.metadata.get("employment_type", ""),
            "url": r.metadata.get("url", ""),
        }
        for r in results
    ]





if __name__ == "__main__":
    main()
