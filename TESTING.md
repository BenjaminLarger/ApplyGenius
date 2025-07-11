# CV Generator UI Testing Guide

This guide explains how to test the Streamlit UI for the CV Generator application.

## Prerequisites

Install the testing dependencies:

```bash
pip install -r requirements_test.txt
```

These dependencies include:
- Selenium for browser automation
- Webdriver Manager for managing browser drivers
- Requests for HTTP requests

## Running the UI

Before testing, start the Streamlit UI:

```bash
./run_ui.sh
```

Or directly with Python:

```bash
cd /home/blarger/Desktop/projects/AI-Agents/finvest-news-ai
PYTHONPATH=$PYTHONPATH:$(pwd) streamlit run src/gui/app.py
```

The UI will be available at http://localhost:8501

## Automated Testing

The `tests/test_ui.py` script provides automated testing for the Streamlit UI. It uses Selenium to interact with the UI and test different input methods.

Run the automated tests:

```bash
python tests/test_ui.py
```

The script will:
1. Test the URL input method with a sample job posting URL
2. Test the text input method with a sample job description
3. Verify that all output files are generated correctly

## Manual Testing

For manual testing, follow these steps:

1. **Test URL Input**:
   - Open the UI at http://localhost:8501
   - Select "Provide URL" input method
   - Enter a job posting URL (e.g., LinkedIn, Indeed)
   - Click "Generate CV & Cover Letter"
   - Verify that documents are generated and can be downloaded

2. **Test Text Input**:
   - Open the UI at http://localhost:8501
   - Select "Paste text" input method
   - Paste a job description
   - Click "Generate CV & Cover Letter"
   - Verify that documents are generated and can be downloaded

3. **Test File Upload**:
   - Open the UI at http://localhost:8501
   - Select "Upload file" input method
   - Upload a text file containing a job description
   - Click "Generate CV & Cover Letter"
   - Verify that documents are generated and can be downloaded

4. **Test Sample Jobs**:
   - Open the UI at http://localhost:8501
   - Select "Use sample" input method
   - Choose one of the sample job descriptions
   - Click "Generate CV & Cover Letter"
   - Verify that documents are generated and can be downloaded

5. **Error Handling**:
   - Test without providing a job description
   - Test with a malformed URL
   - Test with an API key that is not set
   - Verify that appropriate error messages are displayed

## Verifying Generated Documents

After generating documents, verify:

1. **HTML Preview**:
   - Both CV and cover letter should be visible in the preview tabs
   - Content should be correctly formatted and readable

2. **PDF Generation**:
   - Download the PDF files and open them
   - Check that formatting is preserved
   - Ensure all content is readable and properly laid out

3. **Content Relevance**:
   - Check that the generated CV highlights skills relevant to the job posting
   - Verify that the cover letter addresses the job requirements

## Common Issues and Solutions

1. **Missing Output Files**:
   - Check the output directory to see if files were generated
   - Check the application logs for errors
   - Verify that the application has write permissions to the output directory

2. **API Key Issues**:
   - Ensure the OpenAI API key is set in the `.env` file
   - Check that the API key is valid and has sufficient credits

3. **Browser Automation Issues**:
   - Make sure Chrome or Chromium is installed for Selenium testing
   - If headless mode doesn't work, try without the `--headless` option

## Reporting Issues

If you encounter issues during testing:

1. Take screenshots of any error messages
2. Note the steps to reproduce the issue
3. Check the application logs for detailed error information
4. Report the issue with all collected information
