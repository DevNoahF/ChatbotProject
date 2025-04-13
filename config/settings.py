# config/Settings.py
# gpt-4o-mini
import os
from dotenv import load_dotenv

load_dotenv()  # Carregar variáveis do .env

# gpt - 3.5 turbo
ROUTEROPENIA_API_KEY = "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"

def change_tokens(mensagem):#Função que altera os tokens, leva em conta a quantidade de palavras presente na mensagem do usuário
    mensagem.split()
    qtd=len(mensagem)

    return 5*qtd
