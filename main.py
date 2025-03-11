import uuid
import requests
from datetime import datetime, timedelta
import time

# Configurações
WEBHOOK_URL = "https://discord.com/api/webhooks/1349146856722006017/impqKgyW1lZWuSMlmKLvOSLkzUKHlpMHTut3wVMLbk3R4N-Gr9l_He9XmNmydmp11P36"
BASE_URL = "https://discord.com/billing/partner-promotions"
USER_ID = "1310745070936391821"
EXPIRATION_MINUTES = 10  # Tempo de expiração do link
LOOP_DELAY = 5  # Intervalo entre envios (em segundos)

def generate_unique_link(base_url, user_id, expiration_minutes):
    """
    Gera um link único com um token e um tempo de expiração.
    """
    try:
        # Gera um token único
        token = str(uuid.uuid4())
        
        # Calcula o tempo de expiração
        expiration_time = datetime.utcnow() + timedelta(minutes=expiration_minutes)
        
        # Cria o link completo
        link = f"{base_url}/{user_id}/{token}?expires={int(expiration_time.timestamp())}"
        return link
    except Exception as e:
        print(f"Erro ao gerar o link: {e}")
        return None

def send_to_webhook(webhook_url, message):
    """
    Envia uma mensagem para um webhook do Discord.
    """
    try:
        payload = {"content": message}
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()  # Verifica se houve erro na requisição
        print(f"Mensagem enviada com sucesso: {message}")
    except Exception as e:
        print(f"Erro ao enviar mensagem para o webhook: {e}")

def main():
    """
    Gera links e envia para o webhook em loop.
    """
    while True:
        try:
            # Gera o link
            generated_link = generate_unique_link(BASE_URL, USER_ID, EXPIRATION_MINUTES)
            if generated_link:
                print(f"Link gerado: {generated_link}")
                
                # Envia o link para o webhook
                send_to_webhook(WEBHOOK_URL, generated_link)
            else:
                print("Falha ao gerar o link.")
            
            # Aguarda antes de gerar o próximo link
            time.sleep(LOOP_DELAY)
        except KeyboardInterrupt:
            print("Loop interrompido pelo usuário.")
            break
        except Exception as e:
            print(f"Erro no loop principal: {e}")
            break

# Executa o script
if __name__ == "__main__":
    main()
