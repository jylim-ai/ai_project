import csv

def save_job(title: str, company: str, score: int, url: str) -> str:
    with open("matched_jobs.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([title, company, score, url])
    return "saved"
