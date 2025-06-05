import os
import json
import string
import requests
import spacy
from typing import Union, Tuple
from config.settings import ROUTEROPENIA_API_KEY, change_tokens

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

# Download necessário (pode comentar depois de rodar a primeira vez)
nltk.download('punkt')
nltk.download('stopwords')

# NLP Setup
nlp = spacy.load("pt_core_news_lg")
stop_words = set(stopwords.words('portuguese'))

#
# ==========================
# PRÉ-PROCESSAMENTO DE TEXTO
# ==========================

def preprocess_text(text: str) -> str:
    tokens = word_tokenize(text.lower(), language='portuguese')
    clean_tokens = [t for t in tokens if t not in stop_words and t not in string.punctuation]
    return " ".join(clean_tokens)

# ==========================
# SIMILARIDADE ENTRE PERGUNTAS
# ==========================

def idnt_question(message: str) -> Union[int, Tuple[str, float]]:
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, "Perguntas", "Perguntas.json")

    try:
        with open(file_path, encoding="utf-8") as f:
            dados = json.load(f)
    except FileNotFoundError:
        return 1

    user_doc = nlp(preprocess_text(message))

    melhor_sim = 0.0
    pergunta_mais_proxima = None

    for item in dados.get("perguntas", []):
        pergunta_doc = nlp(item.get("pergunta", ""))
        sim = user_doc.similarity(pergunta_doc)
        if sim > melhor_sim:
            melhor_sim = sim
            pergunta_mais_proxima = item.get("pergunta")

    if melhor_sim >= 0.61:
        return 0
    elif melhor_sim >= 0.45:
        return pergunta_mais_proxima, melhor_sim
    else:
        return 1

# ==========================
# INTENÇÕES COM PALAVRAS-CHAVE
# ==========================

def palavras_chave(mensagem: str) -> bool:
    palavras_relevantes = [
        # Suplementos e produtos
        "whey", "whey protein", "creatina", "bcaa", "termogênico", "pré-treino", "glutamina", "multivitamínico",
        "hipercalórico", "caseína", "colágeno", "omega 3", "zma", "cafeína","produto","produtos","peso","massa"

        # Objetivos e benefícios
        "ganho de massa", "hipertrofia", "definição muscular", "perder gordura", "emagrecimento", "energia para treino",
        "recuperação muscular", "rendimento", "performance", "força", "resistência",

        # Dúvidas comuns
        "como tomar", "efeitos colaterais", "posso misturar", "horário ideal", "preciso ciclar",
        "quanto tempo para ver resultado", "faz mal", "funciona mesmo", "para que serve",

        # Compra e suporte
        "comprar", "loja", "entrega", "frete", "disponível", "em estoque", "formas de pagamento", "parcelamento",
        "promoção", "desconto", "cupom", "oferta", "garantia", "troca", "reembolso", "devolução",

        # Atendimento
        "atendimento", "ajuda", "contato", "fale conosco", "suporte", "chatbot", "assistente virtual"
    ]

    mensagem_lower = mensagem.lower()
    return any(palavra in mensagem_lower for palavra in palavras_relevantes)

