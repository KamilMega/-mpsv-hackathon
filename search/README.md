# Search Service with ChromaDB and Azure OpenAI

This project provides a RESTful API service for searching professions using semantic vector search powered by ChromaDB and Azure OpenAI embeddings. The project includes Python scripts for importing data into ChromaDB, a REST API for searching, and utilities to interact with Azure OpenAI models.

## Overview

This project enables semantic search functionality using ChromaDB as a vector store and Azure OpenAI for generating embeddings. The application consists of two main components:
1. A command-line script to import professions and their embeddings into ChromaDB.
2. A Flask-based REST API that allows users to search for professions based on query texts, leveraging Azure OpenAI for generating embeddings.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8+
- An Azure OpenAI subscription and API keys

## Installation

1. **Clone the repository:**

2. **Set up a virtual environment:**

   On Windows:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

   On macOS/Linux:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

You need to configure the API keys for Azure OpenAI and other services. This can be done by creating a `.env` file or by updating the `shared/config.py` file.

Example `.env` file:
```
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_ENDPOINT=https://your-openai-instance-url
AZURE_GPT_DEPLOYMENT_ID=gpt-4o-mini
AZURE_EMBEDDING_DEPLOYMENT_ID=text-embedding-3-small
CHROMA_DB_PATH=chroma_db/
```

## Usage

### Importing Data into ChromaDB

To import data from a JSON file into ChromaDB, run the following command:

```bash
python scripts/import_professions.py
```

Make sure the `professions.json` file is present in the `data/` directory.

### Running the API

You can start the Flask API by running:

```bash
python -m src.server.app
```

The API will be accessible at `http://localhost:5000`.

### Exporting Data from ChromaDB

To export data (including document IDs, documents, and embeddings) from ChromaDB to a CSV or JSON file, run:

```bash
python scripts/export_data.py --format csv --output export.csv
```

Available formats: `json`, `csv`.

## API Endpoints

### Search Endpoint

**GET** `/search`

Search for professions based on a query string.

#### Query Parameters:

- `search_text` (required): The text to search for.
- `n_results` (optional): Number of results to return (default is 50).

#### Example Request:

```bash
curl "http://localhost:5000/search?search_text=software developer"
```

#### Example Response:

```json
{
  "results": [
    { "document": "Software Developer" },
    { "document": "Backend Engineer" },
    { "document": "Frontend Developer" }
  ]
}
```

## Environment Variables

- `AZURE_OPENAI_API_KEY`: Your Azure OpenAI API key.
- `AZURE_OPENAI_ENDPOINT`: Azure OpenAI endpoint URL.
- `AZURE_OPENAI_DEPLOYMENT_ID`: Deployment ID for generating embeddings.
- `CHROMA_DB_PATH`: Path to ChromaDB data storage.

## Virtual Environment

This project uses a virtual environment for dependency management. Follow these steps to activate the virtual environment:

### Activate Virtual Environment:

- **Windows:**
  ```bash
  .\venv\Scripts\activate
  ```

- **macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```