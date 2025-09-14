import discord
import json
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURACIÓN ---
TOKEN = os.getenv("TOKEN")
CANAL_PERMITIDO_ID_STR = os.getenv("CANAL_PERMITIDO_ID") 
ARCHIVO_DATOS = "finanzas.json"

# --- VALIDACIÓN INICIAL ---
if not TOKEN: 
    print("Error: La variable de entorno TOKEN no está definida en el archivo .env.")
    exit()

if not CANAL_PERMITIDO_ID_STR:
    print("Error: La variable de entorno CANAL_PERMITIDO_ID no está definida en el archivo .env.")
    exit()

# Convertir CANAL_PERMITIDO_ID a entero y manejar errores
try:
    CANAL_PERMITIDO_ID = int(CANAL_PERMITIDO_ID_STR)
except ValueError:
    print(f"Error: El CANAL_PERMITIDO_ID ('{CANAL_PERMITIDO_ID_STR}') no es un número válido.")
    exit()


# --- INTENTOS (PERMISOS) ---
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


# --- EVENTOS DEL BOT ---

@client.event
async def on_ready():
    print(f'¡Hemos iniciado sesión como {client.user}!')
    canal = client.get_channel(CANAL_PERMITIDO_ID)
    print(f'Escuchando únicamente en el canal: #{canal.name}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.channel.id != CANAL_PERMITIDO_ID:
        return


    contenido_mensaje = message.content.lower()

    # ---- LÓGICA DE COMANDOS ----
    if contenido_mensaje == '!hola':
        await message.channel.send('¡Hola! Estoy listo para registrar tus gastos en este canal.')

    if contenido_mensaje.startswith('!gasto'):
        await message.channel.send('Comando de gasto recibido en el canal correcto.')


# --- INICIAR EL BOT ---
try:
    client.run(TOKEN)
except discord.errors.LoginFailure:
    print("Error: El token proporcionado no es válido. Revisa el valor en tu archivo .env.")

