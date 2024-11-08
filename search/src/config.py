import os

# Azure OpenAI API konfigurace
AZURE_API_KEY = os.getenv('AZURE_OPENAI_API_KEY', '')
AZURE_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT', 'https://abcf-openai.openai.azure.com/')
AZURE_EMBEDDING_DEPLOYMENT_ID = os.getenv('AZURE_EMBEDDING_DEPLOYMENT_ID', 'text-embedding-3-large')
AZURE_GPT_DEPLOYMENT_ID = os.getenv('AZURE_GPT_DEPLOYMENT_ID', 'gpt-4o')

# Chroma DB konfigurace
CHROMA_DB_PATH = os.getenv('CHROMA_DB_PATH', 'chroma_db')