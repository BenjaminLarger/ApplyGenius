#!/bin/bash
# Run the Streamlit app with the correct Python path
cd "$(dirname "$0")"
export PYTHONPATH=$PYTHONPATH:$(pwd)
streamlit run src/gui/app.py
