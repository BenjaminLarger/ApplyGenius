import asyncio
from playwright.async_api import async_playwright
import logging
import os
# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def html_to_pdf(html_content, output_path):
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


# PDF path to save
html_path = 'src/cv_gen/config/cv_template.html'
print(f"Loading HTML template from: {html_path}")
with open(html_path, 'r') as file:
    html_content = file.read()

output_path = 'output/cv_generation.pdf'

print(f"Generating PDF at: {output_path}")

# Generate PDF
asyncio.run(html_to_pdf(html_content, output_path))
