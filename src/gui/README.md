# CV Generator Streamlit UI

This directory contains the Streamlit web interface for the CV Generator application.

## Structure

- `app.py`: Main Streamlit application file
- `__init__.py`: Package initialization file

## Extending the UI

To add new features to the UI:

1. Modify `app.py` to add new UI components
2. Update the inputs passed to the CrewAI workflow
3. Enhance the document preview and download sections as needed

## UI Components

The current UI includes:

- CV upload section
- Job description input (text, file, or URL)
- Generation button
- Document preview tabs
- Download links for generated files

## Data Flow

1. User inputs are collected through the Streamlit interface
2. Inputs are passed to the CrewAI workflow
3. CrewAI agents process the data and generate documents
4. Generated files are saved to the output directory
5. UI reads the output directory and provides previews/downloads

## Adding New Features

When adding new features, ensure they are properly integrated with the existing CrewAI workflow. You can add new tools to `tools.py` and update the agents and tasks as needed.

Example of adding a new feature:

```python
# Add a new UI section
st.header("New Feature")
new_input = st.text_input("Enter new information")

# Add the new input to the CrewAI inputs
inputs = {
    'job_offer_url': job_url,
    'job_offer_fallback': job_description,
    'cv_template': load_cv_template(),
    'cover_letter_template': load_cover_letter_template(),
    'new_input': new_input,  # Add the new input
}
```
