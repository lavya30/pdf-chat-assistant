# pdf-chat-assistant

A Streamlit web app that enables users to upload a PDF and interactively query its contents using language models and embeddings.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Requirements](#requirements)
- [Contribution](#contribution)
- [License](#license)
- [Contact](#contact)

## Introduction
**pdf-chat-assistant** is a tool for generating executive summaries and extracting information from PDF documents through natural language questions. Users can upload a PDF and ask questions; the app will provide AI-generated answers based strictly on the document's context.

## Features
- Upload and process PDF documents
- Extract text, split into chunks, and embed them for efficient search
- Query the document using natural language and get accurate, context-based answers
- Built with Streamlit for a simple, responsive web UI
- Uses HuggingFace embeddings, FAISS vector store, and LangChain for advanced retrieval

## Installation
```bash
# Clone the repository
https://github.com/lavya30/pdf-chat-assistant.git
cd pdf-chat-assistant

# (Optional) Create a new virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage
```bash
streamlit run streamlit_app.py
```

- Open your browser to the local Streamlit address provided in the terminal.
- Upload a PDF in the app. Enter your queries in the textbox.

## Requirements
See `requirements.txt` for all packages, including:
- streamlit
- langchain
- langchain-community
- langchain-groq
- faiss-cpu
- sentence-transformers
- python-dotenv
- pypdf

## Contribution
Contributions are welcome! Feel free to fork this repo, open issues, or submit pull requests.

## License
MIT License

## Contact
Maintainer: lavya30  
GitHub: https://github.com/lavya30
