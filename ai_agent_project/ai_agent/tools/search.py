from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Load once at startup
embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001"
)

vectorstore = FAISS.load_local(
    "job_embeddings",
    embeddings,
    allow_dangerous_deserialization=True
)

print("FAISS loaded:", vectorstore.index.ntotal)


def search_jobs(resume_description: str, k: int = 5) -> list:
    

    """
    Search for the most relevant job postings based on a candidate's resume or experience.
    
    Args:
        resume_description: A text description of skills and experience.
        k: The number of job results to return (default is 5).

    """
    results = vectorstore.similarity_search(resume_description, k=k)

    return [
        {
            "title": r.metadata.get("title", ""),
            "company": r.metadata.get("company", ""),
            "employment_type": r.metadata.get("employment_type", ""),
            "url": r.metadata.get("url", ""),
        }
        for r in results
    ]