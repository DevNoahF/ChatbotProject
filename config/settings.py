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
