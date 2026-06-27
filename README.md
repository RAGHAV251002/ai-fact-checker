# 🕵️ AI Fact-Checking Web App

An AI-powered web application that automatically extracts factual claims from PDF documents, verifies them using live web data, and generates a downloadable verification report.

## 🚀 Live Demo

**Streamlit App:**
https://ai-fact-checker-yuzvbgavppcsh88zkbpdsf.streamlit.app/

**GitHub Repository:**
https://github.com/RAGHAV251002/ai-fact-checker/tree/main

---

## 📌 Project Overview

Marketing documents, reports, and presentations often contain outdated or incorrect statistics. This application acts as a **Truth Layer** by:

* Extracting factual claims from uploaded PDFs
* Searching the live web for supporting evidence
* Verifying each claim using Google's Gemini model
* Classifying claims as:

  * ✅ Verified
  * ❌ False
  * 🟡 Outdated
  * ⚪ Insufficient Evidence
* Generating downloadable JSON, CSV, and PDF reports

---

## ✨ Features

* 📄 Upload PDF documents
* 🤖 AI-powered claim extraction using Gemini
* 🌐 Live web verification using Tavily Search API
* 🧠 AI-based fact verification
* 📊 Verification dashboard with summary metrics
* 🔗 Source URLs for every verified claim
* ⬇️ Download reports in JSON, CSV, and PDF formats

---

## 🏗️ Tech Stack

### Frontend

* Streamlit

### Backend

* Python

### AI Models

* Google Gemini 2.5 Flash

### Search API

* Tavily Search API

### PDF Processing

* PyMuPDF

### Report Generation

* Pandas
* ReportLab

---

## 📂 Project Structure

```text
ai-fact-checker/
│
├── app.py
├── requirements.txt
├── README.md
│
├── services/
│   ├── pdf_parser.py
│   ├── gemini_service.py
│   ├── search_service.py
│   ├── verification_service.py
│   ├── report_generator.py
│   └── fact_checker.py
│
├── utils/
│   └── json_parser.py
│
└── .streamlit/
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPO_URL
cd ai-fact-checker
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

### Windows

```bash
venv\Scripts\activate
```

### macOS/Linux

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

---

## 🧠 Workflow

1. Upload a PDF.
2. Extract text from the document.
3. Identify factual claims using Gemini.
4. Search the live web using Tavily.
5. Verify claims using Gemini.
6. Display verification results.
7. Download the final report.

---

## 📊 Verification Categories

| Status                  | Description                                       |
| ----------------------- | ------------------------------------------------- |
| ✅ Verified              | The claim matches reliable web evidence.          |
| ❌ False                 | The claim contradicts reliable evidence.          |
| 🟡 Outdated             | The claim was once true but is no longer current. |
| ⚪ Insufficient Evidence | Not enough reliable information is available.     |

---

## 📦 Output Reports

The application generates:

* JSON Report
* CSV Report
* PDF Report

---

## 📸 Demo

Record a short demo showing:

* Uploading a PDF
* Claim extraction
* Verification process
* Report generation
* Report downloads

---

## 👨‍💻 Author

**Ayush Raghav**

Product Management & AI Enthusiast

---

## 📄 License

This project was developed as part of a Product Management technical assessment and is intended for educational and evaluation purposes.
