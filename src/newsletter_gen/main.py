#!/usr/bin/env python
from newsletter_gen.crew import NewsletterGenCrew
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def load_html_template(): 
    with open('src/newsletter_gen/config/cv_template.html', 'r') as file:
        html_template = file.read()
        
    return html_template


def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {
        'job offer desciption': input('Enter the job offer description: '),
        'html_template': load_html_template()
    }
    print("Generating newsletter...")
    print(f"exa api key: {os.getenv('EXA_API_KEY')}")
    NewsletterGenCrew().crew().kickoff(inputs=inputs)