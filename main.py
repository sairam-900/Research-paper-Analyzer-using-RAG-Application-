import os
import time
import requests
import pdfplumber
import markdown  # ✅ ADDED
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # ✅ Enable CORS

# -------- Secure Configuration --------
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env file")

GEMINI_MODEL = "gemini-2.5-flash"

GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"


# -------- Gemini API Call with Retry --------
def call_gemini_with_retry(prompt, system_instruction=""):
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "systemInstruction": {"parts": [{"text": system_instruction}]}
    }

    retries = 5
    for i in range(retries):
        try:
            response = requests.post(GEMINI_URL, json=payload, timeout=30)
            result = response.json()

            if response.status_code == 200:
                return result.get('candidates', [{}])[0]\
                    .get('content', {})\
                    .get('parts', [{}])[0]\
                    .get('text', "")

            if response.status_code in [429, 500, 503]:
                time.sleep(2 ** i)
                continue

            return f"Error: {response.status_code} - {response.text}"

        except Exception as e:
            if i == retries - 1:
                return f"Connection failed after {retries} attempts: {str(e)}"
            time.sleep(2 ** i)

    return "Failed to get response from Gemini."


# -------- PDF Extraction --------
def extract_text_from_pdf(file_path):
    full_text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages[:15]:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
        return full_text
    except Exception as e:
        print(f"Extraction error: {e}")
        return None


# -------- Routes --------
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze_paper():

    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    temp_path = f"temp_{file.filename}"
    file.save(temp_path)

    try:
        content = extract_text_from_pdf(temp_path)

        if not content or len(content.strip()) < 100:
            return jsonify({
                "error": "Could not extract enough text from PDF. Is it scanned?"
            }), 400

        system_prompt = """
        You are a world-class research scientist.
        Analyze the provided text and create a structured report with Markdown:
        # Title
        ## Abstract Summary
        ## Key Findings
        ## Methodology
        ## Limitations
        """

        analysis_markdown = call_gemini_with_retry(
            f"Paper Content:\n{content[:10000]}",
            system_prompt
        )

        # ✅ CONVERT MARKDOWN TO HTML
        analysis_html = markdown.markdown(analysis_markdown)

        return jsonify({
            "analysis": analysis_html,   # HTML now
            "extracted_text": content[:12000]
        })

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


@app.route('/chat', methods=['POST'])
def chat_with_paper():

    data = request.json
    user_query = data.get('query')
    paper_context = data.get('context', "")

    if not user_query:
        return jsonify({"error": "No question provided"}), 400

    system_prompt = f"""
    You are an assistant for 'Research Paper A&A'.
    Use ONLY the provided research paper context to answer.
    If the answer is not in the document, say:
    "The answer is not found in the provided document."

    Context:
    {paper_context}
    """

    answer_markdown = call_gemini_with_retry(user_query, system_prompt)

    # ✅ CONVERT MARKDOWN TO HTML
    answer_html = markdown.markdown(answer_markdown)

    return jsonify({"answer": answer_html})


if __name__ == '__main__':
    app.run(debug=True)
