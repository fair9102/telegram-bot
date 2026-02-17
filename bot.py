import os
import time
import requests
from telegram import Bot

# ----------------------------
# Configurações
# ----------------------------
TOKEN = os.environ.get("TOKEN")       # Token do BotFather
CHAT_ID = os.environ.get("CHAT_ID")   # ID do canal (ex: -1003836443380)
API_KEY = os.environ.get("API_KEY")   # API Key TheSportsDB

bot = Bot(token=TOKEN)

# ----------------------------
# Jogos que queres monitorar
# Preenche com os nomes exatos do TheSportsDB
# ----------------------------
jogos_monitorados = [
    {"home": "Arsenal", "away": "Wolverhampton Wanderers"},
    {"home": "Chelsea", "away": "Liverpool"}
]

# ----------------------------
# Armazena últimos status para não repetir mensagens
# ----------------------------
ultimo_estado = {}

# ----------------------------
# Função para buscar jogos ao vivo
# ----------------------------
def buscar_jogos_ao_vivo():
    url = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}/livescore.php?s=Soccer"
    response = requests.get(url)
    data = response.json()
    
    if not data.get("events"):
        return []

    # Filtra apenas os jogos que monitoramos
    jogos_filtrados = []
    for jogo in data["events"]:
        for monitor in jogos_monitorados:
            if (jogo.get("strHomeTeam") == monitor["home"] and
                jogo.get("strAwayTeam") == monitor["away"]):
                jogos_filtrados.append(jogo)
    return jogos_filtrados

# ----------------------------
# Função para enviar mensagem
# ----------------------------
def enviar_mensagem(jogo):
    home = jogo.get("strHomeTeam")
    away = jogo.get("strAwayTeam")
    score = f"{jogo.get('intHomeScore','0')} - {jogo.get('intAwayScore','0')}"
    status = jogo.get("strStatus") or "Atualização"
    
    mensagem = f"⚽ {home} {score} {away}\nStatus: {status}"
    bot.send_message(chat_id=CHAT_ID, text=mensagem)

# ----------------------------
# Loop principal
# ----------------------------
while True:
    jogos = buscar_jogos_ao_vivo()
    for jogo in jogos:
        jogo_id = jogo["idEvent"]
        # Só envia mensagem se houve mudança
        if ultimo_estado.get(jogo_id) != jogo.get("strStatus"):
            enviar_mensagem(jogo)
            ultimo_estado[jogo_id] = jogo.get("strStatus")
    time.sleep(300)  # Atualiza a cada 5 minutos
