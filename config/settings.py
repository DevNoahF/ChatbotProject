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
