#!/usr/bin/env python
import os
import sys
from dotenv import load_dotenv
from crewai_tools import ScrapeWebsiteTool

# Load environment variables
load_dotenv()

def test_scrape_tool():
    """Test the ScrapeWebsiteTool functionality"""
    print("Testing ScrapeWebsiteTool...")
    
    # Ask for a test URL
    test_url = input("Enter a URL to test scraping (or press Enter for default LinkedIn job): ")
    if not test_url:
        test_url = "https://www.linkedin.com/jobs/view/python-developer-at-acme-corp-3694151349/"
        print(f"Using default test URL: {test_url}")
    
    # Create and use the tool
    scrape_tool = ScrapeWebsiteTool(website_url=test_url)
    
    try:
        result = scrape_tool.run()
        print("\n--- Scraping Result ---")
        print(f"Successfully scraped content from: {test_url}")
        print(f"Content length: {len(result)} characters")
        print("\nFirst 500 characters of content:")
        print(result[:500] + "...\n")
        return True
    except Exception as e:
        print(f"Error scraping {test_url}: {str(e)}")
        return False

if __name__ == "__main__":
    test_scrape_tool()
