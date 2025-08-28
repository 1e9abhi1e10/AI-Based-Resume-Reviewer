

###### Required Packages ######
import streamlit as st # core package used in this project
import pandas as pd
import base64, random
import time,datetime
import os
import socket
import platform
import geocoder
import secrets
import io,random
import re
from PIL import Image
import plotly.express as px # to create visualisations at the admin session
import plotly.graph_objects as go
from geopy.geocoders import Nominatim
from streamlit_tags import st_tags
import docx2txt

# Ensure NLTK stopwords are present BEFORE importing pyresparser (which requires them at import time)
import nltk
_ = nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords

# spaCy model bootstrap (used by pyresparser at runtime)
import spacy
from spacy.cli import download as spacy_download
try:
    spacy.load('en_core_web_sm')
except OSError:
    try:
        spacy_download('en_core_web_sm')
    except Exception:
        pass

# libraries used to parse the pdf files
from pdfminer.high_level import extract_text as pdf_extract_text
from pyresparser.resume_parser import ResumeParser
from Courses import ds_course,web_course,android_course,ios_course,uiux_course,resume_videos,interview_videos


###### Preprocessing functions ######


# Generates a link allowing the data in a given panda dataframe to be downloaded in csv format 
def get_csv_download_link(df,filename,text):
    csv = df.to_csv(index=False)
    ## bytes conversions
    b64 = base64.b64encode(csv.encode()).decode()      
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href


# Reads Pdf file and check_extractable
def pdf_reader(file):
    try:
        return pdf_extract_text(file) or ''
    except Exception:
        return ''


# show uploaded file path to view pdf_display
def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


# read resume text for pdf/docx
def read_resume_text(file_path):
    if file_path.lower().endswith('.pdf'):
        return pdf_reader(file_path)
    if file_path.lower().endswith('.docx'):
        try:
            return docx2txt.process(file_path) or ''
        except Exception:
            return ''
    return ''


# course recommendations which has data already loaded from Courses.py
def course_recommender(course_list):
    st.subheader("**Courses & Certificates Recommendations 👨‍🎓**")
    c = 0
    rec_course = []
    ## slider to choose from range 1-10
    no_of_reco = st.slider('Choose Number of Course Recommendations:', 1, 10, 5)
    random.shuffle(course_list)
    for c_name, c_link in course_list:
        c += 1
        st.markdown(f"({c}) [{c_name}]({c_link})")
        rec_course.append(c_name)
        if c == no_of_reco:
            break
    return rec_course


###### Database Stuffs ######

import sqlite3
import os

# sql connector (use SQLite for simplicity and reliability)
try:
    # Create SQLite database file
    db_path = 'resume_reviewer.db'
    connection = sqlite3.connect(db_path, check_same_thread=False)
    cursor = connection.cursor()
    print("SQLite database connected successfully")
except Exception as e:
    print(f"Database connection error: {e}")
    connection = None
    cursor = None


# inserting miscellaneous data, fetched results, prediction and recommendation into user_data table
def insert_data(sec_token,ip_add,host_name,dev_user,os_name_ver,latlong,city,state,country,act_name,act_mail,act_mob,name,email,res_score,timestamp,no_of_pages,reco_field,cand_level,skills,recommended_skills,courses,pdf_name):
    if cursor is None or connection is None:
        return
    insert_sql = """INSERT INTO user_data (
        sec_token, ip_add, host_name, dev_user, os_name_ver, latlong, city, state, country,
        act_name, act_mail, act_mob, Name, Email_ID, resume_score, Timestamp, Page_no,
        Predicted_Field, User_level, Actual_skills, Recommended_skills, Recommended_courses, pdf_name
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    rec_values = (str(sec_token),str(ip_add),host_name,dev_user,os_name_ver,str(latlong),city,state,country,act_name,act_mail,act_mob,name,email,str(res_score),timestamp,str(no_of_pages),reco_field,cand_level,skills,recommended_skills,courses,pdf_name)
    cursor.execute(insert_sql, rec_values)
    connection.commit()


# inserting feedback data into user_feedback table
def insertf_data(feed_name,feed_email,feed_score,comments,Timestamp):
    if cursor is None or connection is None:
        return
    insertfeed_sql = """INSERT INTO user_feedback (
        feed_name, feed_email, feed_score, comments, Timestamp
    ) VALUES (?, ?, ?, ?, ?)"""
    rec_values = (feed_name, feed_email, feed_score, comments, Timestamp)
    cursor.execute(insertfeed_sql, rec_values)
    connection.commit()


###### Setting Page Configuration (favicon, Logo, Title) ######


st.set_page_config(
   page_title="AI Based Resume Reviewer",
   page_icon='./Logo/Recommend.png',
)


# Simple visual theme improvements
def apply_theme():
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
            html, body, [class*="css"]  { font-family: 'Inter', sans-serif; }
            h1, h2, h3, h4 { font-weight: 700; }
            /* Elevate cards */
            .stApp { background: linear-gradient(180deg, #ffffff 0%, #f7f9fc 100%); }
            section.main > div { padding-top: 0.5rem; }
            /* Buttons */
            .stButton>button {
                border-radius: 10px;
                border: 1px solid #e8e8e8;
                background: #1f6feb;
                color: white;
                padding: 0.5rem 1rem;
            }
            .stButton>button:hover { filter: brightness(0.95); }
            /* Progress bars */
            .stProgress > div > div > div > div { background: linear-gradient(90deg,#d73b5c,#f59f00); }
            /* Tags */
            .stTags [data-baseweb="tag"] { border-radius: 8px; }
            /* Sidebar */
            [data-testid="stSidebar"] { background: #0f172a; }
            [data-testid="stSidebar"] * { color: #e2e8f0 !important; }
            /* Sidebar selectbox (activities) */
            [data-testid="stSidebar"] [data-baseweb="select"] > div {
                background: #1e293b !important;
                color: #e2e8f0 !important;
                border-radius: 10px;
                border: 1px solid #334155;
            }
            [data-testid="stSidebar"] [data-baseweb="select"] svg { fill: #94a3b8; }
            [data-testid="stSidebar"] [data-baseweb="select"] input { color: #e2e8f0 !important; }
            [data-testid="stSidebar"] [data-baseweb="popover"] [role="listbox"] {
                background: #0b1220 !important;
                color: #e2e8f0 !important;
                border: 1px solid #334155;
            }
            [data-testid="stSidebar"] [data-baseweb="popover"] [role="option"] {
                color: #e2e8f0 !important;
            }
            [data-testid="stSidebar"] [data-baseweb="popover"] [role="option"][aria-selected="true"] {
                background: #334155 !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


###### Main function run() ######


def run():
    apply_theme()
    st.markdown("""
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:8px">
      <span style="font-size:28px">📄</span>
      <div>
        <div style="font-size:22px;font-weight:700;line-height:1">AI Based Resume Reviewer</div>
        <div style="font-size:13px;color:#475569">Analyze, match with JD, and get smart suggestions</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # (Logo, Heading, Sidebar etc)
    try:
        img = Image.open('./Logo/Resume.jpeg')
        st.image(img)
    except FileNotFoundError:
        st.title("AI Based Resume Reviewer")
    st.sidebar.markdown("# Choose Something...")
    activities = ["User", "Feedback", "About", "Admin"]
    choice = st.sidebar.selectbox("Choose among the given options:", activities)
    st.sidebar.info("Upload your resume and optionally paste a JD to get a match score.")

    ###### Creating Database and Table ######


    # Create table user_data and user_feedback
    if cursor is not None:
        # Create user_data table
        table_sql = """CREATE TABLE IF NOT EXISTS user_data (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    sec_token TEXT NOT NULL,
                    ip_add TEXT,
                    host_name TEXT,
                    dev_user TEXT,
                    os_name_ver TEXT,
                    latlong TEXT,
                    city TEXT,
                    state TEXT,
                    country TEXT,
                    act_name TEXT NOT NULL,
                    act_mail TEXT NOT NULL,
                    act_mob TEXT NOT NULL,
                    Name TEXT NOT NULL,
                    Email_ID TEXT NOT NULL,
                    resume_score TEXT NOT NULL,
                    Timestamp TEXT NOT NULL,
                    Page_no TEXT NOT NULL,
                    Predicted_Field TEXT NOT NULL,
                    User_level TEXT NOT NULL,
                    Actual_skills TEXT NOT NULL,
                    Recommended_skills TEXT NOT NULL,
                    Recommended_courses TEXT NOT NULL,
                    pdf_name TEXT NOT NULL
                )"""
        cursor.execute(table_sql)

        # Create user_feedback table
        tablef_sql = """CREATE TABLE IF NOT EXISTS user_feedback (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    feed_name TEXT NOT NULL,
                    feed_email TEXT NOT NULL,
                    feed_score TEXT NOT NULL,
                    comments TEXT,
                    Timestamp TEXT NOT NULL
                )"""
        cursor.execute(tablef_sql)
        
        # Create visitors table
        visitors_table_sql = """CREATE TABLE IF NOT EXISTS visitors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    visit_date DATE DEFAULT CURRENT_DATE,
                    visit_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ip_address TEXT
                )"""
        cursor.execute(visitors_table_sql)
        
        connection.commit()


    ###### CODE FOR CLIENT SIDE (USER) ######

    if choice == 'User':
        
        # Collecting Miscellaneous Information
        act_name = st.text_input('Name*')
        act_mail = st.text_input('Mail*')
        act_mob  = st.text_input('Mobile Number*')
        sec_token = secrets.token_urlsafe(12)
        host_name = socket.gethostname()
        ip_add = socket.gethostbyname(host_name)
        # Resolve username safely in container/cloud (os.getlogin can fail without a TTY)
        try:
            dev_user = os.getlogin()
        except Exception:
            import getpass
            dev_user = os.getenv('USER') or os.getenv('USERNAME') or getpass.getuser() or 'unknown'
        os_name_ver = platform.system() + " " + platform.release()
        g = geocoder.ip('me')
        latlong = g.latlng
        geolocator = Nominatim(user_agent="http")
        location = geolocator.reverse(latlong, language='en')
        address = location.raw['address']
        cityy = address.get('city', '')
        statee = address.get('state', '')
        countryy = address.get('country', '')  
        city = cityy
        state = statee
        country = countryy

        # Local visitor counter
        if cursor is not None:
            try:
                # Insert this visit
                insert_visit_sql = "INSERT INTO visitors (ip_address) VALUES (?)"
                cursor.execute(insert_visit_sql, (ip_add,))
                connection.commit()
                
                # Get total visitors count
                cursor.execute("SELECT COUNT(*) FROM visitors")
                total_visitors = cursor.fetchone()[0]
                
                # Get today's visitors (SQLite date format)
                from datetime import date
                today = date.today().strftime('%Y-%m-%d')
                cursor.execute("SELECT COUNT(*) FROM visitors WHERE date(visit_date) = ?", (today,))
                today_visitors = cursor.fetchone()[0]
                
                st.sidebar.markdown(f"""
                ### 📊 Visitor Statistics
                **Total Visitors:** {total_visitors:,}
                **Today:** {today_visitors}
                """)
            except Exception as e:
                st.sidebar.markdown("### 📊 Visitor Counter")
                st.sidebar.info("Counter temporarily unavailable")
        else:
            # Simple session-based counter when database is not available
            if 'visitor_count' not in st.session_state:
                st.session_state.visitor_count = 1
            else:
                st.session_state.visitor_count += 1
            
            st.sidebar.markdown(f"""
            ### 📊 Visitor Counter
            **Session Visits:** {st.session_state.visitor_count}
            """)


        # Optional Job Description input
        jd_text = st.text_area('Paste the Job Description (optional)', height=160, help='We will compare your resume to this JD to estimate relevance and suggest missing keywords.')

        # Upload Resume
        st.markdown('''<h5 style='text-align: left; color: #021659;'>✨ Upload Your Resume, And Get Smart Recommendations</h5>''',unsafe_allow_html=True)
        
        ## file upload in pdf format
        pdf_file = st.file_uploader("Choose your Resume", type=["pdf","docx"])
        if pdf_file is not None:
            with st.spinner('Hang On While We Cook Magic For You...'):
                time.sleep(4)
        
            ### saving the uploaded resume to folder
            save_image_path = './Uploaded_Resumes/'+pdf_file.name
            pdf_name = pdf_file.name
            with open(save_image_path, "wb") as f:
                f.write(pdf_file.getbuffer())
            if pdf_name.lower().endswith('.pdf'):
                show_pdf(save_image_path)
            else:
                st.info('DOCX uploaded. Preview is not shown; analysis will proceed below.')

            ### parsing and extracting whole resume 
            resume_data = ResumeParser(save_image_path).get_extracted_data()
            if resume_data:
                
                ## Get the whole resume data into resume_text
                resume_text = read_resume_text(save_image_path)

                ## Showing Analyzed data from (resume_data)
                st.markdown('''<h3>🧠 Resume Analysis</h3>''', unsafe_allow_html=True)
                st.success("Hello "+ resume_data['name'])
                st.subheader("**Your Basic info 👀**")
                try:
                    st.text('Name: '+resume_data['name'])
                    st.text('Email: ' + resume_data['email'])
                    st.text('Contact: ' + resume_data['mobile_number'])
                    st.text('Degree: '+str(resume_data['degree']))                    
                    st.text('Resume pages: '+str(resume_data['no_of_pages']))

                except:
                    pass
                ## Predicting Candidate Experience Level 

                ### Trying with different possibilities
                cand_level = ''
                if resume_data['no_of_pages'] < 1:                
                    cand_level = "NA"
                    st.markdown( '''<h4 style='text-align: left; color: #d73b5c;'>You are at Fresher level!</h4>''',unsafe_allow_html=True)
                
                #### if internship then intermediate level
                elif 'INTERNSHIP' in resume_text:
                    cand_level = "Intermediate"
                    st.markdown('''<h4 style='text-align: left; color: #1ed760;'>You are at intermediate level!</h4>''',unsafe_allow_html=True)
                elif 'INTERNSHIPS' in resume_text:
                    cand_level = "Intermediate"
                    st.markdown('''<h4 style='text-align: left; color: #1ed760;'>You are at intermediate level!</h4>''',unsafe_allow_html=True)
                elif 'Internship' in resume_text:
                    cand_level = "Intermediate"
                    st.markdown('''<h4 style='text-align: left; color: #1ed760;'>You are at intermediate level!</h4>''',unsafe_allow_html=True)
                elif 'Internships' in resume_text:
                    cand_level = "Intermediate"
                    st.markdown('''<h4 style='text-align: left; color: #1ed760;'>You are at intermediate level!</h4>''',unsafe_allow_html=True)
                
                #### if Work Experience/Experience then Experience level
                elif 'EXPERIENCE' in resume_text:
                    cand_level = "Experienced"
                    st.markdown('''<h4 style='text-align: left; color: #fba171;'>You are at experience level!''',unsafe_allow_html=True)
                elif 'WORK EXPERIENCE' in resume_text:
                    cand_level = "Experienced"
                    st.markdown('''<h4 style='text-align: left; color: #fba171;'>You are at experience level!''',unsafe_allow_html=True)
                elif 'Experience' in resume_text:
                    cand_level = "Experienced"
                    st.markdown('''<h4 style='text-align: left; color: #fba171;'>You are at experience level!''',unsafe_allow_html=True)
                elif 'Work Experience' in resume_text:
                    cand_level = "Experienced"
                    st.markdown('''<h4 style='text-align: left; color: #fba171;'>You are at experience level!''',unsafe_allow_html=True)
                else:
                    cand_level = "Fresher"
                    st.markdown('''<h4 style='text-align: left; color: #fba171;'>You are at Fresher level!!''',unsafe_allow_html=True)


                ## Skills Analyzing and Recommendation
                st.subheader("**💡 Skills Recommendation**")
                
                ### Current Analyzed Skills
                keywords = st_tags(label='### Your Current Skills',
                text='See our skills recommendation below',value=resume_data['skills'],key = '1  ')

                ### Keywords for Recommendations
                ds_keyword = ['tensorflow','keras','pytorch','machine learning','deep Learning','flask','streamlit']
                web_keyword = ['react', 'django', 'node jS', 'react js', 'php', 'laravel', 'magento', 'wordpress','javascript', 'angular js', 'C#', 'Asp.net', 'flask']
                android_keyword = ['android','android development','flutter','kotlin','xml','kivy']
                ios_keyword = ['ios','ios development','swift','cocoa','cocoa touch','xcode']
                uiux_keyword = ['ux','adobe xd','figma','zeplin','balsamiq','ui','prototyping','wireframes','storyframes','adobe photoshop','photoshop','editing','adobe illustrator','illustrator','adobe after effects','after effects','adobe premier pro','premier pro','adobe indesign','indesign','wireframe','solid','grasp','user research','user experience']
                n_any = ['english','communication','writing', 'microsoft office', 'leadership','customer management', 'social media']
                ### Skill Recommendations Starts                
                recommended_skills = []
                reco_field = ''
                rec_course = ''

                ### condition starts to check skills from keywords and predict field
                for i in resume_data['skills']:
                
                    #### Data science recommendation
                    if i.lower() in ds_keyword:
                        print(i.lower())
                        reco_field = 'Data Science'
                        st.success("** Our analysis says you are looking for Data Science Jobs.**")
                        recommended_skills = ['Data Visualization','Predictive Analysis','Statistical Modeling','Data Mining','Clustering & Classification','Data Analytics','Quantitative Analysis','Web Scraping','ML Algorithms','Keras','Pytorch','Probability','Scikit-learn','Tensorflow',"Flask",'Streamlit']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                        text='Recommended skills generated from System',value=recommended_skills,key = '2')
                        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job</h5>''',unsafe_allow_html=True)
                        # course recommendation
                        rec_course = course_recommender(ds_course)
                        break

                    #### Web development recommendation
                    elif i.lower() in web_keyword:
                        print(i.lower())
                        reco_field = 'Web Development'
                        st.success("** Our analysis says you are looking for Web Development Jobs **")
                        recommended_skills = ['React','Django','Node JS','React JS','php','laravel','Magento','wordpress','Javascript','Angular JS','c#','Flask','SDK']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                        text='Recommended skills generated from System',value=recommended_skills,key = '3')
                        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h5>''',unsafe_allow_html=True)
                        # course recommendation
                        rec_course = course_recommender(web_course)
                        break

                    #### Android App Development
                    elif i.lower() in android_keyword:
                        print(i.lower())
                        reco_field = 'Android Development'
                        st.success("** Our analysis says you are looking for Android App Development Jobs **")
                        recommended_skills = ['Android','Android development','Flutter','Kotlin','XML','Java','Kivy','GIT','SDK','SQLite']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                        text='Recommended skills generated from System',value=recommended_skills,key = '4')
                        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h5>''',unsafe_allow_html=True)
                        # course recommendation
                        rec_course = course_recommender(android_course)
                        break

                    #### IOS App Development
                    elif i.lower() in ios_keyword:
                        print(i.lower())
                        reco_field = 'IOS Development'
                        st.success("** Our analysis says you are looking for IOS App Development Jobs **")
                        recommended_skills = ['IOS','IOS Development','Swift','Cocoa','Cocoa Touch','Xcode','Objective-C','SQLite','Plist','StoreKit',"UI-Kit",'AV Foundation','Auto-Layout']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                        text='Recommended skills generated from System',value=recommended_skills,key = '5')
                        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h5>''',unsafe_allow_html=True)
                        # course recommendation
                        rec_course = course_recommender(ios_course)
                        break

                    #### Ui-UX Recommendation
                    elif i.lower() in uiux_keyword:
                        print(i.lower())
                        reco_field = 'UI-UX Development'
                        st.success("** Our analysis says you are looking for UI-UX Development Jobs **")
                        recommended_skills = ['UI','User Experience','Adobe XD','Figma','Zeplin','Balsamiq','Prototyping','Wireframes','Storyframes','Adobe Photoshop','Editing','Illustrator','After Effects','Premier Pro','Indesign','Wireframe','Solid','Grasp','User Research']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                        text='Recommended skills generated from System',value=recommended_skills,key = '6')
                        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h5>''',unsafe_allow_html=True)
                        # course recommendation
                        rec_course = course_recommender(uiux_course)
                        break

                    #### For Not Any Recommendations
                    elif i.lower() in n_any:
                        print(i.lower())
                        reco_field = 'NA'
                        st.warning("** Currently our tool only predicts and recommends for Data Science, Web, Android, IOS and UI/UX Development**")
                        recommended_skills = ['No Recommendations']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                        text='Currently No Recommendations',value=recommended_skills,key = '6')
                        st.markdown('''<h5 style='text-align: left; color: #092851;'>Maybe Available in Future Updates</h5>''',unsafe_allow_html=True)
                        # course recommendation
                        rec_course = "Sorry! Not Available for this Field"
                        break


                ## Resume Scorer & Resume Writing Tips
                st.subheader("**📝 Resume Tips & Ideas**")
                resume_score = 0
                
                ### Predicting Whether these key points are added to the resume
                if 'Objective' or 'Summary' in resume_text:
                    resume_score = resume_score+6
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Objective/Summary</h4>''',unsafe_allow_html=True)                
                else:
                    st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add your career objective, it will give your career intension to the Recruiters.</h4>''',unsafe_allow_html=True)

                if 'Education' or 'School' or 'College'  in resume_text:
                    resume_score = resume_score + 12
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Education Details</h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add Education. It will give Your Qualification level to the recruiter</h4>''',unsafe_allow_html=True)

                if 'EXPERIENCE' in resume_text:
                    resume_score = resume_score + 16
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Experience</h4>''',unsafe_allow_html=True)
                elif 'Experience' in resume_text:
                    resume_score = resume_score + 16
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Experience</h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add Experience. It will help you to stand out from crowd</h4>''',unsafe_allow_html=True)

                if 'INTERNSHIPS'  in resume_text:
                    resume_score = resume_score + 6
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Internships</h4>''',unsafe_allow_html=True)
                elif 'INTERNSHIP'  in resume_text:
                    resume_score = resume_score + 6
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Internships</h4>''',unsafe_allow_html=True)
                elif 'Internships'  in resume_text:
                    resume_score = resume_score + 6
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Internships</h4>''',unsafe_allow_html=True)
                elif 'Internship'  in resume_text:
                    resume_score = resume_score + 6
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Internships</h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add Internships. It will help you to stand out from crowd</h4>''',unsafe_allow_html=True)

                if 'SKILLS'  in resume_text:
                    resume_score = resume_score + 7
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Skills</h4>''',unsafe_allow_html=True)
                elif 'SKILL'  in resume_text:
                    resume_score = resume_score + 7
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Skills</h4>''',unsafe_allow_html=True)
                elif 'Skills'  in resume_text:
                    resume_score = resume_score + 7
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Skills</h4>''',unsafe_allow_html=True)
                elif 'Skill'  in resume_text:
                    resume_score = resume_score + 7
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Skills</h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add Skills. It will help you a lot</h4>''',unsafe_allow_html=True)

                if 'HOBBIES' in resume_text:
                    resume_score = resume_score + 4
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Hobbies</h4>''',unsafe_allow_html=True)
                elif 'Hobbies' in resume_text:
                    resume_score = resume_score + 4
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Hobbies</h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add Hobbies. It will show your personality to the Recruiters and give the assurance that you are fit for this role or not.</h4>''',unsafe_allow_html=True)

                if 'INTERESTS'in resume_text:
                    resume_score = resume_score + 5
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Interest</h4>''',unsafe_allow_html=True)
                elif 'Interests'in resume_text:
                    resume_score = resume_score + 5
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Interest</h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add Interest. It will show your interest other that job.</h4>''',unsafe_allow_html=True)

                if 'ACHIEVEMENTS' in resume_text:
                    resume_score = resume_score + 13
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Achievements </h4>''',unsafe_allow_html=True)
                elif 'Achievements' in resume_text:
                    resume_score = resume_score + 13
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Achievements </h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add Achievements. It will show that you are capable for the required position.</h4>''',unsafe_allow_html=True)

                if 'CERTIFICATIONS' in resume_text:
                    resume_score = resume_score + 12
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Certifications </h4>''',unsafe_allow_html=True)
                elif 'Certifications' in resume_text:
                    resume_score = resume_score + 12
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Certifications </h4>''',unsafe_allow_html=True)
                elif 'Certification' in resume_text:
                    resume_score = resume_score + 12
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Certifications </h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add Certifications. It will show that you have done some specialization for the required position.</h4>''',unsafe_allow_html=True)

                if 'PROJECTS' in resume_text:
                    resume_score = resume_score + 19
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Projects</h4>''',unsafe_allow_html=True)
                elif 'PROJECT' in resume_text:
                    resume_score = resume_score + 19
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Projects</h4>''',unsafe_allow_html=True)
                elif 'Projects' in resume_text:
                    resume_score = resume_score + 19
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Projects</h4>''',unsafe_allow_html=True)
                elif 'Project' in resume_text:
                    resume_score = resume_score + 19
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Projects</h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add Projects. It will show that you have done work related the required position or not.</h4>''',unsafe_allow_html=True)

                st.subheader("**📊 Resume Score**")
                
                st.markdown(
                    """
                    <style>
                        .stProgress > div > div > div > div {
                            background-color: #d73b5c;
                        }
                    </style>""",
                    unsafe_allow_html=True,
                )

                ### Score Bar
                my_bar = st.progress(0)
                score = 0
                for percent_complete in range(resume_score):
                    score +=1
                    time.sleep(0.1)
                    my_bar.progress(percent_complete + 1)

                ### Score
                st.success('** Your Resume Writing Score: ' + str(score)+'**')
                st.warning("** Note: This score is calculated based on the content that you have in your Resume. **")

                # JD Match Scoring (optional)
                st.subheader("**🔍 Job Description Match**")
                if jd_text and isinstance(jd_text, str) and len(jd_text.strip()) > 0:
                    # Extract simple keyword sets from JD and resume
                    try:
                        stop_words = set(stopwords.words('english'))
                    except Exception:
                        stop_words = set()

                    def tokenize(text):
                        tokens = re.findall(r"[A-Za-z][A-Za-z+.#\-]*", text.lower())
                        return [t for t in tokens if t not in stop_words and len(t) > 1]

                    jd_tokens = set(tokenize(jd_text))
                    resume_tokens = set(tokenize(resume_text))
                    skills_tokens = set([s.lower() for s in (resume_data.get('skills') or [])])

                    # Combine resume text tokens and extracted skills
                    resume_all = resume_tokens.union(skills_tokens)

                    if len(jd_tokens) == 0:
                        st.info('The provided Job Description does not contain enough keywords to score.')
                    else:
                        matched = jd_tokens.intersection(resume_all)
                        match_ratio = int(round((len(matched) / len(jd_tokens)) * 100))

                        # Progress bar for JD match
                        jd_bar = st.progress(0)
                        for pct in range(match_ratio):
                            time.sleep(0.01)
                            jd_bar.progress(pct + 1)
                        st.success('** JD Match Score: ' + str(match_ratio) + '% **')

                        # Show missing top keywords (up to 15)
                        missing = sorted(list(jd_tokens - resume_all))
                        if missing:
                            st.markdown("**Top missing keywords to consider adding:**")
                            st.write(', '.join(missing[:15]))
                        else:
                            st.markdown("Great! Your resume covers the JD keywords well.")
                else:
                    st.info('Paste a Job Description above to see the JD-match score and suggestions.')

                # print(str(sec_token), str(ip_add), (host_name), (dev_user), (os_name_ver), (latlong), (city), (state), (country), (act_name), (act_mail), (act_mob), resume_data['name'], resume_data['email'], str(resume_score), timestamp, str(resume_data['no_of_pages']), reco_field, cand_level, str(resume_data['skills']), str(recommended_skills), str(rec_course), pdf_name)


                ### Getting Current Date and Time
                ts = time.time()
                cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                timestamp = str(cur_date+'_'+cur_time)


                ## Calling insert_data to add all the data into user_data                
                insert_data(str(sec_token), str(ip_add), (host_name), (dev_user), (os_name_ver), (latlong), (city), (state), (country), (act_name), (act_mail), (act_mob), resume_data['name'], resume_data['email'], str(resume_score), timestamp, str(resume_data['no_of_pages']), reco_field, cand_level, str(resume_data['skills']), str(recommended_skills), str(rec_course), pdf_name)

                ## Recommending Resume Writing Video
                st.header("**Bonus Video for Resume Writing Tips💡**")
                resume_vid = random.choice(resume_videos)
                st.video(resume_vid)

                ## Recommending Interview Preparation Video
                st.header("**Bonus Video for Interview Tips💡**")
                interview_vid = random.choice(interview_videos)
                st.video(interview_vid)

                ## On Successful Result 
                st.balloons()

            else:
                st.error('Something went wrong..')                


    ###### CODE FOR FEEDBACK SIDE ######
    elif choice == 'Feedback':   
        
        # timestamp 
        ts = time.time()
        cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        timestamp = str(cur_date+'_'+cur_time)

        # Feedback Form
        with st.form("my_form"):
            st.write("Feedback form")            
            feed_name = st.text_input('Name')
            feed_email = st.text_input('Email')
            feed_score = st.slider('Rate Us From 1 - 5', 1, 5)
            comments = st.text_input('Comments')
            Timestamp = timestamp        
            submitted = st.form_submit_button("Submit")
            if submitted:
                ## Calling insertf_data to add dat into user feedback
                insertf_data(feed_name,feed_email,feed_score,comments,Timestamp)    
                ## Success Message 
                st.success("Thanks! Your Feedback was recorded.") 
                ## On Successful Submit
                st.balloons()    


        # query to fetch data from user feedback table
        if connection is not None and cursor is not None:
            try:
                query = 'select * from user_feedback'        
                plotfeed_data = pd.read_sql(query, connection)                        

                # fetching feed_score from the query and getting the unique values and total value count 
                labels = plotfeed_data.feed_score.unique()
                values = plotfeed_data.feed_score.value_counts()

                # plotting pie chart for user ratings
                st.subheader("**Past User Rating's**")
                fig = px.pie(values=values, names=labels, title="Chart of User Rating Score From 1 - 5", color_discrete_sequence=px.colors.sequential.Aggrnyl)
                st.plotly_chart(fig)

                #  Fetching Comment History
                cursor.execute('select feed_name, comments from user_feedback')
                plfeed_cmt_data = cursor.fetchall()

                st.subheader("**User Comment's**")
                dff = pd.DataFrame(plfeed_cmt_data, columns=['User', 'Comment'])
                st.dataframe(dff, width=1000)
            except Exception as e:
                st.error("Unable to load feedback data. Database connection issue.")
                st.info("Feedback form still works for submitting new feedback.")
        else:
            st.info("Database not connected. Feedback form still works for submitting new feedback.")

    
    ###### CODE FOR ABOUT PAGE ######
    elif choice == 'About':   

        st.subheader("**About The Tool - AI Based Resume Reviewer**")

        st.markdown('''

        <p align='justify'>
            A tool which parses information from a resume using natural language processing and finds the keywords, cluster them onto sectors based on their keywords. And lastly show recommendations, predictions, analytics to the applicant based on keyword matching.
        </p>

        <p align="justify">
            <b>How to use it: -</b> <br/><br/>
            <b>User -</b> <br/>
            In the Side Bar choose yourself as user and fill the required fields and upload your resume in pdf format.<br/>
            Just sit back and relax our tool will do the magic on it's own.<br/><br/>
            <b>Feedback -</b> <br/>
            A place where user can suggest some feedback about the tool.<br/><br/>
            <b>Admin -</b> <br/>
            For login use <b>admin</b> as username and <b>admin@resume-Reviewer</b> as password.<br/>
            It will load all the required stuffs and perform analysis.
        </p><br/><br/>


        ''',unsafe_allow_html=True)  


    ###### CODE FOR ADMIN SIDE (ADMIN) ######
    else:
        st.success('Welcome to Admin Side')

        #  Admin Login
        ad_user = st.text_input("Username")
        ad_password = st.text_input("Password", type='password')

        if st.button('Login'):
            
            ## Credentials 
            if ad_user == 'admin' and ad_password == 'admin@resume-Reviewer':
                
                if connection is not None and cursor is not None:
                    try:
                        ### Fetch miscellaneous data from user_data(table) and convert it into dataframe
                        cursor.execute('''SELECT ID, ip_add, resume_score, Predicted_Field, User_level, city, state, country from user_data''')
                        datanalys = cursor.fetchall()
                        plot_data = pd.DataFrame(datanalys, columns=['Idt', 'IP_add', 'resume_score', 'Predicted_Field', 'User_Level', 'City', 'State', 'Country'])
                        
                        ### Total Users Count with a Welcome Message
                        values = plot_data.Idt.count()
                        st.success("Welcome Abhishek ! Total %d " % values + " User's Have Used Our Tool : )")                
                        
                        ### Fetch user data from user_data(table) and convert it into dataframe
                        cursor.execute('''SELECT ID, sec_token, ip_add, act_name, act_mail, act_mob, Predicted_Field, Timestamp, Name, Email_ID, resume_score, Page_no, pdf_name, User_level, Actual_skills, Recommended_skills, Recommended_courses, city, state, country, latlong, os_name_ver, host_name, dev_user from user_data''')
                        data = cursor.fetchall()                

                        st.header("**User's Data**")
                        df = pd.DataFrame(data, columns=['ID', 'Token', 'IP Address', 'Name', 'Mail', 'Mobile Number', 'Predicted Field', 'Timestamp',
                                                         'Predicted Name', 'Predicted Mail', 'Resume Score', 'Total Page',  'File Name',   
                                                         'User Level', 'Actual Skills', 'Recommended Skills', 'Recommended Course',
                                                         'City', 'State', 'Country', 'Lat Long', 'Server OS', 'Server Name', 'Server User',])
                        
                        ### Viewing the dataframe
                        st.dataframe(df)
                        
                        ### Downloading Report of user_data in csv file
                        st.markdown(get_csv_download_link(df,'User_Data.csv','Download Report'), unsafe_allow_html=True)
                    except Exception as e:
                        st.error("Database connection error. Admin features unavailable.")
                else:
                    st.error("Database not connected. Admin features unavailable.")

            ## For Wrong Credentials
            else:
                st.error("Wrong ID & Password Provided")

# Calling the main (run()) function to make the whole process run
run()
