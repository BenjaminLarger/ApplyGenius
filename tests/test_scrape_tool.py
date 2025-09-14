#!/usr/bin/env python
"""
Test script for scraping a job description from a URL.
This helps verify that the job posting scraper is working correctly.
"""

import sys
import os
import argparse

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.cv_gen.tools.tools import JobPostingScraper

def main():
    parser = argparse.ArgumentParser(description='Test the job posting scraper')
    parser.add_argument('url', help='The URL of the job posting to scrape')
    args = parser.parse_args()
    
    print(f"Testing job posting scraper with URL: {args.url}")
    
    # Create a scraper instance
    scraper = JobPostingScraper()
    
    # Scrape the job posting
    result = scraper._run(args.url)
    
    # Display the result
    print("\n" + "="*50)
    print("SCRAPED JOB DESCRIPTION:")
    print("="*50)
    print(result[:1000] + "..." if len(result) > 1000 else result)
    print("="*50)
    print(f"Total length: {len(result)} characters")
    
    # Check if the job description was saved
    job_offer_path = "src/cv_gen/config/job_offer.txt"
    if os.path.exists(job_offer_path):
        with open(job_offer_path, "r", encoding="utf-8") as f:
            saved_content = f.read()
        
        if saved_content == result:
            print("\n✅ SUCCESS: Job description was correctly saved to the config file.")
        else:
            print("\n⚠️ WARNING: The saved content differs from the scraped result.")
    else:
        print("\n❌ ERROR: Job offer file was not created.")

if __name__ == "__main__":
    main()
