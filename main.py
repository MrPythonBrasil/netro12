import requests
import random
import string
import time
import sys
import os

# Função para enviar a mensagem com o link do código gerado para o Webhook do Discord
def send_webhook(webhook_url, message):
    payload = {"content": message}  # A mensagem será o link do código gerado com o emoji de foguete
    try:
        response = requests.post(webhook_url, json=payload)

        # Verificar resposta do Webhook
        if response.status_code == 204:
            print(f"Link enviado com sucesso!")  # Sucesso ao enviar
        else:
            print(f"Erro ao enviar mensagem para o webhook. Status Code: {response.status_code}")  # Erro no envio
            print(f"Detalhes do erro: {response.text}")  # Mostrar resposta do erro
    except Exception as e:
        print(f"Erro ao enviar mensagem para o webhook: {e}")  # Caso ocorra algum erro ao enviar

# Função principal de geração de códigos Nitro
class SapphireGen:
    def __init__(self, code_type: str, webhook_url: str):
        self.type = code_type
        self.session = requests.Session()
        self.webhook_url = webhook_url

    def generate(self):
        while True:  # Loop infinito para continuar gerando os códigos sem parar
            try:
                # Gerar código aleatório (24 caracteres para "boost", 16 para "classic")
                code = "".join(
                    random.choices(string.ascii_letters + string.digits, k=24 if self.type == "boost" else 16)
                )

                # Formatar o link para o código
                discord_link = f"discord.gift/{code}"

                # Adicionar o emoji de foguete
                message = f"🚀 {discord_link}"

                # Enviar o código gerado para o Webhook
                send_webhook(self.webhook_url, message)  # Envia o link para o Webhook

                time.sleep(1)  # Pausar por 1 segundo para não sobrecarregar o Webhook

            except Exception as e:
                print(f"Erro ao gerar o código: {e}")  # Caso ocorra algum erro

if __name__ == "__main__":
    # URL do Webhook do Discord (atualizado com a URL fornecida)
    webhook_url = "https://discord.com/api/webhooks/1346137737832431716/OZbSTAjFQDs-_lAny_bfLxW0KLMZ4BRGr0E1yCzr3qsS7GCthQzigOMfV1Z_8hH-4Pde"

    # Tipo de código ("boost" ou "classic")
    code_type = "boost"  # Pode ser "boost" ou "classic"

    # Passando os parâmetros para a classe SapphireGen
    SapphireGen(code_type, webhook_url).generate()
