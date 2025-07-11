#!/usr/bin/env python
"""
Test script for the CV Generator Streamlit UI
This script provides functions to test different aspects of the UI
"""

import os
import sys
import time
import requests
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Add the parent directory to sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

def setup_driver():
    """Setup and return a Chrome WebDriver instance."""
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def test_url_input(driver, streamlit_url, job_url):
    """Test the URL input method for job descriptions."""
    print(f"Testing URL input with job URL: {job_url}")
    
    # Navigate to the Streamlit app
    driver.get(streamlit_url)
    
    # Wait for the page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))
    )
    
    # Select URL input method
    radio_buttons = driver.find_elements(By.CSS_SELECTOR, 'div[role="radiogroup"] label')
    for button in radio_buttons:
        if "Provide URL" in button.text:
            button.click()
            break
    
    # Enter the job URL
    url_input = driver.find_element(By.CSS_SELECTOR, 'input[type="text"]')
    url_input.clear()
    url_input.send_keys(job_url)
    
    # Click the generate button
    generate_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Generate CV & Cover Letter')]"))
    )
    generate_button.click()
    
    # Wait for the generation process to complete
    try:
        WebDriverWait(driver, 180).until(  # 3 minutes timeout
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'CV and cover letter generation complete!')]"))
        )
        print("✅ Generation process completed successfully")
        return True
    except Exception as e:
        print(f"❌ Generation process failed: {str(e)}")
        return False

def test_text_input(driver, streamlit_url, job_description):
    """Test the text input method for job descriptions."""
    print(f"Testing text input with job description length: {len(job_description)} characters")
    
    # Navigate to the Streamlit app
    driver.get(streamlit_url)
    
    # Wait for the page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))
    )
    
    # Select text input method (should be selected by default)
    radio_buttons = driver.find_elements(By.CSS_SELECTOR, 'div[role="radiogroup"] label')
    for button in radio_buttons:
        if "Paste text" in button.text:
            button.click()
            break
    
    # Enter the job description
    text_area = driver.find_element(By.CSS_SELECTOR, 'textarea')
    text_area.clear()
    text_area.send_keys(job_description)
    
    # Click the generate button
    generate_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Generate CV & Cover Letter')]"))
    )
    generate_button.click()
    
    # Wait for the generation process to complete
    try:
        WebDriverWait(driver, 180).until(  # 3 minutes timeout
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'CV and cover letter generation complete!')]"))
        )
        print("✅ Generation process completed successfully")
        return True
    except Exception as e:
        print(f"❌ Generation process failed: {str(e)}")
        return False

def verify_output_files(timestamp=None):
    """Verify that the output files exist."""
    if timestamp is None:
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y-%m-%d')
    
    output_dir = Path("output")
    
    # Define expected output files
    expected_files = [
        output_dir / f"cv_{timestamp}.html",
        output_dir / f"cv_{timestamp}.pdf",
        output_dir / f"cover_letter_{timestamp}.html",
        output_dir / f"cover_letter_{timestamp}.pdf"
    ]
    
    # Check if files exist
    missing_files = [str(f) for f in expected_files if not f.exists()]
    
    if missing_files:
        print(f"❌ Missing output files: {', '.join(missing_files)}")
        return False
    else:
        print("✅ All output files generated successfully")
        file_sizes = {str(f): f.stat().st_size for f in expected_files}
        print("File sizes:")
        for file, size in file_sizes.items():
            print(f"  - {file}: {size} bytes")
        return True

def run_tests():
    """Run all tests."""
    print("Running CV Generator UI tests...")
    
    # Streamlit URL (local)
    streamlit_url = "http://localhost:8501"
    
    # Sample job URL and description for testing
    job_url = "https://www.linkedin.com/jobs/view/software-engineer-at-microsoft-3743761782"
    
    job_description = """
    Software Engineer
    Microsoft - Redmond, WA

    About the job
    Microsoft's mission is to empower every person and every organization on the planet to achieve more. As employees we come together with a growth mindset, innovate to empower others, and collaborate to realize our shared goals. Each day we build on our values of respect, integrity, and accountability to create a culture of inclusion where everyone can thrive at work and beyond.

    The Data & AI team is looking for a talented Software Engineer to join our team. In this role, you will be responsible for developing and maintaining high-quality software solutions for our data and AI products. You will work closely with cross-functional teams to design, implement, and deploy software that meets business requirements and provides value to our customers.

    Responsibilities:
    • Design, develop, test, deploy, maintain, and improve software
    • Manage individual project priorities, deadlines, and deliverables
    • Write clean, maintainable, and efficient code
    • Participate in code reviews and contribute to team engineering best practices
    • Collaborate with other team members and stakeholders

    Qualifications:
    • Bachelor's degree in Computer Science, Engineering, or related field, or equivalent practical experience
    • 3+ years of professional software development experience
    • Strong proficiency in Python, Java, or C#
    • Experience with cloud platforms (Azure, AWS, or GCP)
    • Knowledge of data structures, algorithms, and software design principles
    • Experience with databases (SQL and NoSQL)
    • Familiarity with AI/ML technologies and frameworks is a plus
    • Strong problem-solving skills and attention to detail
    • Excellent communication and teamwork skills

    Benefits:
    • Competitive salary and benefits package
    • Flexible work arrangements
    • Professional development opportunities
    • Health and wellness programs
    • Generous PTO and holidays
    """
    
    driver = None
    try:
        # Setup WebDriver
        driver = setup_driver()
        
        # Test URL input
        print("\n=== Testing URL Input ===")
        test_url_input(driver, streamlit_url, job_url)
        
        time.sleep(5)  # Wait between tests
        
        # Test text input
        print("\n=== Testing Text Input ===")
        test_text_input(driver, streamlit_url, job_description)
        
        # Verify output files
        print("\n=== Verifying Output Files ===")
        verify_output_files()
        
    except Exception as e:
        print(f"Test error: {str(e)}")
    finally:
        if driver:
            driver.quit()
    
    print("\nTests completed")

if __name__ == "__main__":
    run_tests()
