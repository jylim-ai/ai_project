from langchain_google_genai import ChatGoogleGenerativeAI

def generate_resume_description(resume_text: str) -> str:
    """
    Summarize resume and extract skills, experience, and preferences.
    """
    # Initialize a chat LLM (Google Gemini)
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        temperature=0.7  # optional
    )

    prompt = f"""
    Extract a short and professional summary from the following resume text. 
    Include:
    - Key skills
    - Work experience highlights
    - Job preferences (if mentioned)
    
    Resume:
    {resume_text}

    Output:
    plain text string
    """

    # `invoke()` returns a response object
    response = llm.invoke(prompt)
    # The text can be in `response.text` or `response.content_blocks`
    return response.text