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
