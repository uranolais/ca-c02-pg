import anthropic
import dotenv
import os
from helpers import *

dotenv.load_dotenv()
cliente = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)
modelo = "claude-3-5-sonnet-20240620"
ferramentas = [
    {
        "name": "pega_detalhes_do_pedido",
        "description": "Recupera os detalhes de um pedido específico com base no CÓDIGO do pedido. Retorna o CÓDIGO do pedido, preço e status do pedido.",
        "input_schema": {
            "type": "object",
            "properties": {
                "codigo_pedido": {
                    "type": "string",
                    "description": "O identificador único do pedido"
                }
            },
            "required": ["codigo_pedido"]
        }
    },
    {
        "name": "cancela_pedido",
        "description": "Cancela um pedido com base no CÓDIGO do pedido fornecido. Retorna uma mensagem de confirmação se o cancelamento for bem-sucedido.",
        "input_schema": {
            "type": "object",
            "properties": {
                "codigo_pedido": {
                    "type": "string",
                    "description": "O identificador único do pedido a ser cancelado."
                }
            },
            "required": ["codigo_pedido"]
        }
    }
]

def pega_detalhes_do_pedido(codigo_pedido):
    pedidos = {
        "C001": {"id": "O1", "preço": "R$25.00", "status": "Em Rota de Entrega"},
        "C002": {"id": "O2", "preço": "R$43.00", "status": "Confirmado"},
    }
    return pedidos.get(codigo_pedido, "Pedido não encontrado")

def cancela_pedido(codigo_pedido):
    if codigo_pedido in ["C001", "C002"]:
        return True
    else:
        return False

def processa_chamada_de_ferramenta(tool_name, tool_input):
    if tool_name == "pega_detalhes_do_pedido":
        return pega_detalhes_do_pedido(tool_input["codigo_pedido"])
    elif tool_name == "cancela_pedido":
        return cancela_pedido(tool_input["codigo_pedido"])


def chamar_ferramenta(prompt):
    prompt_do_usuario = prompt
    try:
        mensagem = cliente.messages.create(
            model=modelo,
            max_tokens=4000,
            temperature=0,
            tools=ferramentas,
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
        print(mensagem)
        print(f"Motivo de Parada: {mensagem.stop_reason}")
        print(f"Conteúdo: {mensagem.content[0].text}")
        return mensagem
    except anthropic.APIConnectionError as e:
        print("O servidor não pode ser acessado! Erro:", e.__cause__)
    except anthropic.RateLimitError as e:
        print("Um status code 429 foi recebido! Limite de acesso atingido.")
    except anthropic.APIStatusError as e:
        print(f"Um erro {e.status_code} foi recebido. Mais informações: {e.response}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

prompt = "Qual é o status do meu pedido C001?"
chamar_ferramenta(prompt)