from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Resume Analyzer backend is running!"

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    # Get resume text from JSON body
    data = request.get_json()
    text = data.get("text", "")

    # Dummy analysis: word count and simple keyword check
    word_count = len(text.split())
    has_python = "python" in text.lower()
    has_ml = "machine learning" in text.lower()

    result = {
        "word_count": word_count,
        "contains_python": has_python,
        "contains_machine_learning": has_ml
    }

    return jsonify(result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
