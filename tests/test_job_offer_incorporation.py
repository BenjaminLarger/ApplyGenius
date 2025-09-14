#!/usr/bin/env python3
"""
Test script to verify that the job offer is being correctly loaded and incorporated
into the cover letter generation.
"""

import os
import sys
import traceback
from datetime import datetime

# Add the parent directory to sys.path
parent_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, parent_dir)
print(f"Added {parent_dir} to Python path")

try:
    print("Importing NewsletterGenCrew...")
    from src.cv_gen.crew import NewsletterGenCrew
    print("Import successful")
except Exception as e:
    print(f"Error importing NewsletterGenCrew: {str(e)}")
    traceback.print_exc()
    sys.exit(1)

def test_job_offer_loading():
    """Test that the job offer is correctly loaded from the file."""
    print("Testing job offer loading...")
    
    try:
        # Create an instance of the NewsletterGenCrew
        print("Creating NewsletterGenCrew instance...")
        crew = NewsletterGenCrew()
        print("Instance created")
        
        # Call the job_offer method
        print("Calling job_offer method...")
        job_offer_text = crew.job_offer()
        print(f"job_offer method returned {len(job_offer_text)} chars")
        
        # Print the loaded job offer
        print("\nLoaded job offer:")
        print("=" * 50)
        print(job_offer_text[:500] + "..." if len(job_offer_text) > 500 else job_offer_text)
        print("=" * 50)
        
        # Check if the job offer was successfully loaded
        if len(job_offer_text) > 100 and "error" not in job_offer_text.lower() and "not found" not in job_offer_text.lower():
            print("\n✅ SUCCESS: Job offer was correctly loaded from the file.")
        else:
            print("\n❌ ERROR: Failed to load job offer. Got: " + job_offer_text[:100])
            
        return job_offer_text
    except Exception as e:
        print(f"Error in test_job_offer_loading: {str(e)}")
        traceback.print_exc()
        return "Error: " + str(e)

def test_cover_letter_task():
    """Test that the cover letter task includes the job offer."""
    print("\nTesting cover letter task configuration...")
    
    try:
        # Create an instance of the NewsletterGenCrew
        print("Creating NewsletterGenCrew instance...")
        crew = NewsletterGenCrew()
        print("Instance created")
        
        # Get the cover letter task
        print("Getting cover_letter_html_generation task...")
        cover_letter_task = crew.cover_letter_html_generation()
        print(f"Task retrieved: {cover_letter_task}")
        
        # Check if the task is None
        if cover_letter_task is None:
            print("❌ ERROR: cover_letter_task is None. Check if the method exists and is working correctly.")
            
            # Try to debug by checking if the task is defined in tasks_config
            if hasattr(crew, 'tasks_config'):
                print(f"Tasks config path: {crew.tasks_config}")
                try:
                    import yaml
                    with open(os.path.join('src/cv_gen', crew.tasks_config), 'r') as f:
                        tasks = yaml.safe_load(f)
                    if 'cover_letter_html_generation' in tasks:
                        print("✅ Task 'cover_letter_html_generation' is defined in tasks.yaml")
                    else:
                        print("❌ Task 'cover_letter_html_generation' is NOT defined in tasks.yaml")
                        print(f"Available tasks: {list(tasks.keys())}")
                except Exception as e:
                    print(f"Error loading tasks config: {e}")
            
            return "Error: cover_letter_task is None"
        
        # Check if the job offer is included in the task description
        task_description = cover_letter_task.config.get("description", "")
        print(f"Task description has {len(task_description)} chars")
        
        # Rest of the function remains the same...
        
        # Print the task description
        print("\nCover letter task description:")
        print("=" * 50)
        print(task_description[:500] + "..." if len(task_description) > 500 else task_description)
        print("=" * 50)
        
        # Check if the job offer details are included in the task description
        if "Job Offer Details:" in task_description:
            print("\n✅ SUCCESS: Job offer details are included in the cover letter task.")
            
            # Extract the job offer from the task description
            job_offer_in_task = task_description.split("Job Offer Details:")[1].strip()
            print(f"\nJob offer in task ({len(job_offer_in_task)} chars):")
            print("=" * 50)
            print(job_offer_in_task[:500] + "..." if len(job_offer_in_task) > 500 else job_offer_in_task)
            print("=" * 50)
            
            # Check if the job offer in the task matches the job offer in the file
            job_offer_from_file = crew.job_offer()
            # Calculate a simple similarity metric
            words_in_task = set(job_offer_in_task.split())
            words_in_file = set(job_offer_from_file.split())
            if len(words_in_file) > 0:  # Avoid division by zero
                similarity = len(words_in_task & words_in_file) / len(words_in_file)
                print(f"\nSimilarity between job offer in task and file: {similarity:.2%}")
                
                if similarity > 0.5:
                    print("✅ SUCCESS: Job offer in task is similar to the one in the file.")
                else:
                    print("⚠️ WARNING: Job offer in task differs significantly from the one in the file.")
            else:
                print("⚠️ WARNING: No words found in the job offer file.")
        else:
            print("\n❌ ERROR: Job offer details are not included in the cover letter task.")
        
        return task_description
    except Exception as e:
        print(f"Error in test_cover_letter_task: {str(e)}")
        traceback.print_exc()
        return "Error: " + str(e)

if __name__ == "__main__":
    print("=" * 60)
    print("JOB OFFER INCORPORATION TEST SCRIPT")
    print("=" * 60)
    
    # Check if the job offer file exists
    job_offer_path = "src/cv_gen/config/job_offer.txt"
    if os.path.exists(job_offer_path):
        print(f"Job offer file exists at {job_offer_path}")
        with open(job_offer_path, "r", encoding="utf-8") as f:
            content = f.read()
        print(f"File contains {len(content)} chars")
        print(f"First 100 chars: {content[:100]}")
    else:
        print(f"Job offer file does not exist at {job_offer_path}")
    
    # Test job offer loading
    job_offer = test_job_offer_loading()
    
    # Test cover letter task
    task_description = test_cover_letter_task()
    
    print("\nTests completed!")
