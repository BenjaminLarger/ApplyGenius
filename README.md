# CV Generator with CrewAI

This project uses CrewAI to automatically tailor CVs for specific job applications. It analyzes job postings, matches skills to requirements, and generates a customized HTML CV ready for submission.

## Key Features

- **Job Analysis**: Extracts critical requirements from job postings
- **Skills Matching**: Maps candidate skills to job requirements
- **HTML CV Generation**: Creates a professionally formatted CV in HTML
- **PDF Conversion**: Converts HTML CVs to PDF format for submission

## Installation

Ensure you have Python >=3.10 <=3.13 installed on your system. This project uses [Poetry](https://python-poetry.org/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install Poetry:

```bash
pip install poetry
```

Next, navigate to your project directory and install the dependencies:

1. First lock the dependencies and then install them:
```bash
poetry lock
```
```bash
poetry install
```

### Alternatively, you can use pip:

```bash
pip install -r requirements.txt
```

## Configuration

**Set your API keys in the `.env` file**

```
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here  # Optional
```

## Usage

1. Start the Streamlit interface:

```bash
poetry run streamlit run src/gui/app.py
```

2. Paste the job posting text into the input field
3. Click "Generate CV" to start the process
4. The system will analyze the job, match skills, and generate a tailored CV
5. Download the HTML or PDF version of your customized CV

## Customizing

- Modify `src/newsletter_gen/config/agents.yaml` to define your agents
- Modify `src/newsletter_gen/config/tasks.yaml` to define your tasks
- Modify `src/newsletter_gen/config/cv_template.html` to change the CV template
- Modify `src/newsletter_gen/crew.py` to add your own logic and tools

## Converting HTML to PDF

The system uses Playwright to convert HTML CVs to PDF format. Make sure Playwright is properly installed:

```bash
playwright install chromium
```

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
poetry run newsletter_gen
```

This command initializes the newsletter-gen Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folser

## Understanding Your Crew

The newsletter-gen Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding the NewsletterGen Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Joing our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat wtih our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
