<p><small>Best View in <a href="https://github.com/settings/appearance">Light Mode</a> and Desktop Site (Recommended)</small></p><br/>

<div align="center">
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
    <li><a href="https://www.mysql.com/">MySQL</a></li>
  </ul>
</details>

<!-- Features -->
## Features 🔎
### Client-Side: -
- Utilizing Parsing Techniques to Retrieve Location and Miscellaneous Data
  - Extracting Basic Info, Skills, and Keywords

Employing logical programs to provide recommendations on:
- Additional skills
- Predicted job role
- Relevant courses and certificates
- Resume tips and ideas
- Overall Score
- Access to Interview & Resume tip videos

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
1) Python: [Download Python](https://www.python.org/downloads/)
2) MySQL: [Download MySQL](https://www.mysql.com/downloads/)
3) Visual Studio Code **(Preferred Code Editor)**: [Download VS Code](https://code.visualstudio.com/Download)
4) Visual Studio Build Tools for C++: [Download VS Build Tools](https://aka.ms/vs/17/release/vs_BuildTools.exe)

## Setup & Installation 👀

To run this project, perform the following tasks 😨

Download the code file manually or via git
```bash
git clone https://github.com/1e9abhi1e10/AI-Based-Resume-Reviewer.git
```

Create a virtual environment and activate it **(recommended)**

Open your command prompt and change your project directory to ```AI-Based-Resume-Reviewer``` and run the following command 
```bash
python -m venv venvapp

cd venvapp/Scripts

activate

```

Downloading packages from ```requirements.txt``` inside ``App`` folder
```bash
cd../..

cd App

pip install -r requirements.txt

python -m spacy download en_core_web_sm

```

After installation is finished create a Database ```cv```

And change user credentials inside ```App.py```
LINK

Go to ```venvapp\Lib\site-packages\pyresparser``` folder

And replace the ```resume_parser.py``` with ```resume_parser.py``` 

which I supplied within the `pyresparser` folder.

``Congratulations 🎉😱, your setup 👆 and installation are complete 😵🤯``

I hope that your ``venvapp`` is activated and working directory is inside ``App``

Run the ```App.py``` file using
```bash
streamlit run App.py

```

## Usage
- After the setup it will do stuff's automatically
- You just need to upload a resume and see it's magic
- Try first with my resume uploaded in ``Uploaded_Resumes`` folder
- Admin userid is ``admin`` and password is ``admin@resume-Reviewer``
