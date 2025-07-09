#!/usr/bin/env python
import os
import sys
from dotenv import load_dotenv

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cv_gen.crew import NewsletterGenCrew

# Load environment variables from .env file
load_dotenv()

def load_html_template(): 
    with open('src/cv_gen/config/cv_template.html', 'r') as file:
        html_template = file.read()
        
    return html_template

def load_job_offer():
    with open('src/cv_gen/config/job_offer.txt', 'r') as file:
        job_offer = file.read()
        
    return job_offer


def run():
    # Get the job URL from user input or use a default fallback
    job_url = input("Enter the job posting URL (or press Enter to use the default job offer): ")
    
    # Load the default job offer text as fallback
    fallback_job_text = load_job_offer()
    
    # If no URL provided, use the default job offer text
    if not job_url:
        job_url = fallback_job_text
        print("Using default job offer text...")
    else:
        print(f"Using job posting URL: {job_url}")
    
    # Set up inputs for the crew
    inputs = {
        'job_offer_url': job_url,
        'job_offer_fallback': fallback_job_text,  # Provide fallback text in case URL scraping fails
        'html_template': load_html_template()
    }
    
    print("Starting CV generation process...")
    NewsletterGenCrew().crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    run()
