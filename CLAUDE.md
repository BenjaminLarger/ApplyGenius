# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a CrewAI-powered CV and cover letter generator that automatically tailors resumes for specific job applications. The system uses multiple AI agents to analyze job postings, match skills, and generate customized HTML/PDF documents.

## Architecture

The project consists of two main components:
- **Backend**: CrewAI workflow with specialized agents for document generation
- **Frontend**: Streamlit web interface for user interaction

### Agent System
The CrewAI system uses 5 specialized agents:
1. **Job Analyst**: Scrapes and analyzes job postings
2. **Skills Matcher**: Maps candidate skills to job requirements  
3. **CV HTML Generator**: Creates tailored HTML CVs
4. **Cover Letter Generator**: Creates personalized cover letters
5. **PDF Generator**: Converts HTML documents to PDF

### Key Directories
- `src/cv_gen/` - Core CrewAI implementation and agents
- `src/cv_gen/config/` - Agent definitions, tasks, and HTML templates
- `src/cv_gen/tools/` - Custom tools for scraping and PDF conversion
- `src/gui/` - Streamlit web interface
- `output/` - Generated documents (HTML and PDF)
- `logs/` - Task execution logs

## Development Commands

### Setup and Dependencies
```bash
# Install dependencies (Poetry preferred)
poetry install
poetry lock

# Alternative with pip
pip install -r requirements.txt

# Install Playwright for PDF conversion
playwright install chromium
```

### Running the Application
```bash
# Command line interface
poetry run cv_gen

# Web interface  
./run_ui.sh
# OR
PYTHONPATH=$PYTHONPATH:$(pwd) streamlit run src/gui/app.py
```

### Testing
```bash
# Run UI tests (requires Selenium)
pip install -r requirements_test.txt
python tests/test_ui.py

# Manual testing via web interface at http://localhost:8501
```

## Configuration

### Environment Variables
Required in `.env` file:
- `OPENAI_API_KEY` - Primary LLM provider
- `ANTHROPIC_API_KEY` - Alternative LLM provider (optional)

### Key Configuration Files
- `src/cv_gen/config/agents.yaml` - Agent definitions and backstories
- `src/cv_gen/config/tasks.yaml` - Task workflow and dependencies
- `src/cv_gen/config/cv_template.html` - CV HTML template
- `src/cv_gen/config/cover_letter_template.html` - Cover letter template
- `src/cv_gen/config/job_offer.txt` - Default job description fallback

## Workflow Process

1. **Input**: Job posting URL or text description
2. **Job Analysis**: Extract requirements, skills, company info
3. **Skills Matching**: Score and prioritize candidate skills vs requirements
4. **Document Generation**: Create tailored HTML CV and cover letter
5. **PDF Conversion**: Convert HTML to professional PDF documents

## Technical Implementation Details

### CrewAI Integration
- Agents defined with specific roles, goals, and backstories
- Sequential task execution with dependency management
- Custom tools for web scraping (`JobPostingScraper`) and PDF conversion (`ConverterHtmlToPdf`)

### Streamlit UI Features
- Multiple input methods: URL, text paste, file upload, sample jobs
- Real-time preview of generated documents
- Download functionality for HTML and PDF versions
- Error handling and progress indicators

### Document Templates
- Jinja2-style HTML templates for CV and cover letter
- Responsive design with professional styling
- Dynamic content population based on job analysis

## Important Notes

- PDF conversion requires Playwright with Chromium browser
- The system maintains original template structure while adapting content
- Generated documents are timestamped and saved to `output/` directory
- Fallback mechanisms ensure robustness (URL scraping → text fallback)
- All agent interactions are logged for debugging and analysis