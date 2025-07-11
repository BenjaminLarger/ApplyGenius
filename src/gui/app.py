#!/usr/bin/env python
import streamlit as st
import os
import sys
import json
import time
from datetime import datetime
import base64
from pathlib import Path

# Add the parent directory to sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(parent_dir)
from src.cv_gen.crew import NewsletterGenCrew
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Check if OpenAI API key is available
def check_api_keys():
    """Check if necessary API keys are set in environment variables."""
    if not os.getenv("OPENAI_API_KEY"):
        st.error("⚠️ OpenAI API key is not set. Please add it to your .env file.")
        st.code("OPENAI_API_KEY=your_key_here", language="bash")
        return False
    return True

# Set page configuration
st.set_page_config(
    page_title="CV & Cover Letter Generator",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stButton button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 10px 24px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    .output-container {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 5px;
        border: 1px solid #ddd;
        margin-top: 20px;
    }
    .header-container {
        background-color: #0e1117;
        padding: 20px;
        border-radius: 5px;
        margin-bottom: 20px;
        color: white;
    }
    .sample-box {
        background-color: #f0f8ff;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #cce5ff;
        margin-top: 10px;
        cursor: pointer;
    }
    .sample-box:hover {
        background-color: #e6f3ff;
        border: 1px solid #b3d7ff;
    }
</style>
""", unsafe_allow_html=True)

def create_download_link(file_path, link_text):
    """Create a download link for a file."""
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    filename = os.path.basename(file_path)
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">{link_text}</a>'

def upload_cv_section():
    """Section for uploading the user's CV."""
    st.header("1. Upload Your CV (Optional)")
    
    uploaded_file = st.file_uploader("Upload your existing CV (HTML", type=["html"])
    
    if uploaded_file is not None:
        # Create the uploads directory if it doesn't exist
        os.makedirs("uploads", exist_ok=True)
        
        # Save the uploaded file
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file_path = os.path.join("uploads", f"{timestamp}_{uploaded_file.name}")
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"CV uploaded successfully: {uploaded_file.name}")
        return file_path
    
    return "src/cv_gen/config/cv_template.html"  # Default CV template path

def upload_cover_letter_section():
    """Section for uploading the user's cover letter."""
    st.header("2. Upload Your Cover Letter (Optional)")
    
    uploaded_file = st.file_uploader("Upload your existing cover letter (HTML)", type=["html"])
    
    if uploaded_file is not None:
        # Create the uploads directory if it doesn't exist
        os.makedirs("uploads", exist_ok=True)
        
        # Save the uploaded file
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file_path = os.path.join("uploads", f"{timestamp}_{uploaded_file.name}")
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"Cover letter uploaded successfully: {uploaded_file.name}")
        return file_path
    
    return "src/cv_gen/config/cover_letter_template.html"  # Default cover letter template path
# Sample job descriptions for quick testing
SAMPLE_JOB_DESCRIPTIONS = {
    "Software Engineer": """
Software Engineer
Microsoft - Redmond, WA

About the job
Microsoft's mission is to empower every person and every organization on the planet to achieve more. As employees we come together with a growth mindset, innovate to empower others, and collaborate to realize our shared goals.

The Software Engineering team is looking for a talented Software Engineer to join our team. In this role, you will be responsible for developing and maintaining high-quality software solutions.

Responsibilities:
• Design, develop, test, deploy, maintain, and improve software
• Manage individual project priorities, deadlines, and deliverables
• Write clean, maintainable, and efficient code
• Participate in code reviews and contribute to team engineering best practices

Qualifications:
• Bachelor's degree in Computer Science, Engineering, or related field
• 3+ years of professional software development experience
• Strong proficiency in Python, Java, or C#
• Experience with cloud platforms (Azure, AWS, or GCP)
• Knowledge of data structures, algorithms, and software design principles
""",
    "Data Scientist": """
Data Scientist
Google - Mountain View, CA

About the job
At Google, we're always looking to solve complex problems, and data scientists play a key role in this mission. We're looking for a talented Data Scientist to join our team.

Responsibilities:
• Develop innovative machine learning models to solve complex business problems
• Analyze large datasets to extract insights and drive decision-making
• Collaborate with cross-functional teams to implement data-driven solutions
• Communicate findings and recommendations to stakeholders

Qualifications:
• Master's or PhD in Statistics, Computer Science, or related field
• Experience with statistical analysis, machine learning, and data visualization
• Proficiency in Python, R, or similar programming languages
• Experience with SQL and data manipulation techniques
• Strong problem-solving and analytical skills
""",
    "Marketing Manager": """
Marketing Manager
Apple - Cupertino, CA

About the job
Apple is seeking a creative and strategic Marketing Manager to lead our product marketing initiatives. In this role, you will be responsible for developing and executing marketing strategies to drive product awareness and growth.

Responsibilities:
• Develop and implement marketing strategies for Apple products
• Lead market research efforts to understand customer needs and preferences
• Collaborate with product teams to define positioning and messaging
• Manage digital marketing campaigns across various channels
• Analyze campaign performance and optimize marketing efforts

Qualifications:
• Bachelor's degree in Marketing, Business, or related field
• 5+ years of experience in product marketing
• Strong understanding of digital marketing channels and tactics
• Excellent communication and presentation skills
• Experience with marketing analytics and tools
"""
}

@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_cv_template(cv_path):
    try:
        with open(cv_path, 'r') as file:
            cv_template = file.read()
        return cv_template
    except Exception as e:
        st.error(f"Error loading CV template: {str(e)}")
        return None

@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_cover_letter_template(cover_letter_path):
    """Load the cover letter template from the specified path."""
    try:
        with open(cover_letter_path, 'r') as file:
            cover_letter_template = file.read()
        return cover_letter_template
    except Exception as e:
        st.error(f"Error loading cover letter template: {str(e)}")
        return None

def job_description_section():
    """Section for entering or uploading job description."""
    st.header("3. Job Description")
    
    job_method = st.radio("How would you like to input the job description?", 
                          ["Paste text", "Provide URL", "Use sample"])
    
    job_description = None
    job_url = None
    
    if job_method == "Paste text":
        job_description = st.text_area("Paste the job description here:", height=300,
                                     placeholder="Copy and paste the complete job description text here...")
        if job_description:
            st.info(f"Text input received ({len(job_description)} characters)")
            
    elif job_method == "Provide URL":
        job_url = st.text_input("Enter the URL of the job posting:", 
                             placeholder="https://example.com/job-posting")
        if job_url:
            if not job_url.startswith(('http://', 'https://')):
                job_url = f"https://{job_url}"
                st.info(f"Added 'https://' prefix to URL: {job_url}")
            else:
                st.info(f"URL received: {job_url}")
    
    elif job_method == "Use sample":
        st.subheader("Select a sample job description")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Software Engineer"):
                job_description = SAMPLE_JOB_DESCRIPTIONS["Software Engineer"]
                
        with col2:
            if st.button("Data Scientist"):
                job_description = SAMPLE_JOB_DESCRIPTIONS["Data Scientist"]
                
        with col3:
            if st.button("Marketing Manager"):
                job_description = SAMPLE_JOB_DESCRIPTIONS["Marketing Manager"]
        
        if job_description:
            st.success("Sample job description selected")
            st.markdown(
                f'<div class="sample-box">{job_description[:300]}...</div>',
                unsafe_allow_html=True
            )
        
    return job_description, job_url

def run_cv_generation(job_description, job_url, cv_path, cover_letter_path, model_name="gpt-4o-mini", debug_mode=False):
    """Run the CV generation process."""
    timestamp = datetime.now().strftime('%Y-%m-%d')
    
    # Create a progress container
    progress_container = st.empty()
    progress_container.info("Initializing CV and cover letter generation process...")
    
    progress_bar = st.progress(0)
    
    try:
        # Configure the input based on what was provided
        if job_url:
            progress_container.info("Processing job posting from URL...")
            progress_bar.progress(10)
            
            inputs = {
                'job_offer_url': job_url,
                'job_offer_fallback': job_description if job_description else "",
                'cv_template': load_cv_template(cv_path),
                'cover_letter_template': load_cover_letter_template(cover_letter_path),
                'model_name': model_name,
            }
            progress_container.info(f"Job URL prepared: {job_url}")
            progress_bar.progress(20)
            
        else:
            # Save job description to a temporary file
            progress_container.info("Processing job description text...")
            progress_bar.progress(10)
            
            job_file_path = f"uploads/job_description_{timestamp}.txt"
            os.makedirs(os.path.dirname(job_file_path), exist_ok=True)
            
            with open(job_file_path, "w") as f:
                f.write(job_description)
            
            inputs = {
                'job_offer_url': "",  # Empty URL will make it use the fallback
                'job_offer_fallback': job_description,
                'cv_template': load_cv_template(cv_path),
                'cover_letter_template': load_cover_letter_template(cover_letter_path),
                'model_name': model_name,
            }
            progress_container.info("Job description prepared")
            progress_bar.progress(20)
        
        # Run the CV generation process
        progress_container.info("Starting job analysis...")
        progress_bar.progress(30)
        
        # Debug mode - show more detailed logs
        if debug_mode:
            st.text_area("Debug: Input data", json.dumps(inputs, indent=2), height=150)
        
        start_time = time.time()
        # print(f"inputs = {inputs}")
        st.info(f"inputs = {inputs}")
        #result = NewsletterGenCrew().crew().kickoff(inputs=inputs)
        end_time = time.time()
        
        progress_container.info("Documents generated. Preparing final files...")
        progress_bar.progress(90)
        
        # Define expected output files
        cv_html_path = f"output/cv_{timestamp}.html"
        cv_pdf_path = f"output/cv_{timestamp}.pdf"
        cover_letter_html_path = f"output/cover_letter_{timestamp}.html"
        cover_letter_pdf_path = f"output/cover_letter_{timestamp}.pdf"
        
        # Check if files exist
        files_exist = all([
            os.path.exists(cv_html_path),
            os.path.exists(cover_letter_html_path),
            os.path.exists(cover_letter_pdf_path)
        ])
        
        if not files_exist:
            missing_files = []
            if not os.path.exists(cv_html_path): missing_files.append("CV HTML")
            if not os.path.exists(cover_letter_html_path): missing_files.append("Cover Letter HTML")
            if not os.path.exists(cover_letter_pdf_path): missing_files.append("Cover Letter PDF")
            
            progress_container.warning(f"Some output files are missing: {', '.join(missing_files)}")
        else:
            progress_container.success(f"All files generated successfully in {end_time - start_time:.1f} seconds!")
        
        progress_bar.progress(100)
        
        # Create result container
        st.success("CV and cover letter generation complete!")
        
        # Display processing time
        st.info(f"⏱️ Processing time: {end_time - start_time:.1f} seconds")
        
        # Display download links
        st.subheader("Download Your Documents")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### CV")
            if os.path.exists(cv_html_path):
                st.markdown(create_download_link(cv_html_path, "Download CV (HTML)"), unsafe_allow_html=True)
            else:
                st.error("CV HTML file not found")
            
            if os.path.exists(cv_pdf_path):
                st.markdown(create_download_link(cv_pdf_path, "Download CV (PDF)"), unsafe_allow_html=True)
            else:
                st.error("CV PDF file not found")
        
        with col2:
            st.markdown("### Cover Letter")
            if os.path.exists(cover_letter_html_path):
                st.markdown(create_download_link(cover_letter_html_path, "Download Cover Letter (HTML)"), unsafe_allow_html=True)
            else:
                st.error("Cover Letter HTML file not found")
            
            if os.path.exists(cover_letter_pdf_path):
                st.markdown(create_download_link(cover_letter_pdf_path, "Download Cover Letter (PDF)"), unsafe_allow_html=True)
            else:
                st.error("Cover Letter PDF file not found")
        
        # Preview section
        st.subheader("Document Preview")
        
        preview_tabs = st.tabs(["CV", "Cover Letter"])
        
        with preview_tabs[0]:
            if os.path.exists(cv_html_path):
                with open(cv_html_path, "r") as f:
                    cv_html = f.read()
                st.components.v1.html(cv_html, height=600, scrolling=True)
            else:
                st.warning("CV HTML preview not available")
        
        with preview_tabs[1]:
            if os.path.exists(cover_letter_html_path):
                with open(cover_letter_html_path, "r") as f:
                    cover_letter_html = f.read()
                st.components.v1.html(cover_letter_html, height=600, scrolling=True)
            else:
                st.warning("Cover letter HTML preview not available")
        
        return True
            
    except Exception as e:
        progress_container.error(f"Error in generation process")
        progress_bar.progress(100)
        st.error(f"Error generating documents: {str(e)}")
        st.error("Please check the logs for more details and try again.")
        
        # More detailed error information in debug mode
        if debug_mode:
            import traceback
            st.text_area("Debug: Error details", traceback.format_exc(), height=300)
            
        return False

def main():
    """Main function for the Streamlit app."""
    st.markdown("""
    <div class="header-container">
        <h1>AI-Powered CV & Cover Letter Generator</h1>
        <p>Automatically generate customized CVs and cover letters tailored to specific job postings</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check API keys first
    api_keys_valid = check_api_keys()
    
    # Create a sidebar for instructions and options
    with st.sidebar:
        st.title("How It Works")
        st.markdown("""
        1. **Upload your existing CV** (optional)
        2. **Enter job description** by pasting text, uploading a file, or providing a URL
        3. **Click 'Generate CV & Cover Letter'**
        4. **Download** your customized documents
        
        The AI will analyze the job requirements, match them with your skills, and generate 
        documents optimized for this specific position.
        """)
        
        st.markdown("---")
        
        # Settings section
        st.subheader("Settings")
        model_option = st.selectbox(
            "AI Model",
            ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"],
            index=0,
            help="Select the AI model to use for generation. More powerful models may produce better results but take longer."
        )
        
        debug_mode = st.checkbox("Debug Mode", value=False, 
                             help="Enable to see detailed process logs and information")
        
        st.markdown("---")
        
        st.markdown("""
        ### About
        This tool uses CrewAI to power a team of specialized AI agents that work together to:
        
        - Analyze job postings
        - Match skills to requirements
        - Generate tailored documents
        - Convert to professional formats
        
        Each document is uniquely crafted to maximize your chances of landing an interview.
        """)
        
        # Version and credits
        st.markdown("---")
        st.caption("Version 1.0.0 | Built with CrewAI")
        st.caption("© 2025 CV Generator")
    
    # Main content
    if api_keys_valid:
        cv_path = upload_cv_section()
        cover_letter_path = upload_cover_letter_section()
        job_description, job_url = job_description_section()
        
        # Generate button with a more attractive style
        st.markdown("""
        <style>
        div.stButton > button:first-child {
            background-color: #0066cc;
            color: white;
            font-size: 20px;
            font-weight: bold;
            height: 3em;
            border-radius: 10px;
            border: none;
            margin-top: 20px;
            margin-bottom: 20px;
        }
        div.stButton > button:hover {
            background-color: #0055a7;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Add a helpful message before the button
        st.info("Click the button below to start the generation process. This may take several minutes depending on the complexity of the job description.")
        
        # Generate button
        if st.button("⚡ Generate CV & Cover Letter ⚡"):
            if not job_description and not job_url:
                st.warning("⚠️ Please provide a job description or URL")
            else:
                run_cv_generation(job_description, job_url, cv_path, cover_letter_path, model_option, debug_mode)

def run():
    main()

if __name__ == "__main__":
    run()
