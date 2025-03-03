import sys
import time
from time import localtime, strftime, sleep
import requests
import random
import string
import os
import re  # Para remover sequências de controle de cor

# Função para enviar mensagens para o Webhook do Discord
def send_webhook(webhook_url, message):
    # Remover sequências de controle de cor
    message = re.sub(r'\x1b\[[0-9;]*m', '', message)  # Regex para remover as sequências ANSI (código de cor)

    payload = {"content": message}
    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 204:
            print(f"[{strftime('%H:%M', localtime())}] Mensagem enviada para o webhook.")
        else:
            print(f"[{strftime('%H:%M', localtime())}] Erro ao enviar mensagem para o webhook.")
    except Exception as e:
        print(f"[{strftime('%H:%M', localtime())}] Erro ao enviar mensagem para o webhook: {e}")

# Função principal de geração de códigos
class SapphireGen:
    def __init__(self, code_type: str, prox=None, codes=None, webhook_url=None):
        self.type = code_type
        self.codes = int(codes)
        self.proxies = prox
        self.session = requests.Session()
        self.prox_api = (
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"
        )
        self.webhook_url = webhook_url

    def __proxies__(self):
        req = self.session.get(self.prox_api).text
        if req:
            open("./data/proxies.txt", "w").write(req.strip())

    def send_webhook(self, message):
        send_webhook(self.webhook_url, message)

    def generate(self, scrape=None):
        if scrape == "True":
            self.__proxies__()

        os.system("cls" if os.name == "nt" else "clear")
        print(f"Iniciando geração de códigos...")

        valid_codes = 0
        generated_codes = set()
        while valid_codes < self.codes:
            try:
                if self.proxies == "True":
                    prox = {
                        "http": random.choice(
                            open("./data/proxies.txt", "r").read().splitlines()
                        )
                    }
                else:
                    prox = None

                # Gerando código aleatório
                code = "".join(
                    random.choices(string.ascii_letters + string.digits, k=24 if self.type == "boost" else 16)
                )

                # Verificar se o código foi gerado antes
                if code in generated_codes:
                    continue
                generated_codes.add(code)

                # Validar o código
                req = self.session.get(
                    f"https://discordapp.com/api/entitlements/gift-codes/{code}",
                    proxies=prox,
                    timeout=10,
                ).status_code

                # Se o código for válido
                if req == 200:
                    print(f"Código válido encontrado: discord.gift/{code}")
                    open("./data/valid.txt", "a").write(f"discord.gift/{code}\n")
                    valid_codes += 1
                    self.send_webhook(f"Código válido encontrado: discord.gift/{code}")
                elif req == 429:
                    print(f"Rate limitado ao validar código: discord.gift/{code}")
                    self.send_webhook(f"Rate limitado ao validar código: discord.gift/{code}")
                    sleep(2)

            except Exception as e:
                print(f"Erro: {e}")
                self.send_webhook(f"Erro: {e}")

        print(f"\nVerificação concluída para {self.codes} códigos válidos.")
        self.send_webhook(f"Verificação concluída para {self.codes} códigos válidos.")
        sleep(1.5)
        os.system("cls" if os.name == "nt" else "clear")


# Função que gerencia os diálogos do terminal
def get_user_input(webhook_url):
    # Captura as respostas do usuário e envia para o Discord
    print("Tipo de código (boost, classic): ", end="")
    code_type = input()
    send_webhook(webhook_url, f"Tipo de código escolhido: {code_type}")

    print("Usar proxies (True, False): ", end="")
    prox = input()
    send_webhook(webhook_url, f"Usar proxies: {prox}")

    if prox == "True":
        print("Coletar proxies automaticamente (True, False): ", end="")
        scrape_proxy = input()
        send_webhook(webhook_url, f"Coletar proxies automaticamente: {scrape_proxy}")
    else:
        scrape_proxy = False
        send_webhook(webhook_url, "Não coletar proxies automaticamente.")

    print("Número de códigos válidos desejados: ", end="")
    codes = input()
    send_webhook(webhook_url, f"Número de códigos válidos desejados: {codes}")

    return code_type, prox, scrape_proxy, codes


if __name__ == "__main__":
    # A URL do webhook já foi configurada diretamente no código
    webhook_url = "https://discord.com/api/webhooks/1346085542026149949/xdN-GdWGAtUOgUXIWeLnRyl4FVpz3OMhxV0V1bM3ujIXVZb_tedcPlj-4HDCgvwHVHxg"

    # Loop principal que continua perguntando ao usuário
    while True:
        # Obtém as respostas do usuário e envia para o Discord
        code_type, prox, scrape_proxy, codes = get_user_input(webhook_url)

        # Passando a URL do webhook para a classe SapphireGen
        SapphireGen(code_type, prox, codes, webhook_url).generate(scrape=scrape_proxy)
