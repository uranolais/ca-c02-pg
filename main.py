from flask import Flask,render_template, request, Response # type: ignore
from bot import bot
from helpers import *
import os
from resumidor_de_historico import criar_resumo

app = Flask(__name__)
app.secret_key = 'alura'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods = ['POST'])
def chat():
    prompt = request.json["msg"]
    nome_do_arquivo = './historico/historico_SaborExpress'
    historico = ''
    if os.path.exists(nome_do_arquivo):
        historico = carrega(nome_do_arquivo)
    historico_resumido = criar_resumo(historico)
    resposta = bot(prompt, historico_resumido)
    conteudo = f"""
    Histórico: {historico_resumido}
    Usuário: {prompt}
    IA: {resposta}
    """
    salva(nome_do_arquivo,conteudo)
    return resposta

@app.route("/limparhistorico", methods = ["POST"])
def limpar_historico():
    nome_do_arquivo = './historico/historico_SaborExpress'
    if os.path.exists(nome_do_arquivo):
        os.remove(nome_do_arquivo)
        print("Arquivo de histórico removido!")
    else: 
        print("Não foi possivel remover esse arquivo!")
    return {}


if __name__ == "__main__":
    app.run(debug = True)