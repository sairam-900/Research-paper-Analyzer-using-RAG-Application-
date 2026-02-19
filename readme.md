📚 AI Research Paper Assistant

An AI-powered web application that allows users to upload research papers (PDF) and interact with them through an intelligent chatbot.
The assistant analyzes the paper, generates structured summaries, and answers context-aware questions using Google Gemini AI.

🚀 Features

📄 Upload research paper (PDF)

🧠 Automatic structured analysis:

Title

Abstract Summary

Key Findings

Methodology

Limitations

💬 Context-aware chatbot Q&A

🔐 Secure API key management using .env

🔁 Exponential backoff retry mechanism

🎨 Modern glassmorphism UI design

⚡ Real-time chat interface

🏗️ Tech Stack
🎨 Frontend

HTML5

CSS3

JavaScript (Vanilla JS)

Fetch API for backend communication

⚙️ Backend

Python

Flask

pdfplumber (PDF text extraction)

requests (API communication)

markdown (convert AI response to HTML)

python-dotenv (environment variables)

🤖 AI Integration

1)Google Gemini API

2)Context-based Q&A system

3)Structured research analysis generation

🧠 How It Works

1)User uploads a PDF research paper

2)Backend extracts text using pdfplumber

3)Extracted content is sent to Gemini API

4)Gemini generates structured summary

5)User asks questions

6)Chat endpoint answers using provided research context

7)Responses are rendered as formatted HTML

🛠️ Installation Guide
1️⃣ Clone Repository
git clone https://github.com/your-username/research-assistant-ai.git
cd research-assistant-ai

2️⃣ Create Virtual Environment
py -m venv venv
venv\Scripts\activate

3️⃣ Install Dependencies
pip install flask python-dotenv requests pdfplumber markdown

4️⃣ Create .env File
GOOGLE_API_KEY=your_google_api_key_here

5️⃣ Run Application
python main.py


Open browser:

http://127.0.0.1:5000


📂 Project Structure
research-assistant-ai/
│
├── templates/
│   └── index.html
│
├── main.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md

🔐 Security

API key stored securely in .env

.env excluded from Git via .gitignore

No API keys exposed in frontend

🎯 Use Cases

Research scholars

Engineering students

Academic reviewers

Literature review automation

Research summarization



👨‍💻 Author

N Leela Sai Ram Nakka
B.Tech – Electronics & Communication Engineering