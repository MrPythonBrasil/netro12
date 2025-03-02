import sys
import time
from time import localtime, strftime, sleep
from colorama import Fore
import requests
import random
import string
import os
import itertools
import threading

def animated_text(text, delay=0.05):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def loading_animation():
    for frame in itertools.cycle(['|', '/', '-', '\\']):
        sys.stdout.write(f"\r{Fore.BLUE}[{strftime('%H:%M', localtime())}] Gerando códigos... {frame} ")
        sys.stdout.flush()
        time.sleep(0.1)

def progress_bar(iteration, total, length=30):
    percent = (iteration / total)
    bar = '█' * int(length * percent) + '-' * (length - int(length * percent))
    sys.stdout.write(f"\r{Fore.BLUE}[{strftime('%H:%M', localtime())}] [{bar}] {int(percent * 100)}% ")
    sys.stdout.flush()

class SapphireGen:
    def __init__(this, code_type: str, prox=None, codes=None):
        this.type = code_type
        this.codes = codes
        this.proxies = prox
        this.session = requests.Session()
        this.prox_api = (
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"
        )

    def __proxies__(this):
        req = this.session.get(this.prox_api).text
        if req != None:
            open("./data/proxies.txt", "a+").truncate(0)
            for proxy in req.split("\n"):
                proxy = proxy.strip()
                proxy = f"https://{proxy}"
                open("./data/proxies.txt", "a").write(f"{proxy}\n")

    def generate(this, scrape=None):
        if scrape == "True":
            this.__proxies__()
        
        os.system("clear")
        print(f"{Fore.BLUE}Iniciando geração de códigos...\n")
        loader = threading.Thread(target=loading_animation)
        loader.daemon = True
        loader.start()
        
        for i in range(int(this.codes)):
            try:
                if this.proxies == "True":
                    prox = {
                        "http": random.choice(
                            open("./data/proxies.txt", "r").read().splitlines()
                        )
                    }
                else:
                    prox = None

                if this.type == "boost":
                    code = "".join(
                        [
                            random.choice(string.ascii_letters + string.digits)
                            for _ in range(24)
                        ]
                    )
                else:
                    code = "".join(
                        [
                            random.choice(string.ascii_letters + string.digits)
                            for _ in range(16)
                        ]
                    )
                req = this.session.get(
                    f"https://discordapp.com/api/entitlements/gift-codes/{code}",
                    proxies=prox,
                    timeout=10,
                ).status_code
                if req == 200:
                    animated_text(f"{Fore.GREEN}[{strftime('%H:%M', localtime())}] Código válido encontrado: discord.gift/{code}")
                    open("./data/valid.txt", "a").write(f"{code}\n")
                elif req == 404:
                    animated_text(f"{Fore.RED}[{strftime('%H:%M', localtime())}] Código inválido: discord.gift/{code}")
                elif req == 429:
                    animated_text(f"{Fore.YELLOW}[{strftime('%H:%M', localtime())}] Rate limitado ao validar código: discord.gift/{code}")
                progress_bar(i + 1, int(this.codes))
            except Exception as e:
                animated_text(f"{Fore.RED}[{strftime('%H:%M', localtime())}] Erro: {e}")
        
        print(f"\n{Fore.BLUE}[{strftime('%H:%M', localtime())}] Verificação concluída para {this.codes} códigos.")
        sleep(1.5)
        os.system("clear")

if __name__ == "__main__":
    while True:
        animated_text(f"{Fore.BLUE}[{strftime('%H:%M', localtime())}] Tipo de código (boost, classic): ", 0.02)
        code_type = input()
        animated_text(f"{Fore.BLUE}[{strftime('%H:%M', localtime())}] Usar proxies (True, False): ", 0.02)
        prox = input()
        if prox == "True":
            animated_text(f"{Fore.BLUE}[{strftime('%H:%M', localtime())}] Coletar proxies automaticamente (True, False): ", 0.02)
            scrape_proxy = input()
        else:
            scrape_proxy = False
        animated_text(f"{Fore.BLUE}[{strftime('%H:%M', localtime())}] Número de códigos: ", 0.02)
        codes = input()
        SapphireGen(code_type, prox, codes).generate(scrape=scrape_proxy)
