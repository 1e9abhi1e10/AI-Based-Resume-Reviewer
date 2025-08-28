<p><small>Best View in <a href="https://github.com/settings/appearance">Light Mode</a> and Desktop Site (Recommended)</small></p><br/>

<div align="left">
  <h1> 📥 AI BASED RESUME REVIEWER 📤 </h1>
  <p>A Tool for Resume Analysis, Predictions and Recommendations</p>

## About the Project 📪
<div align="center">
    <p align="justify"> 
      A tool which parses information from a resume using natural language processing and finds the keywords, cluster them onto sectors based on their keywords. 
      And lastly show recommendations, predictions, analytics to the applicant / recruiter based on keyword matching.
    </p>
</div>

## Scope 📈
i. Transforming all resume data into a structured tabular format and CSV enables organizations to utilize the information for analytical purposes.

ii. Users can enhance their resumes by receiving recommendations, predictions, and an overall score through our tool, allowing for continuous testing and improvement.

iii. The user section's enhanced features can contribute to increased traffic on our tool.

iv. Colleges can utilize the tool to gain insights into students' resumes before placements.

v. Obtain analytics on the roles most sought after by users.

vi. Continuous improvement of the tool is facilitated through user feedback.

<!-- TechStack -->
## Tech Stack 📱
<details>
  <summary>Frontend</summary>
  <ul>
    <li><a href="https://streamlit.io/">Streamlit</a></li>
    <li><a href="https://developer.mozilla.org/en-US/docs/Learn/HTML">HTML</a></li>
    <li><a href="https://developer.mozilla.org/en-US/docs/Web/CSS">CSS</a></li>
    <li><a href="https://developer.mozilla.org/en-US/docs/Learn/JavaScript">JavaScript</a></li>
  </ul>
</details>

<details>
  <summary>Backend</summary>
  <ul>
    <li><a href="https://streamlit.io/">Streamlit</a></li>
    <li><a href="https://www.python.org/">Python</a></li>
  </ul>
</details>

<details>
<summary>Modules</summary>
  <ul>
    <li><a href="https://pandas.pydata.org/">pandas</a></li>
    <li><a href="https://github.com/OmkarPathak/pyresparser">pyresparser</a></li>
    <li><a href="https://pypi.org/project/pdfminer3/">pdfminer3</a></li>
    <li><a href="https://plotly.com/">Plotly</a></li>
    <li><a href="https://www.nltk.org/">NLTK</a></li>
  </ul>
</details>

<details>
<summary>Database</summary>
  <ul>
    <li><a href="https://www.sqlite.org/">SQLite</a> (default, file-based)</li>
  </ul>
</details>

<!-- Features -->
## Features 🔎
### Client-Side: -
- Utilizing Parsing Techniques to Retrieve Location and Miscellaneous Data
  - Extracting Basic Info, Skills, and Keywords

- New: Paste a Job Description (JD) and see a JD-match score with top missing keywords
- New: DOCX upload support (PDF and DOCX are both supported)
- New: Refreshed UI/theme for better readability

Employing logical programs to provide recommendations on:
- Additional skills
- Predicted job role
- Relevant courses and certificates
- Resume tips and ideas
- Overall Score
- Access to Interview & Resume tip videos

### Data & Storage:
- Local persistence via SQLite (no external DB needed by default)
- Visitor counter with DB tracking and session-based fallback

## How It Works ⚙️
1) Upload & Pre-processing
- User uploads a resume as PDF or DOCX. PDFs are previewed inline; DOCX is parsed directly.
- Text is extracted via pdfminer.six (PDF) or docx2txt (DOCX).
- pyresparser + spaCy (en_core_web_sm) + NLTK tokenize and extract: name, email, phone, degree, skills, and page count.

2) Skill & Field Inference
- Extracted skills are matched against curated keyword lists to infer a likely field (e.g., Data Science, Web, Android, iOS, UI/UX).
- Based on the inferred field, the app recommends additional skills and relevant courses (from `App/Courses.py`).

3) Resume Heuristics Scoring
- A ruleset checks for presence of common sections: Objective/Summary, Education, Experience/Internships, Skills, Hobbies/Interests, Achievements, Certifications, Projects.
- A progress bar visualizes the computed score.

4) JD Match Scoring (Optional)
- User pastes a Job Description (JD). The app tokenizes JD text, removes stopwords, and compares against resume tokens + extracted skills.
- It outputs a JD-match percentage and a list of top missing keywords to add to the resume.

5) Results & Extras
- Displays extracted basics, score, recommendations, and two helpful videos (resume tips and interview tips).
- Data can be stored to the local SQLite DB for admin analytics (optional).

## System Architecture 🧭
- UI: Streamlit app (`App/App.py`)
- Parsing Layer:
  - PDF: pdfminer.six
  - DOCX: docx2txt
  - NLP: spaCy (en_core_web_sm), NLTK (stopwords)
  - pyresparser for entity/skill extraction (uses spaCy internally)
- Heuristics & Recommendations: Python rule-based logic + keyword lists
- Storage: SQLite (`resume_reviewer.db`) created at runtime (no external setup)
- Visualization: Plotly for charts (admin/feedback analytics)

## Technologies Used 🧰
- Streamlit, Python 3.10+
- spaCy, NLTK, pyresparser
- pdfminer.six, docx2txt
- pandas, plotly, streamlit-tags
- SQLite (default) or MySQL (optional, if you re-enable connector)

## Security & Privacy 🔒
- PII (name, email, phone) may be parsed for display and optional storage.
- By default, data is stored locally in SQLite; for production, use a managed DB and restrict access.
- Avoid uploading confidential documents to public deployments.
- No third-party API calls are required for core functionality.

## Deployment Options 🚀
- Streamlit Community Cloud: simplest. Connect GitHub repo and deploy.
- Render/Railway/Fly.io: containerize (Docker) if you need more control or background workers.
- Vercel (not recommended for Streamlit directly): use only if you split into a FastAPI backend + Next.js frontend.

## Limitations & Future Enhancements 🧪
- OCR for image-based/scanned PDFs not enabled (could add Tesseract + pytesseract).
- JD match uses keyword overlap; a semantic matcher (e.g., embeddings) could improve quality.
- Multilingual resumes are not deeply supported; add locale detection and language-specific models for best results.

### Admin-Side: -
- Aggregating all applicant data in a tabular format
- Downloading user data in CSV format
- Viewing all saved uploaded PDFs in the Uploaded Resume folder
- Collecting user feedback and ratings
  
  Generating Pie Charts for: -
- Ratings
- Predicted fields/roles
- Experience levels
- Resume scores
- User counts
- City, State, and Country breakdown

### Feedback System: -
- Easy-to-fill forms
- Rating scale from 1 to 5
- Displaying an overall ratings pie chart
- Providing a history of past user comments 

## Requirements 🔐
### Ensure a Smooth Process by Installing the Following:
1) Python 3.10+ (3.11–3.13 recommended): [Download Python](https://www.python.org/downloads/)
2) Visual Studio Code **(Preferred Code Editor)**: [Download VS Code](https://code.visualstudio.com/Download)

## Setup & Installation 👀

To run this project, perform the following tasks 😨

Download the code file manually or via git
```bash
git clone https://github.com/1e9abhi1e10/AI-Based-Resume-Reviewer.git
```

Create a virtual environment and activate it **(recommended)**

Open your terminal and change your project directory to ```AI-Based-Resume-Reviewer``` and run the following: 
```bash
python -m venv venv
# macOS/Linux
source venv/bin/activate
# Windows (PowerShell)
venv\Scripts\Activate.ps1
```

Install dependencies (minimal set to run the app):
```bash
cd App
pip install streamlit pandas plotly streamlit-tags docx2txt nltk pyresparser pdfminer.six geopy geocoder

# Models/data downloads
python -m spacy download en_core_web_sm
python -c "import nltk; nltk.download('stopwords')"
```

Run the app:
```bash
streamlit run App.py
```

Notes:
- The app defaults to SQLite (creates a local file automatically). No DB setup needed.
- If you want to use MySQL instead, restore the original connector in `App/App.py` and ensure credentials/DB exist.

## Usage
- After the setup it will do stuff's automatically
- You just need to upload a resume and see it's magic
- Try first with my resume uploaded in ``Uploaded_Resumes`` folder
- Admin userid is ``admin`` and password is ``admin@resume-Reviewer``

### New UI/Feature Tips
- Paste a JD in the new textarea to see the JD match score and missing keywords.
- Upload DOCX or PDF; PDFs show inline preview, DOCX is analyzed without preview.
- The sidebar theme is dark with improved contrast for selections.

## Troubleshooting
- If you see spaCy or NLTK errors, re-run:
```bash
python -m spacy download en_core_web_sm
python -c "import nltk; nltk.download('stopwords')"
```
- If `pyresparser` throws model/config warnings, they are safe; we load the standard spaCy model by default.
