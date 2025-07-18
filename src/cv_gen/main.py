#!/usr/bin/env python
import os
import sys
from dotenv import load_dotenv

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cv_gen.crew import NewsletterGenCrew

# Load environment variables from .env file
load_dotenv()

def load_cv_template(): 
    with open('src/cv_gen/config/cv_template.html', 'r') as file:
        cv_template = file.read()
        
    return cv_template

def load_cover_letter_template():
    with open('src/cv_gen/config/cover_letter_template.html', 'r') as file:
        cover_letter_template = file.read()

    return cover_letter_template

def load_job_offer():
    with open('src/cv_gen/config/job_offer.txt', 'r') as file:
        job_offer = file.read()
        
    return job_offer


def run():
    # Get the job URL from user input or use a default fallback
    print("CV Generator - Command Line Interface")
    print("-------------------------------------")
    print("Note: For a more user-friendly interface, you can use the Streamlit UI:")
    print("      streamlit run src/gui/app.py")
    print("-------------------------------------\n")
    
    job_url = input("Enter the job posting URL (or press Enter to use the default job offer): ")
    
    # Load the default job offer text as fallback
    try:
        fallback_job_text = load_job_offer()
    except:
        print("No default job offer found, creating an empty one...")
        # Create an empty job offer file
        os.makedirs(os.path.dirname('src/cv_gen/config/job_offer.txt'), exist_ok=True)
        with open('src/cv_gen/config/job_offer.txt', 'w') as file:
            file.write("")
        fallback_job_text = ""
    
    # If no URL provided, use the default job offer text
    if not job_url:
        job_url = ""
        print("Using default job offer text...")
    else:
        print(f"Using job posting URL: {job_url}")
        
        # Add https:// prefix if needed
        if not job_url.startswith(('http://', 'https://')):
            job_url = f"https://{job_url}"
            print(f"Added 'https://' prefix: {job_url}")
    
    # Set up inputs for the crew
    inputs = {
        'job_offer_url': job_url,
        'job_offer_fallback': fallback_job_text,  # Provide fallback text in case URL scraping fails
        'cv_template': load_cv_template(),
        'cover_letter_template': load_cover_letter_template(),
    }
    
    print("Starting CV and cover letter generation process...")
    NewsletterGenCrew().crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    run()
