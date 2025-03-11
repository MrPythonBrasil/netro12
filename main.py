import uuid
from datetime import datetime, timedelta

def generate_unique_link(base_url, user_id, expiration_minutes=10):
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

def validate_link(link, user_id):
    """
    Valida se o link é válido e se ainda está dentro do prazo de expiração.
    """
    try:
        # Verifica se o link está no formato correto
        if not link or not isinstance(link, str) or link.count("/") < 3:
            print("Formato do link inválido.")
            return False
        
        # Extrai o token e o tempo de expiração do link
        parts = link.split("/")
        token_and_params = parts[-1]
        
        if "?" not in token_and_params:
            print("Link não contém parâmetros de expiração.")
            return False
        
        token, params = token_and_params.split("?")
        
        if "expires=" not in params:
            print("Parâmetro 'expires' não encontrado.")
            return False
        
        expiration_timestamp = int(params.split("expires=")[1])
        
        # Verifica se o link expirou
        if datetime.utcnow().timestamp() > expiration_timestamp:
            print("Link expirado.")
            return False
        
        # Verifica se o user_id está correto
        if parts[-2] != user_id:
            print("User ID não corresponde.")
            return False
        
        print("Link válido.")
        return True
    except Exception as e:
        print(f"Erro ao validar o link: {e}")
        return False

# Exemplo de uso
if __name__ == "__main__":
    # Configurações
    base_url = "https://discord.com/billing/partner-promotions"
    user_id = "1310745070936391821"
    expiration_minutes = 10  # Tempo de expiração do link

    # Gera o link
    generated_link = generate_unique_link(base_url, user_id, expiration_minutes)
    if generated_link:
        print("Generated Link:", generated_link)
        
        # Valida o link
        is_valid = validate_link(generated_link, user_id)
        print("Link válido?" if is_valid else "Link inválido!")
    else:
        print("Falha ao gerar o link.")
