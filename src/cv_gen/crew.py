from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from src.cv_gen.tools.tools import ConverterHtmlToPdf, JobPostingScraper
from langchain_openai import ChatOpenAI
from datetime import datetime
import os


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
            tools=[JobPostingScraper()],
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
        )

    @task
    def job_analysis(self) -> Task:
        return Task(
            config=self.tasks_config["job_analysis"],
            agent=self.job_analyst(),
            output_file=f"logs/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_job_analysis.md",
        )

    @task
    def skills_matching(self) -> Task:
        return Task(
            config=self.tasks_config["skills_matching"],
            agent=self.skills_matcher(),
            output_file=f"logs/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_skills_matching.md",
            context=[self.job_analysis()],
        )

    @task
    def cv_html_generation(self) -> Task:
        return Task(
            config=self.tasks_config["cv_html_generation"],
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
        return Task(
            config=self.tasks_config["cover_letter_html_generation"],
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
            print(f"\n[Task Callback] Successfully processed HTML content from: {html_file}")
            # Ensure html file does not have HTML_CONTENT_HERE
            if "HTML_CONTENT_HERE" in html_content or len(html_content) < 100:
                print("[Task Callback] HTML content contains 'HTML_CONTENT_HERE', please check the generation process.")
                # Do not proceed with PDF generation

        else:
            print(f"[Task Callback] HTML file not found: {html_file}. Please check the generation process.")
        # Return a message indicating the task was processed
        return f"PDF generation requested with HTML content from {html_file}"

    @crew
    def crew(self) -> Crew:
        """Creates the NewsletterGen crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=2,
        )
