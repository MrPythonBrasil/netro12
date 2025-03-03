import sys
import time
from time import localtime, strftime, sleep
from colorama import Fore
import requests
import random
import string
import os

class SapphireGen:
    def __init__(this, code_type: str, prox=None, codes=None):
        this.type = code_type
        this.codes = int(codes)
        this.proxies = prox
        this.session = requests.Session()
        this.prox_api = (
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"
        )

    def __proxies__(this):
        req = this.session.get(this.prox_api).text
        if req:
            open("./data/proxies.txt", "w").write(req.strip())

    def generate(this, scrape=None):
        if scrape == "True":
            this.__proxies__()
        
        os.system("clear")
        print(f"{Fore.BLUE}Iniciando geração de códigos...")
        
        valid_codes = 0
        generated_codes = set()
        while valid_codes < this.codes:
            try:
                if this.proxies == "True":
                    prox = {
                        "http": random.choice(
                            open("./data/proxies.txt", "r").read().splitlines()
                        )
                    }
                else:
                    prox = None

                code = "".join(
                    random.choices(string.ascii_letters + string.digits, k=24 if this.type == "boost" else 16)
                )
                
                if code in generated_codes:
                    continue
                generated_codes.add(code)
                
                req = this.session.get(
                    f"https://discordapp.com/api/entitlements/gift-codes/{code}",
                    proxies=prox,
                    timeout=10,
                ).status_code
                
                if req == 200:
                    print(f"{Fore.GREEN}[{strftime('%H:%M', localtime())}] Código válido encontrado: discord.gift/{code}")
                    open("./data/valid.txt", "a").write(f"discord.gift/{code}\n")
                    valid_codes += 1
                elif req == 429:
                    print(f"{Fore.YELLOW}[{strftime('%H:%M', localtime())}] Rate limitado ao validar código: discord.gift/{code}")
                    sleep(2)
            except Exception as e:
                print(f"{Fore.RED}[{strftime('%H:%M', localtime())}] Erro: {e}")
        
        print(f"\n{Fore.BLUE}[{strftime('%H:%M', localtime())}] Verificação concluída para {this.codes} códigos válidos.")
        sleep(1.5)
        os.system("clear")

if __name__ == "__main__":
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
        SapphireGen(code_type, prox, codes).generate(scrape=scrape_proxy)
