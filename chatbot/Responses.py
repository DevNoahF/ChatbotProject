# services/responses.py



import json
import requests
from config.settings import ROUTEROPENIA_API_KEY, change_tokens
import spacy
import os


nlp=spacy.load("pt_core_news_lg")#Carrega o spacy


# Função para carregar o contexto do template com base no ID
def load_template_context(template_id):
    try:
        with open(f"templates_contexto/{template_id}.json", "r", encoding="utf-8") as f:
            return json.load(f)["contexto"]
    except FileNotFoundError:
        return "Você é um assistente virtual de atendimento. Seja educado, claro e objetivo."

# Função principal de resposta do bot
def get_bot_reply(user_message, template_id="loja_designs"): # Mudar o template se necessario
    contexto = load_template_context(template_id)

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {ROUTEROPENIA_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": contexto},
                {"role": "user", "content": user_message}
            ],
            "temperature": 0.7,
            "max_tokens": change_tokens(user_message),
            "presence_penalty": 0.3,
            "top_p": 0.8
        }
    )

    return response.json()["choices"][0]["message"]["content"]

def idnt_question(message):
    base_path = os.path.dirname(os.path.abspath(__file__))
    caminho_arquivo = os.path.join(base_path, "Perguntas/Perguntas.json")
    similaridade=0.0
    mes=nlp(message)

    with open(caminho_arquivo, "r") as file:
        dados=json.load(file)

    pergunta=None
    sim=0.0
    for perguntas in dados["perguntas"]:
        texto_pergunta = perguntas["pergunta"]
        doc_pergunta = nlp(texto_pergunta)
        similaridade=mes.similarity(doc_pergunta)
        if sim<similaridade:
            sim=similaridade
            pergunta=doc_pergunta

    if similaridade>=0.61:
        return 0

    if similaridade<=0.60:

        return pergunta

    return 1


def palavras_chave(mensagem):
    palavras=["frete","produto", "valores", "plano", "Design","chatbot", "suporte", "loja virtual", "vantagens","planos","suporte","assistencia técnica" ]#Aqui fica as palavras chave que são RELEVANTES, as que não estiverem aqui não serão relevantes

    for palavras in palavras:
        if palavras.lower() in mensagem.lower():
            return True
    return False

