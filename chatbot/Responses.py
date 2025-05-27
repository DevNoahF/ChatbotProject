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

# ==========================
# CONTEXTO DE TEMPLATE
# ==========================

def load_template_context(template_id: str) -> str:
    try:
        with open(f"templates_contexto/{template_id}.json", encoding="utf-8") as f:
            return json.load(f).get("contexto", "")
    except FileNotFoundError:
        return "Você é um assistente virtual de atendimento. Seja educado, claro e objetivo."

# ==========================
# CHAMADA GPT
# ==========================

def get_bot_reply(user_message: str, template_id: str = "loja_designs") -> str:
    contexto = load_template_context(template_id)
    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": contexto},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.3,
        "max_tokens": min(150, change_tokens(user_message)),
        "presence_penalty": 0.3,
        "top_p": 0.8
    }
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {ROUTEROPENIA_API_KEY}",
                "Content-Type": "application/json"
            },
            json=payload
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception:
        return "Desculpe, ocorreu um erro ao tentar gerar a resposta. Tente novamente em instantes."

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
        "suporte", "atendimento", "contato", "ajuda", "assistência", "fale conosco", "central de atendimento", "suporte técnico",
        "chatbot", "assistente virtual", "bot", "chat online", "chat ao vivo",
        "pedido", "compra", "status", "andamento", "rastrear", "acompanhar pedido", "situação do pedido",
        "24 horas", "tempo integral", "atendimento contínuo", "atendimento sempre disponível",
        "vantagens", "benefícios", "promoções", "ofertas", "descontos", "planos", "assinatura", "pacotes", "melhor preço",
        "cadastrar", "inscrever", "registrar", "novidades", "promoções", "ofertas especiais", "novos produtos",
        "garantia", "reembolso", "troca", "devolução", "suporte pós-venda",
        "fidelidade", "recompensas", "programa de pontos", "benefícios exclusivos",
        "personalizar", "design", "layout", "customizar", "cores", "opções de cor", "variações de cor", "visualização",
        "custos adicionais", "taxas extras", "formas de pagamento", "meios de pagamento", "parcelamento", "pagamento à vista", "à vista", "desconto",
        "código promocional", "cupom", "voucher", "promo code",
        "estoque", "disponibilidade", "produtos disponíveis",
        "planos de assinatura", "assinatura", "plano", "pacote", "personalização"
    ]

    mensagem_lower = mensagem.lower()
    return any(palavra in mensagem_lower for palavra in palavras_relevantes)
