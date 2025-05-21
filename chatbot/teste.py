import json
import os

base_path = os.path.dirname(os.path.abspath(__file__))
caminho_arquivo = os.path.join(base_path, "Perguntas/Perguntas.json")



# Abrir e ler o arquivo JSON
with open("Perguntas/Perguntas.json","r") as arquivo:
    dados = json.load(arquivo,)

# Acessar os dados
print(dados["perguntas"][0]["pergunta"])
