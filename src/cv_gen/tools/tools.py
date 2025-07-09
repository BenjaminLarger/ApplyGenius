from crewai_tools import BaseTool, ScrapeWebsiteTool
from playwright.async_api import async_playwright
import logging
import asyncio
from datetime import datetime
import os
logger = logging.getLogger(__name__)

class JobAnalysisTool(BaseTool):
    name: str = "Job Analysis Tool"
    description: str = "Extract requirements from job postings"
    
    def _run(self, job_text: str) -> dict:
        # This is a stub - the actual analysis will be done by the LLM
        # We're just providing a placeholder for the CrewAI framework
        return {"status": "Analysis requested", "job_text_length": len(job_text)}

class SkillsMatcherTool(BaseTool):
    name: str = "Skills Matcher Tool"
    description: str = "Match job requirements with candidate skills"
    
    def _run(self, job_requirements: dict) -> dict:
        # This is a stub - the actual matching will be done by the LLM
        # We're just providing a placeholder for the CrewAI framework
        return {"status": "Matching requested", "requirements_count": len(job_requirements)}

class HTMLGeneratorTool(BaseTool):
    name: str = "HTML Generator Tool"
    description: str = "Generate CV using template"
    
    def _run(self, matched_data: dict) -> str:
        # This is a stub - the actual HTML generation will be done by the LLM
        # We're just providing a placeholder for the CrewAI framework
        return f"HTML generation requested with {len(matched_data)} data points"
    
class CVConverterHtmlToPdf(BaseTool):
    name: str = "CV Converter HTML to PDF"
    description: str = "Convert HTML CV to PDF format"
    
    async def html_to_pdf(self, html_content, output_path):
        try:
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                
                # Set content with proper encoding
                await page.set_content(html_content, wait_until="networkidle")
                
                # Add a small delay to ensure rendering is complete
                await page.wait_for_timeout(1000)
                
                # Set PDF options for better formatting
                
                await page.pdf(path=output_path, format="A4", margin={"top": "1cm", "right": "1cm", "bottom": "1cm", "left": "1cm"})
                await browser.close()
                
            logger.info(f"PDF generated successfully: {output_path}")
            return True
        except Exception as e:
            logger.error(f"Error generating PDF: {str(e)}")
            return False

    def _run(self) -> str:
        """
        Convert HTML content to PDF
        
        Args:
            html_content: The full HTML content to convert
            
        Returns:
            A message indicating success or failure
        """
        # Try to read file from cv_{timestamp}.html
        timestamp = datetime.now().strftime('%Y-%m-%d')
        try:
            with open(f"output/cv_{timestamp}.html", 'r', encoding='utf-8') as file:
                html_content = file.read()
        except FileNotFoundError:
            logger.error(f"HTML file not found for timestamp {timestamp}. Please ensure the HTML generation task ran successfully.")
            return f"HTML file not found for timestamp {timestamp}. Please ensure the HTML generation task ran successfully."

        # Clean up the HTML content if it's received as a dictionary
        if isinstance(html_content, dict) and 'html_content' in html_content:
            html_content = html_content['html_content']
        
        # Clean html file
        if html_content.startswith("```html"):
            html_content = html_content.replace("```html", "").replace("```", "").strip() 
            
        # Handle potential string representation of dictionary
        if html_content.startswith("{'html_content':"):
            try:
                import ast
                parsed = ast.literal_eval(html_content)
                if isinstance(parsed, dict) and 'html_content' in parsed:
                    html_content = parsed['html_content']
            except:
                pass
                
        output_filename = f"output//cv_{timestamp}.pdf"
        
        # Write the HTML to a file for debugging
        html_file = f"output/cv_{timestamp}.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        # Convert to PDF
        success = asyncio.run(self.html_to_pdf(html_content, output_filename))
        
        if success:
            return f"Successfully generated PDF at {output_filename} and saved HTML at {html_file}"
        else:
            return f"Failed to generate PDF. HTML content saved at {html_file} for debugging."
        
from crewai_tools import BaseTool, ScrapeWebsiteTool

class JobPostingScraper(BaseTool):
    name: str = "Job Posting Scraper"
    description: str = "Scrapes job posting content from a given URL"
    
    def _run(self, url: str) -> str:
        """Scrapes content from the provided job posting URL."""
        try:
            # Add https:// if missing
            if not url.startswith(('http://', 'https://')):
                url = f"https://{url}"
                
            # Use the ScrapeWebsiteTool internally
            scraper = ScrapeWebsiteTool(website_url=url)
            result = scraper.run()
            return result
        except Exception as e:
            return f"Error scraping the website: {str(e)}"