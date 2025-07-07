#!/usr/bin/env python
import os
import sys
from dotenv import load_dotenv

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from newsletter_gen.crew import NewsletterGenCrew

# Load environment variables from .env file
load_dotenv()

def load_html_template(): 
    with open('src/newsletter_gen/config/cv_template.html', 'r') as file:
        html_template = file.read()
        
    return html_template

def load_job_offer():
    with open('src/newsletter_gen/config/job_offer.txt', 'r') as file:
        job_offer = file.read()
        
    return job_offer


def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {
        'job_offer_desciption': load_job_offer(),
        'html_template': load_html_template()
    }
    print("Generating newsletter...")
    print(f"exa api key: {os.getenv('EXA_API_KEY')}")
    NewsletterGenCrew().crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    run()