import requests
import random
import string

# Função para enviar a mensagem com o link do código gerado para o Webhook do Discord
def send_webhook(webhook_url, message):
    payload = {"content": message}  # A mensagem será o link do código gerado
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

                # Formatar o link para o código
                discord_link = f"discord.gift/{code}"

                # Verificar se o código foi gerado antes
                if discord_link in generated_codes:
                    continue
                generated_codes.add(discord_link)

                # Enviar o código gerado para o Webhook
                send_webhook(self.webhook_url, discord_link)  # Envia o link para o Webhook
                valid_codes += 1

            except Exception as e:
                print(f"Erro ao gerar o código: {e}")  # Caso ocorra algum erro

if __name__ == "__main__":
    # URL do Webhook do Discord (atualizado com a URL fornecida)
    webhook_url = "https://discord.com/api/webhooks/1346091036056883292/Y5xNeLE3w_pXz5w64w8IJZg0NleLhQe0dSv-lCziKud7DYyd2rc7NYwejwtVFEZP-tSA"

    # Tipo de código ("boost" ou "classic")
    code_type = "boost"  # Pode ser "boost" ou "classic"

    # Quantidade de códigos válidos a serem gerados
    codes_to_generate = 10  # Modifique o número conforme necessário

    # Passando os parâmetros para a classe SapphireGen
    SapphireGen(code_type, codes_to_generate, webhook_url).generate()
