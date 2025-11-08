import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import io
from pdfminer.high_level import extract_text
import requests

app = Flask(__name__)

# Allowed upload folder
UPLOAD_FOLDER = '/tmp'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Basic skill dictionary (extend this list as needed)
SKILL_KEYWORDS = [
    "python", "java", "javascript", "html", "css", "react", "flask", "django",
    "machine learning", "deep learning", "nlp", "pandas", "numpy", "sql", "mongodb",
    "aws", "docker", "kubernetes", "git", "excel"
]

# Get Hugging Face API token from environment
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

def extract_text_from_pdf(pdf_bytes):
    """Extract text from PDF file"""
    with io.BytesIO(pdf_bytes) as f:
        text = extract_text(f)
    return text

def extract_skills(text):
    """Simple skill matching using keyword search"""
    text_lower = text.lower()
    found = [skill for skill in SKILL_KEYWORDS if skill in text_lower]
    return list(set(found))

def call_hf_ner_api(text):
    """Call Hugging Face Inference API for Named Entity Recognition"""
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}
    api_url = "https://api-inference.huggingface.co/models/dslim/bert-base-NER"
    payload = {"inputs": text}
    response = requests.post(api_url, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    return response.json()

@app.route("/analyze", methods=["POST"])
def analyze_resume():
    # Accept uploaded file or plain text
    if "file" in request.files:
        file = request.files["file"]
        filename = secure_filename(file.filename)
        pdf_bytes = file.read()
        text = extract_text_from_pdf(pdf_bytes)
    else:
        text = request.form.get("text", "")

    # Extract skills
    skills = extract_skills(text)

    # Run NER
    try:
        ner_result = call_hf_ner_api(text[:1000])  # limit for shorter inference
    except Exception as e:
        ner_result = {"error": str(e)}

    # Compare with optional job description
    job_desc = request.form.get("job_description", "")
    jd_skills = extract_skills(job_desc)
    match_score, matched = None, []
    if jd_skills:
        matched = list(set(skills).intersection(set(jd_skills)))
        match_score = round(len(matched) / len(jd_skills), 2)

    return jsonify({
        "skills_detected": skills,
        "job_match_skills": matched,
        "match_score": match_score,
        "named_entities": ner_result
    })

@app.route("/", methods=["GET"])
def home():
    return "Resume Analyzer Backend is Running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
