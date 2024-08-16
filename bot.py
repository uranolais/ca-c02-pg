import anthropic
import dotenv
import os
from helpers import *
from identificar_persona import *
from identificar_contexto import *
from analisador_de_imagem import *

dotenv.load_dotenv()
cliente = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)
modelo = "claude-3-5-sonnet-20240620"
# contexto = carrega('./dados/SaborExpress.txt')

def bot(prompt,historico, caminho_da_imagem):
    personalidade = personas[identificar_persona(prompt)]
    contexto = identificar_contexto(prompt)
    documento_contexto = selecionar_documento(contexto)
    prompt_do_sistema = f"""
    Você é um chatbot de atendimento a clientes de um aplicativo de entrega para restaurantes, padarias, mercados e farmácias.
    Você não pode e nem deve responder perguntas que não sejam dados do aplicativo informado!
    Você deve gerar respostas utilizando o contexto abaixo.
    Você deve adotar a persona abaixo para responder a mensagem.
    Você deve considerar o histórico da conversa.
            
    # Contexto
    {documento_contexto}

    # Persona
    {personalidade}

    # Historico
    {historico}
    """
    analise_da_imagem = ''
    if caminho_da_imagem != None:
        analise_da_imagem = analisar_imagem(caminho_da_imagem)
        analise_da_imagem += '. Na resposta final, apresente detalhes da descrição da imagem'
        os.remove(caminho_da_imagem)
        caminho_da_imagem = None
        
    prompt_do_usuario = prompt + analise_da_imagem
    try:
        mensagem = cliente.messages.create(
            model=modelo,
            max_tokens=4000,
            temperature=0,
            system=prompt_do_sistema,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt_do_usuario
                        }
                    ]
                }
            ]
        )
        resposta = mensagem.content[0].text
        return resposta, caminho_da_imagem
    except anthropic.APIConnectionError as e:
        print("O servidor não pode ser acessado! Erro:", e.__cause__)
    except anthropic.RateLimitError as e:
        print("Um status code 429 foi recebido! Limite de acesso atingido.")
    except anthropic.APIStatusError as e:
        print(f"Um erro {e.status_code} foi recebido. Mais informações: {e.response}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
