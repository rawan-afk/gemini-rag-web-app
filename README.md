# Gemini RAG Web Application

A web-based Retrieval-Augmented Generation (RAG) application developed collaboratively during our training at the Financial Regulatory Authority (FRA).

The application combines the Google Gemini API with a document-based RAG pipeline to allow users to ask questions about regulatory documents and receive answers based on relevant retrieved context.

## Project Overview

The system follows a complete RAG pipeline:

PDF Document
↓
Text Extraction / OCR
↓
Text Cleaning
↓
Chunking
↓
Embeddings
↓
Semantic Retrieval
↓
Relevant Context
↓
Gemini
↓
Generated Answer

## Features

- Gemini-powered chatbot
- Retrieval-Augmented Generation (RAG)
- Arabic regulatory document processing
- Text cleaning and normalization
- Overlapping text chunking
- Gemini embeddings
- Semantic similarity search
- Cosine similarity-based retrieval
- FastAPI backend
- Web-based frontend
- Conversational chat history

## Technologies

- Python
- FastAPI
- Google Gemini API
- Gemini Embeddings
- NumPy
- Pydantic
- python-dotenv
- HTML
- CSS
- JavaScript

## Team

This project was developed collaboratively during our training at the Financial Regulatory Authority (FRA).

- Rawan Walid — https://github.com/rawan-afk
- Darine Farrag — https://github.com/darinefarrag-droid
- Rana Saied — https://github.com/rana576

## Training Context

The project was developed as part of our practical training at the Financial Regulatory Authority (FRA), where we worked together on LLM, NLP, RAG, and AI application development.

## Disclaimer

This project is intended for educational and demonstration purposes. Generated responses should not be considered legal or regulatory advice.
