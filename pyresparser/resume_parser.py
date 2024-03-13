# Import necessary libraries and modules
import os
import multiprocessing as mp
import io
import spacy
import pprint
from spacy.matcher import Matcher
from . import utils

# Define the ResumeParser class
class ResumeParser(object):

    def __init__(
        self,
        resume,
        skills_file=None,
        custom_regex=None
    ):
        # Load English language model and custom spaCy model
        nlp = spacy.load('en_core_web_sm')
        custom_nlp = spacy.load(os.path.dirname(os.path.abspath(__file__)))

        # Initialize instance variables
        self.__skills_file = skills_file
        self.__custom_regex = custom_regex
        self.__matcher = Matcher(nlp.vocab)
        self.__details = {
            'name': None,
            'email': None,
            'mobile_number': None,
            'skills': None,
            'degree': None,
            'no_of_pages': None,
        }
        self.__resume = resume

        # Extract text from the resume
        if not isinstance(self.__resume, io.BytesIO):
            ext = os.path.splitext(self.__resume)[1].split('.')[1]
        else:
            ext = self.__resume.name.split('.')[1]
        self.__text_raw = utils.extract_text(self.__resume, '.' + ext)
        self.__text = ' '.join(self.__text_raw.split())
        self.__nlp = nlp(self.__text)
        self.__custom_nlp = custom_nlp(self.__text_raw)
        self.__noun_chunks = list(self.__nlp.noun_chunks)
        self.__get_basic_details()

    def get_extracted_data(self):
        # Return the extracted details
        return self.__details

    def __get_basic_details(self):
        # Extract entities using a custom model
        cust_ent = utils.extract_entities_wih_custom_model(self.__custom_nlp)

        # Extract name, email, mobile number, skills, and other basic details
        name = utils.extract_name(self.__nlp, matcher=self.__matcher)
        email = utils.extract_email(self.__text)
        mobile = utils.extract_mobile_number(self.__text, self.__custom_regex)
        skills = utils.extract_skills(
                    self.__nlp,
                    self.__noun_chunks,
                    self.__skills_file
                )

        entities = utils.extract_entity_sections_grad(self.__text_raw)

        # Attempt to extract name from the custom entities, fallback to the extracted name
        try:
            self.__details['name'] = cust_ent['Name'][0]
        except (IndexError, KeyError):
            self.__details['name'] = name

        # Extract email, mobile number, skills, number of pages, and education degree
        self.__details['email'] = email
        self.__details['mobile_number'] = mobile
        self.__details['skills'] = skills
        self.__details['no_of_pages'] = utils.get_number_of_pages(self.__resume)

        try:
            self.__details['degree'] = cust_ent['Degree']
        except KeyError:
            pass

        return

# Define a function to wrap the ResumeParser for parallel processing
def resume_result_wrapper(resume):
    parser = ResumeParser(resume)
    return parser.get_extracted_data()

# Entry point of the script
if __name__ == '__main__':
    # Create a multiprocessing pool based on CPU count
    pool = mp.Pool(mp.cpu_count())

    # Collect the paths of all resume files in the 'resumes' directory
    resumes = []
    data = []
    for root, directories, filenames in os.walk('resumes'):
        for filename in filenames:
            file = os.path.join(root, filename)
            resumes.append(file)

    # Apply the resume_result_wrapper function to each resume in parallel
    results = [
        pool.apply_async(
            resume_result_wrapper,
            args=(x,)
        ) for x in resumes
    ]

    # Retrieve the results from the multiprocessing pool
    results = [p.get() for p in results]

    # Pretty print the extracted data from each resume
    pprint.pprint(results)
