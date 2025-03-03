import sys
import time
from time import localtime, strftime, sleep
from colorama import Fore, init
import requests
import random
import string
import os

init(autoreset=True)

WEBHOOK_URL = "https://discord.com/api/webhooks/1346081852397584516/m6tQM2odk-U7yu_54QAUgkCWQxQuotKHKh9KpiFAg0Bhp7GAWm64dX3I1CnnVKa_4kf2"  # Insira a URL do webhook aqui

class SapphireGen:
    def __init__(self, code_type: str, prox=None, codes=None):
        self.type = code_type
        self.codes = int(codes)
        self.proxies = prox
        self.session = requests.Session()
        self.prox_api = "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"
        self.valid_codes = []
        self.generated_codes = set()
        self.proxy_list = []
        if self.proxies == "True":
            self.load_proxies()

    def load_proxies(self):
        try:
            response = self.session.get(self.prox_api, timeout=10).text
            if response:
                self.proxy_list = response.strip().split("\n")
                print(f"{Fore.CYAN}Proxies carregados: {len(self.proxy_list)}")
        except Exception as e:
            print(f"{Fore.RED}Erro ao buscar proxies: {e}")

    def get_proxy(self):
        if self.proxy_list:
            return {"http": f"http://{random.choice(self.proxy_list)}"}
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
            if response.status_code == 200:
                return "valid"
            elif response.status_code == 404:
                return "invalid"
            elif response.status_code == 403:
                return "used"
            elif response.status_code == 429:
                return "rate_limited"
            else:
                return "unknown"
        except:
            return "error"

    def send_to_webhook(self, code):
        data = {
            "content": f"Código válido encontrado: discord.gift/{code}"
        }
        try:
            requests.post(WEBHOOK_URL, json=data)
        except Exception as e:
            print(f"{Fore.RED}Erro ao enviar para webhook: {e}")

    def generate(self, scrape=None):
        if scrape == "True":
            self.load_proxies()
        
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

            if status == "valid":
                print(f"{Fore.GREEN}[{strftime('%H:%M', localtime())}] Código válido encontrado: discord.gift/{code}")
                self.valid_codes.append(code)
                with open("./data/valid.txt", "a") as file:
                    file.write(f"discord.gift/{code}\n")
                self.send_to_webhook(code)
                valid_count += 1
            elif status == "used":
                print(f"{Fore.YELLOW}[{strftime('%H:%M', localtime())}] Código já foi usado: discord.gift/{code}")
            elif status == "rate_limited":
                print(f"{Fore.YELLOW}[{strftime('%H:%M', localtime())}] Rate limitado. Aguardando 10 segundos...")
                sleep(10)
            else:
                print(f"{Fore.RED}[{strftime('%H:%M', localtime())}] Código inválido: discord.gift/{code}")
            
            sleep(random.uniform(1, 3))  # Aguarda tempo aleatório entre requisições
            
        print(f"\n{Fore.BLUE}Geração concluída. {valid_count} códigos válidos salvos.")
        sleep(1.5)
        os.system("clear")

if __name__ == "__main__":
    while True:
        code_type = input(f"{Fore.BLUE}Tipo de código (boost, classic): ")
        prox = input(f"{Fore.BLUE}Usar proxies (True, False): ")
        scrape_proxy = input(f"{Fore.BLUE}Coletar proxies automaticamente (True, False): ") if prox == "True" else "False"
        codes = input(f"{Fore.BLUE}Número de códigos válidos desejados: ")
        SapphireGen(code_type, prox, codes).generate(scrape=scrape_proxy)
