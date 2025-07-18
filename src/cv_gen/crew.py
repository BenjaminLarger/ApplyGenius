from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_openai import ChatOpenAI
from src.cv_gen.tools.tools import ConverterHtmlToPdf, JobPostingScraper
from datetime import datetime
import os
import logging

logger = logging.getLogger(__name__)

@CrewBase
class NewsletterGenCrew:
    """NewsletterGen crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def llm(self):
        llm = ChatOpenAI(model_name="gpt-4o-mini", max_tokens=4096)
        return llm

    @agent
    def job_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["job_analyst"],
            verbose=True,
            allow_delegation=False,
            llm=self.llm(),
        )

    @agent
    def skills_matcher(self) -> Agent:
        return Agent(
            config=self.agents_config["skills_matcher"],
            verbose=True,
            allow_delegation=False,
            llm=self.llm(),
        )

    @agent
    def cv_html_generator(self) -> Agent:
        return Agent(
            config=self.agents_config["cv_html_generator"],
            verbose=True,
            allow_delegation=False,
            llm=self.llm(),
            memory=True,  # Enable memory for CV generation
        )

    @agent
    def pdf_generator(self) -> Agent:
        return Agent(
            config=self.agents_config["pdf_generator"],
            tools=[ConverterHtmlToPdf()],
            verbose=True,
            allow_delegation=False,
            llm=self.llm(),
        )
    
    @agent
    def cover_letter_generator(self) -> Agent:
        return Agent(
            config=self.agents_config["cover_letter_generator"],
            tools=[],
            verbose=True,
            allow_delegation=False,
            llm=self.llm(),
            memory=True,  # Enable memory for cover letter generation
        )

    @task
    def job_analysis(self) -> Task:
        return Task(
            config=self.tasks_config["job_analysis"],
            tools=[JobPostingScraper()],
            agent=self.job_analyst(),
            output_file="src/cv_gen/config/job_offer.txt",
        )

    @task
    def skills_matching(self) -> Task:
        return Task(
            config=self.tasks_config["skills_matching"],
            agent=self.skills_matcher(),
            context=[self.job_analysis()],
        )

    @task
    def cv_html_generation(self) -> Task:
        # Get the CV generation task configuration
        cv_html_config = self.tasks_config["cv_html_generation"]
        
        # Add the job offer content to the task description for better context
        job_offer_text = self.job_offer()
        if "Job Offer Details:" not in cv_html_config["description"]:
            cv_html_config["description"] += f"\n\nJob Offer Details:\n{job_offer_text}"
            logger.info("Added job offer details to CV generation task")

        return Task(
            config=cv_html_config,
            agent=self.cv_html_generator(),
            output_file=f"output/cv_{datetime.now().strftime('%Y-%m-%d')}.html",
            context=[self.job_analysis(), self.skills_matching()],
        )
        
    @task
    def pdf_generation(self) -> Task:
        return Task(
            config=self.tasks_config["pdf_generation"],
            agent=self.pdf_generator(),
            context=[self.cv_html_generation(), self.cover_letter_html_generation()],
            # callback=self.pdf_task_callback,
        )
    
    @task
    def cover_letter_html_generation(self) -> Task:
        # Get the cover letter generation task configuration
        cover_letter_config = self.tasks_config["cover_letter_html_generation"].copy()
        
        # Read the job offer directly from the file for the most up-to-date content
        job_offer_path = "src/cv_gen/config/job_offer.txt"
        job_offer_text = ""
        
        try:
            with open(job_offer_path, "r", encoding="utf-8") as f:
                job_offer_text = f.read()
                
            print(f"Successfully read job offer from {job_offer_path}: {len(job_offer_text)} chars")
            
            # Add the job offer to the task description in a structured way
            if len(job_offer_text) >= 100 and "Job Offer Details:" not in cover_letter_config["description"]:
                # Add a clear section for the job offer details
                cover_letter_config["description"] += f"\n\n## Job Offer Details:\n{job_offer_text}"
                print("Added job offer details to cover letter task")
                
            # Add explicit instructions to reference the job details
            if "Make sure to reference the specific job requirements" not in cover_letter_config["description"]:
                cover_letter_config["description"] += "\n\nMake sure to reference the specific job requirements, skills, and qualifications mentioned in the job offer. Tailor the cover letter to highlight how the candidate's experience matches these requirements."
                
        except Exception as e:
            print(f"Error reading job offer file: {str(e)}")
            cover_letter_config["description"] += "\n\nWARNING: Could not read job offer file. Please make sure the job offer is properly specified."
        
        return Task(
            config=cover_letter_config,
            agent=self.cover_letter_generator(),
            output_file=f"output/cover_letter_{datetime.now().strftime('%Y-%m-%d')}.html",
            context=[self.job_analysis(), self.skills_matching(), self.cv_html_generation()],
        )
    
    def pdf_task_callback(self, output):
        """Process task output to ensure proper content handling"""
        timestamp = datetime.now().strftime('%Y-%m-%d')
        html_file = f"output//cv_{timestamp}.html"
        # Ensure file exists before reading
        if os.path.exists(html_file):
            with open(html_file, 'r') as file:
                html_content = file.read()
            # Process the HTML content as needed
            logger.info(f"\n[Task Callback] Successfully processed HTML content from: {html_file}")
            # Ensure html file does not have HTML_CONTENT_HERE
            if "HTML_CONTENT_HERE" in html_content or len(html_content) < 100:
                logger.info("[Task Callback] HTML content contains 'HTML_CONTENT_HERE', please check the generation process.")
                # Do not proceed with PDF generation

        else:
            logger.info(f"[Task Callback] HTML file not found: {html_file}. Please check the generation process.")
        # Return a message indicating the task was processed
        return f"PDF generation requested with HTML content from {html_file}"
        
    def _format_job_description(self, description):
        """Ensures the job description has proper formatting and sections.
        
        Args:
            description: The raw job description text
            
        Returns:
            str: The formatted job description with proper sections
        """
        # If the description is already well-structured, return it as is
        if len(description.strip()) < 50:
            return description
            
        lines = description.split('\n')
        formatted_desc = []
        
        # Try to identify if this is already a structured job description
        has_job_title = any(len(line.strip()) < 50 and len(line.strip()) > 5 for line in lines[:3])
        has_sections = any(line.strip().endswith(':') for line in lines)
        
        # If it seems already structured, return as is
        if has_job_title and has_sections:
            return description
            
        # Add a title if not present
        if not has_job_title:
            # Check if there's a clear job title indicator
            job_title = None
            for line in lines[:10]:
                if "developer" in line.lower() or "engineer" in line.lower() or "manager" in line.lower():
                    job_title = line.strip()
                    break
                    
            if not job_title:
                job_title = "Job Description"
                
            formatted_desc.append(job_title)
            formatted_desc.append("")
        else:
            # Keep the existing title
            for i, line in enumerate(lines[:3]):
                if len(line.strip()) < 50 and len(line.strip()) > 5:
                    formatted_desc.append(line)
                    if i < 2 and lines[i+1].strip() == "":
                        formatted_desc.append("")
                    break
        
        # Add the rest of the content
        in_section = False
        for line in lines:
            if line in formatted_desc:
                continue
                
            # Try to identify section headers
            if line.strip().endswith(':') or (line.strip() and line.strip().upper() == line.strip() and len(line.strip()) < 30):
                if in_section:
                    formatted_desc.append("")  # Add a blank line before new sections
                formatted_desc.append(line)
                in_section = True
            else:
                formatted_desc.append(line)
                
        return '\n'.join(formatted_desc)

    def job_offer(self):
        """Loads and returns the job offer description from the configuration file.
        
        Returns:
            str: The job offer description text, or an error message if not found.
        """
        job_offer_path = "src/cv_gen/config/job_offer.txt"
        
        if os.path.exists(job_offer_path):
            try:
                with open(job_offer_path, "r", encoding="utf-8") as f:
                    content = f.read()
                logger.info(f"job offer content: {content[:100]}...")  # Log first 100 characters
                
                # Check if the content is just a placeholder or URL
                if ("Job URL:" in content and "placeholder" in content) or len(content.strip()) < 50:
                    logger.info("WARNING: job_offer.txt contains placeholder content or is too short")
                    return "CAUTION: The job description appears to be incomplete. " + content
                logger.info(f"Loaded job offer from {job_offer_path}")
                return content
            except Exception as e:
                logger.info(f"Error reading job offer file: {str(e)}")
                return f"Error reading job offer: {str(e)}"
        else:
            logger.info(f"Job offer file not found at {job_offer_path}")
            return "Job offer description not found. Please check the configuration."

    @crew
    def crew(self) -> Crew:
        """Creates the NewsletterGen crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=2,
        )
