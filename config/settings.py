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
