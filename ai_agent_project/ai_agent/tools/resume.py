from google import genai
import os
import pathlib
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, List, Union

from langchain_google_genai import GoogleGenerativeAIEmbeddings
import pdfplumber

load_dotenv()  # Loads variables from .env
gemini_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=gemini_key)

def parse_resume(filename: str) -> str:
    """
    Load resume and extract text from file.

    Args:
        filename: File name or path

    Returns:
        text
    """
    path = pathlib.Path(filename)
    text = ""

    if not path.exists():
        raise FileNotFoundError(f"{filename} does not exist")

    if not path.is_file():
        raise ValueError(f"{filename} is not a file")
    ext = Path(path).suffix.lower()
    




    if ext == ".pdf":
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    
    elif ext == ".txt":
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
    
    else:
        raise ValueError("Unsupported file type. Only PDF and TXT allowed.")
    
    return text
        


