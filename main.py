import sys
import time
from time import localtime, strftime, sleep
from colorama import Fore, init
import requests
import random
import string
import os

init(autoreset=True)

class SapphireGen:
    def __init__(self, code_type: str, prox=None, codes=None):
        self.type = code_type
        self.codes = int(codes)
        self.proxies = prox
        self.session = requests.Session()
        self.prox_api = "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"
        self.valid_codes = []
        self.generated_codes = set()

    def fetch_proxies(self):
        try:
            response = self.session.get(self.prox_api, timeout=10).text
            if response:
                with open("./data/proxies.txt", "w") as file:
                    file.write(response.strip())
        except Exception as e:
            print(f"{Fore.RED}Erro ao buscar proxies: {e}")

    def get_proxy(self):
        try:
            return {
                "http": random.choice(open("./data/proxies.txt", "r").read().splitlines())
            }
        except:
            return None

    def generate_code(self):
        length = 24 if self.type == "boost" else 16
        return "".join(random.choices(string.ascii_letters + string.digits, k=length))

    def validate_code(self, code, proxy):
        try:
            response = self.session.get(
                f"https://discordapp.com/api/entitlements/gift-codes/{code}",
                proxies=proxy,
                timeout=10,
            )
            return response.status_code
        except:
            return None

    def send_to_webhook(self, webhook_url, message):
        data = {
            "content": message
        }
        try:
            response = requests.post(webhook_url, json=data)
            if response.status_code == 204:
                print(f"{Fore.GREEN}Mensagem enviada ao webhook com sucesso!")
            else:
                print(f"{Fore.RED}Falha ao enviar mensagem ao webhook. Status: {response.status_code}")
        except Exception as e:
            print(f"{Fore.RED}Erro ao enviar para o webhook: {e}")

    def generate(self, scrape=None, webhook_url=None):
        if scrape == "True":
            self.fetch_proxies()

        os.system("clear")
        print(f"{Fore.BLUE}Iniciando geração de códigos...")

        valid_count = 0
        while valid_count < self.codes:
            code = self.generate_code()
            if code in self.generated_codes:
                continue
            self.generated_codes.add(code)

            proxy = self.get_proxy() if self.proxies == "True" else None
            status = self.validate_code(code, proxy)

            if status == 200:
                message = f"Código válido encontrado: discord.gift/{code}"
                print(f"{Fore.GREEN}[{strftime('%H:%M', localtime())}] {message}")
                self.valid_codes.append(code)
                with open("./data/valid.txt", "a") as file:
                    file.write(f"discord.gift/{code}\n")
                
                # Enviar o código válido ao webhook, se fornecido
                if webhook_url:
                    self.send_to_webhook(webhook_url, message)

                valid_count += 1
            elif status == 429:
                print(f"{Fore.YELLOW}[{strftime('%H:%M', localtime())}] Rate limitado. Aguardando...")
                sleep(3)
            else:
                print(f"{Fore.RED}[{strftime('%H:%M', localtime())}] Código inválido: discord.gift/{code}")
        
        print(f"\n{Fore.BLUE}Geração concluída. {valid_count} códigos válidos salvos.")
        sleep(1.5)
        os.system("clear")

if __name__ == "__main__":
    while True:
        code_type = input(f"{Fore.BLUE}Tipo de código (boost, classic): ")
        prox = input(f"{Fore.BLUE}Usar proxies (True, False): ")
        scrape_proxy = input(f"{Fore.BLUE}Coletar proxies automaticamente (True, False): ") if prox == "True" else "False"
        codes = input(f"{Fore.BLUE}Número de códigos válidos desejados: ")
        webhook_url = input(f"{Fore.BLUE}URL do webhook (pressione Enter para não usar): ")

        # Se o usuário fornecer um URL do webhook, envie os dados para lá
        if webhook_url.strip():
            SapphireGen(code_type, prox, codes).generate(scrape=scrape_proxy, webhook_url=webhook_url)
        else:
            SapphireGen(code_type, prox, codes).generate(scrape=scrape_proxy)
