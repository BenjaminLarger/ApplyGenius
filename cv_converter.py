import asyncio
from playwright.async_api import async_playwright
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def html_to_pdf(html_content, output_path):
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

# HTML content
html_content = '''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
  <title>Benjamin Larger Resume</title>
  <meta name="author" content="Emily Nousbaum"/>
  <style type="text/css">
    * {
      margin: 0; 
      padding: 0; 
      text-indent: 0;
    }
    
    h1 { 
      color: #000080; 
      font-family: Calibri, sans-serif; 
      font-style: normal; 
      font-weight: bold; 
      text-decoration: none; 
      font-size: 16pt;
    }
    
    a { 
      color: #00F; 
      font-family: Calibri, sans-serif; 
      font-style: normal; 
      font-weight: normal; 
      text-decoration: underline; 
      font-size: 11pt;
    }
    
    .p, p { 
      color: black; 
      font-family: Calibri, sans-serif; 
      font-style: normal; 
      font-weight: normal; 
      text-decoration: none; 
      font-size: 11pt; 
      margin: 0pt;
    }
    
    .date { 
      color: black; 
      font-family: Calibri, sans-serif; 
      font-style: normal; 
      font-weight: normal; 
      text-decoration: none; 
      font-size: 11pt; 
      margin: 0pt; 
      float: right;
    }

    h2 {
      color: black;
      font-family: Calibri, sans-serif;
      font-style: normal;
      font-weight: bold;
      font-size: 12pt;
      border-bottom: 1px solid #979797;
    }

    h3 { 
      color: black; 
      font-family: Calibri, sans-serif; 
      font-style: normal; 
      font-weight: bold; 
      text-decoration: none; 
      font-size: 11pt;
    }
    
    .s2 { 
      color: #212121; 
      font-family: Arial, sans-serif; 
      font-style: normal; 
      font-weight: normal; 
      text-decoration: none; 
      font-size: 9pt;
    }
    
    li {
      display: block;
    }
    
    #l1 {
      padding-left: 0pt;
    }
    
    #l1 > li > *:first-child:before {
      content: "• ";
      display: inline-block;
    }
  </style>
</head>
<body style="border: 2px solid black; padding: 30px;">

  <!-- Header Container -->
  <div style="display: flex; justify-content: space-between; align-items: flex-start; padding: 25px;">

    <!-- Left Side: 42 Logo -->
    <div>
      <a href="https://42.fr/">
        <img width="90" height="90" src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/42_Logo.svg/768px-42_Logo.svg.png" alt="42 Logo" />
      </a>
    </div>

    <!-- Right Side: Info + Profile Pic -->
    <div style="display: flex; gap: 20px; align-items: flex-start;">
      
      <!-- Info (on the left of picture) -->
      <div style="text-align: right;">
        <h1 style="color: #000080; font-family: Calibri, sans-serif;">Benjamin Larger</h1>
        <p><a href="mailto:benjaminlarger.bl@gmail.com">benjaminlarger.bl@gmail.com</a></p>
        <p>+34 667 006 863</p>
        <p>Madrid, Spain — 24 years old</p>
      </div>

      <!-- Profile Picture (on the far right) -->
      <div>
        <img style="border: 2px solid #555;" width="110" height="136" src="https://cdn.intra.42.fr/users/6d79a7e027d618814eabe63b048b628a/blarger.jpg" alt="Profile Picture"/>
      </div>

    </div>
  </div>

  <h2 style="padding-left: 6pt; text-indent: 0pt; text-align: left;">SUMMARY</h2>
  <p style="padding-left: 6pt; text-indent: 0pt; text-align: left;">Tech-savvy engineer with dual expertise in software development and market finance. Trained at 42 School and the University of Montpellier, with hands-on experience in data science, API design, and cloud deployment.</p>
  <p style="padding-left: 6pt; text-indent: 0pt; text-align: left;">Looking to drive impact as a Software Developer in a fast-paced, innovation-driven team. I am open to relocate.</p>
  <br/>

  <h2 style="padding-left: 6pt; text-indent: 0pt; text-align: left;">EDUCATION</h2>
  
  <h3 style="padding-left: 6pt; text-indent: 0pt; text-align: left;">
    Bootcamp 42 Spain - Data Science
    <span class="date">May 2025</span>
  </h3>
  <p style="padding-left: 6pt; text-indent: 0pt; text-align: left;">Machine learning with Scikit-Learn (supervised/unsupervised), data analysis with Pandas/NumPy, and visualization using Matplotlib/Seaborn. Solid grounding in regression, hypothesis testing, and time series. Completed projects in predictive modeling, segmentation, and decision support.</p>

  <h3 style="padding-top: 13pt; padding-left: 6pt; text-indent: 0pt; text-align: left;">
    42 Málaga Fundación Telefónica, Spain – Peer to Peer Training
    <span class="date">2023 – 2025</span>
  </h3>
  <p style="padding-left: 6pt; text-indent: 0pt; text-align: left;">Programming Engineering training – Common Core</p>
  <p style="padding-left: 6pt; text-indent: 0pt; text-align: left;"><u>Relevant Skills</u>: Web Server creation, 3D video game, shell replication, efficient sorting algorithm, Docker, MySQL</p>

  <h3 style="padding-top: 13pt; padding-left: 6pt; text-indent: 0pt; text-align: left;">
    University of Montpellier, France
    <span class="date">2019 – 2025</span>
  </h3>
  <p style="padding-left: 6pt; text-indent: 0pt; text-align: left;">Master's degree in Market Finance - Bachelor of Economics</p>
  <p style="padding-left: 6pt; text-indent: 0pt; text-align: left;"><u>Main classes</u>: Stochastic mathematics, Corporate finance, Python, VBA, Statistical modeling Exchange Program at University of Nebraska Omaha (United States – 2022)</p>
  <br/>

  <h2 style="padding-left: 6pt; text-indent: 0pt; text-align: left;">PROFESSIONAL EXPERIENCE</h2>
  
  <h3 style="padding-left: 6pt; text-indent: 0pt; text-align: left;">
    ENGIE Madrid, Spain
    <span class="date">January 2023 – June 2023</span>
  </h3>
  <h3 style="padding-left: 6pt; text-indent: 0pt; text-align: left;">IS Software Engineer Intern</h3>
  <ul id="l1">
    <li>
      <p style="padding-left: 14pt; text-indent: -7pt; text-align: left;">Collaborated with Back and Middle Office teams to implement tailored software solutions.</p>
    </li>
    <li>
      <p style="padding-left: 14pt; text-indent: -7pt; text-align: left;">Scraped data from internal software using Playwright to extract and process business-critical information.</p>
    </li>
    <li>
      <p style="padding-left: 6pt; text-indent: 0pt; text-align: left;">Developed Energy Management Solutions: Designed RESTful APIs in Python to optimize powerplant unit-commitment, integrating algorithmic efficiency and robust error handling.</p>
    </li>
    <li>
      <p style="padding-left: 14pt; text-indent: -7pt; text-align: left;">Dockerized Applications: Built containerized microservices for scalability purpose, deployed on AWS lambdas.</p>
    </li>
  </ul>

  <h3 style="padding-top: 13pt; padding-left: 6pt; text-indent: 0pt; text-align: left;">
    ING Brussels, Belgium
    <span class="date">May 2023 – September 2023</span>
  </h3>
  <h3 style="padding-left: 6pt; text-indent: 0pt; line-height: 13pt; text-align: left;">FEC Data Analyst Intern</h3>
  <ul id="l1">
    <li>
      <p style="padding-left: 14pt; text-indent: -7pt; line-height: 13pt; text-align: left;">Conducted Python data analytics projects to identify suspicious behaviours in a dataset of 10,000+ records.</p>
    </li>
    <li>
      <p style="padding-left: 14pt; text-indent: -7pt; text-align: left;">Developed VBA scripts to automate data processing tasks, reducing analysis time by 20%.</p>
    </li>
  </ul>

  <h2 style="padding-top: 9pt; padding-left: 6pt; text-indent: 0pt; text-align: left;">SIDE PROJECTS</h2>
  
  <h3 style="padding-left: 6pt; text-indent: 0pt; text-align: left;">Web Application: AI Agent for Financial News</h3>
  <p style="padding-left: 6pt; text-indent: 0pt; text-align: left;">Autonomous agent using LangChain, OpenAI API, and Pinecone to aggregate, summarize, and score stock-related news. Includes real-time data scraping (BeautifulSoup/NewsAPI), sentiment analysis, and a Streamlit dashboard.</p>

  <h3 style="padding-top: 13pt; padding-left: 6pt; text-indent: 0pt; text-align: left;">Data Science: Multiclass Logistic Regression from Scratch</h3>
  <p style="padding-left: 6pt; text-indent: 0pt; text-align: left;">Implemented one-vs-all logistic regression using NumPy and gradient descent with regularization. Evaluated performance (accuracy, precision, recall) and compared with scikit-learn baseline. Used UCI datasets for testing.</p>
  <br/>

  <h2 style="padding-left: 6pt; text-indent: 0pt; text-align: left;">SKILLS, LANGUAGES &amp; HOBBIES</h2>
  <ul id="l1">
    <li>
      <p style="padding-left: 14pt; text-indent: -8pt; text-align: left;"><u>Technical Skills:</u> Python, C/C++, Bash, Docker, AWS Lambda, Scikit-learn, SQL, Unit Test, Django, REST API</p>
    </li>
    <li>
      <p style="padding-left: 14pt; text-indent: -8pt; text-align: left;"><u>Tools</u>: Git, Playwright, Matplotlib, Seaborn, VirtualBox, DBeaver, Copilot, CrewAI, LangChain, NumPy, GitHub</p>
    </li>
    <li>
      <p style="padding-left: 14pt; text-indent: -8pt; text-align: left;"><u>Languages</u>: French (native); English (fluent); Spanish (fluent)</p>
    </li>
    <li>
      <p style="padding-left: 14pt; text-indent: -8pt; text-align: left;"><u>Hobbies:</u> Blockchain technology, Artificial Intelligence, Golf<span class="s2">, </span>Personal Development</p>
    </li>
  </ul>

</body>
</html>
'''

# PDF path to save
pdf_path = 'example_from_html.pdf'

# Generate PDF
asyncio.run(html_to_pdf(html_content, pdf_path))
