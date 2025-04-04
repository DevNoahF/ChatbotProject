# config/settings.py
# gpt-4o-mini
import os
from dotenv import load_dotenv

load_dotenv()  # Carregar variáveis do .env

# gpt - 3.5 turbo
OPENIA_API_KEY = os.getenv("OPENIAROUTER_API_KEY")
MAX_TOKENS = 20
