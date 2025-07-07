from crewai_tools import BaseTool
from playwright.async_api import async_playwright
import logging
import asyncio
from datetime import datetime

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
          async with async_playwright() as p:
              browser = await p.chromium.launch()
              page = await browser.new_page()
              await page.set_content(html_content)
              await page.pdf(path=output_path)
              await browser.close()
          logger.info(f"PDF generated successfully: {output_path}")
          return True
      except Exception as e:
          logger.error(f"Error generating PDF: {str(e)}")
          return False

    def _run(self, html_content: str, output_filename: str = None) -> str:
        if not output_filename:
            output_filename = f"output/cv_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.pdf"
        
        success = asyncio.run(self.html_to_pdf(html_content, output_filename))
        
        if success:
            return f"Successfully generated PDF at {output_filename}"
        else:
            return f"Failed to generate PDF at {output_filename}"