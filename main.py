import discord
import uuid
import time
from discord.ext import commands

# Configurações do bot
TOKEN = 'MTM0OTE1MTUwNzY2NDIxMjA4MA.Gok6zF.NfXbt30TD_766rYzzOHi0O8oHk322YY16G_aZQ'  # Substitua pelo token do seu bot
PROMO_ID = '1310745070936391821'

# Inicialização do bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=".", intents=intents)

# Função para gerar o link Nitro
def generate_nitro_link():
    # Gerar UUID v4
    unique_id = str(uuid.uuid4())
    
    # Gerar timestamp de expiração (24 horas a partir de agora)
    expiration_time = int(time.time()) + 86400  # 86400 segundos = 24 horas
    
    # Montar o link
    nitro_link = f"https://discord.com/billing/partner-promotions/{PROMO_ID}/{unique_id}?expires={expiration_time}"
    
    return nitro_link

# Comando para gerar o link Nitro
@bot.command(name='gen nitro')
async def gen_nitro(ctx):
    # Gerar o link
    nitro_link = generate_nitro_link()
    
    try:
        # Enviar o link via DM
        await ctx.author.send(f"Aqui está o seu link Nitro: {nitro_link}")
        # Notificar no canal que a mensagem foi enviada
        await ctx.send(f"{ctx.author.mention}, verifique suas mensagens diretas (DMs)!")
    except discord.Forbidden:
        # Se o usuário tiver DMs desativadas
        await ctx.send(f"{ctx.author.mention}, não foi possível enviar a mensagem direta. Verifique se suas DMs estão ativadas!")

# Iniciar o bot
bot.run(TOKEN)
