import discord
import json
from datetime import datetime
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURACIÓN ---
TOKEN = os.getenv("TOKEN")
CANAL_PERMITIDO_ID_STR = os.getenv("CANAL_PERMITIDO_ID") 
WIT_AI_TOKEN = os.getenv("WIT_AI_TOKEN")

directorio_script = os.path.dirname(os.path.realpath(__file__))
ARCHIVO_DATOS = os.path.join(directorio_script, "finanzas.json")

# --- VALIDACIÓN INICIAL ---
if not all([TOKEN, CANAL_PERMITIDO_ID_STR, WIT_AI_TOKEN]):
    print("Error: Asegúrate de que TOKEN, CANAL_PERMITIDO_ID y WIT_AI_TOKEN están en tu archivo .env.")
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

# --- MANEJO DE ARCHIVOS (CARGAR Y GUARDAR DATOS) ---

def cargar_datos():
    try:
        with open(ARCHIVO_DATOS, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Si el archivo no existe, crea una estructura base y la devuelve
        return {"saldo": 0.0, "transacciones": []}

def guardar_datos(datos):
    with open(ARCHIVO_DATOS, 'w') as f:
        json.dump(datos, f, indent=4)


# --- FUNCIÓN DE WIT.AI ---
def interpretar_mensaje(mensaje):
    """Envía un mensaje a Wit.ai y devuelve la respuesta parseada."""
    headers = {'Authorization': f'Bearer {WIT_AI_TOKEN}'}
    params = {'q': mensaje}
    response = requests.get('https://api.wit.ai/message', headers=headers, params=params)
    response.raise_for_status() # Lanza un error si la petición falla
    return response.json()


# --- EVENTOS DEL BOT ---

@client.event
async def on_ready():
    print(f'¡Hemos iniciado sesión como {client.user}!')
    try:
        canal = client.get_channel(CANAL_PERMITIDO_ID)
        print(f'Escuchando únicamente en el canal: #{canal.name}')
    except AttributeError:
        print(f'Error: No se pudo encontrar el canal con ID {CANAL_PERMITIDO_ID}.')
        print('Asegúrate de que el ID del canal es correcto y que el bot tiene acceso a él.')


@client.event
async def on_message(message):
    """Se ejecuta cada vez que se envía un mensaje en un canal al que el bot tiene acceso."""
    # Ignorar mensajes del propio bot
    if message.author == client.user:
        return
    # Ignorar mensajes de canales no permitidos
    if message.author == client.user or message.channel.id != CANAL_PERMITIDO_ID:
        return

    contenido_mensaje = message.content.lower()

    # ---- LÓGICA DE COMANDOS ----
    if contenido_mensaje.startswith('!'): # Solo procesa mensajes que son comandos
        # --- COMANDO DE AYUDA ---
        if contenido_mensaje == '!ayuda':
            embed = discord.Embed(
                title="Centro de Ayuda Financiera",
                description="Aquí están todos los comandos que puedes usar:",
                color=discord.Color.blue()
            )
            embed.add_field(name="!gasto <monto> <descripción>", value="Registra un nuevo gasto. Ejemplo: `!gasto 500 Despensa`", inline=False)
            embed.add_field(name="!ingreso <monto> <descripción>", value="Registra un nuevo ingreso. Ejemplo: `!ingreso 15000 Salario`", inline=False)
            embed.add_field(name="!saldo", value="Muestra tu saldo actual.", inline=False)
            embed.add_field(name="!historial", value="Muestra las últimas 10 transacciones.", inline=False)
            await message.channel.send(embed=embed)

        # --- COMANDO DE GASTO ---
        if contenido_mensaje.startswith('!gasto '):
            try:
                # Divide el mensaje en partes: !gasto, monto, descripcion
                partes = message.content.split(' ', 2)
                monto = float(partes[1])
                descripcion = partes[2]

                datos = cargar_datos()
                datos['saldo'] -= monto
                
                # Crea un registro de la transacción
                nueva_transaccion = {
                    "tipo": "gasto",
                    "monto": monto,
                    "descripcion": descripcion,
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                datos['transacciones'].append(nueva_transaccion)
                
                guardar_datos(datos)
                
                embed = discord.Embed(
                    title="✅ Gasto Registrado",
                    description=f"Se registró un gasto de **${monto:,.2f}**.",
                    color=discord.Color.red()
                )
                embed.add_field(name="Concepto", value=descripcion, inline=False)
                embed.add_field(name="Nuevo Saldo", value=f"${datos['saldo']:,.2f}", inline=False)
                await message.channel.send(embed=embed)

            except (IndexError, ValueError):
                await message.channel.send("❌ **Error de formato.** Usa: `!gasto <monto> <descripción>`\nEjemplo: `!gasto 50 café`")

        # --- COMANDO DE INGRESO ---
        if contenido_mensaje.startswith('!ingreso '):
            try:
                partes = message.content.split(' ', 2)
                monto = float(partes[1])
                descripcion = partes[2]

                datos = cargar_datos()
                datos['saldo'] += monto
                
                nueva_transaccion = {
                    "tipo": "ingreso",
                    "monto": monto,
                    "descripcion": descripcion,
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                datos['transacciones'].append(nueva_transaccion)
                
                guardar_datos(datos)

                embed = discord.Embed(
                    title="💰 Ingreso Registrado",
                    description=f"Se registró un ingreso de **${monto:,.2f}**.",
                    color=discord.Color.green()
                )
                embed.add_field(name="Concepto", value=descripcion, inline=False)
                embed.add_field(name="Nuevo Saldo", value=f"${datos['saldo']:,.2f}", inline=False)
                await message.channel.send(embed=embed)

            except (IndexError, ValueError):
                await message.channel.send("❌ **Error de formato.** Usa: `!ingreso <monto> <descripción>`\nEjemplo: `!ingreso 1000 regalo`")

        # --- COMANDO DE SALDO ---
        if contenido_mensaje == '!saldo':
            datos = cargar_datos()
            saldo_actual = datos.get('saldo', 0.0)
            embed = discord.Embed(
                title="Balance General",
                description=f"Tu saldo actual es de:",
                color=discord.Color.gold()
            )
            embed.add_field(name="Saldo", value=f"**${saldo_actual:,.2f}**")
            await message.channel.send(embed=embed)

        # --- COMANDO DE HISTORIAL ---
        if contenido_mensaje == '!historial':
            datos = cargar_datos()
            transacciones = datos.get('transacciones', [])
            
            if not transacciones:
                await message.channel.send("No hay transacciones registradas todavía.")
                return

            embed = discord.Embed(
                title="Últimas 10 Transacciones",
                description="Aquí está tu historial más reciente:",
                color=discord.Color.purple()
            )
            
            # Muestra las últimas 10 transacciones, de la más reciente a la más antigua
            for transaccion in reversed(transacciones[-10:]):
                tipo_emoji = "🔴" if transaccion['tipo'] == 'gasto' else "🟢"
                monto = transaccion['monto']
                descripcion = transaccion['descripcion']
                embed.add_field(
                    name=f"{tipo_emoji} {transaccion['tipo'].capitalize()}: ${monto:,.2f}",
                    value=f"_{descripcion}_",
                    inline=False
                )
            await message.channel.send(embed=embed)
            
    # ---- LÓGICA CONVERSACIONAL (WIT.AI) ----
    else:
        # --- LÓGICA CONVERSACIONAL (NUEVO) ---
        try:
            wit_response = interpretar_mensaje(contenido_mensaje)
            
            # --- CAMBIO 1: Verificación de seguridad para las intenciones ---
            intents_list = wit_response.get('intents', [])
            if not intents_list:
                # Si Wit.ai no encontró ninguna intención, ignorar el mensaje y terminar.
                return
            
            # Ahora es seguro tomar el primer elemento porque sabemos que la lista no está vacía.
            intent = intents_list[0]
            entities = wit_response.get('entities', {})

            if intent.get('confidence', 0) < 0.8:
                # Si la confianza es demasiado baja, también ignoramos.
                return

            intent_name = intent.get('name')

            # --- LÓGICA PARA REGISTRAR GASTO ---
            if intent_name == 'registrar_gasto':
                # --- CAMBIO 2: Verificación de seguridad para las entidades ---
                monto_list = entities.get('wit$amount_of_money:amount_of_money', [])
                desc_list = entities.get('descripcion:descripcion', [])
                
                if monto_list and desc_list:
                    monto = float(monto_list[0]['value'])
                    descripcion = desc_list[0]['body'].capitalize()

                    # (El resto de la lógica de guardar el gasto es igual)
                    datos = cargar_datos()
                    datos['saldo'] -= monto
                    datos['transacciones'].append({
                        "tipo": "gasto", "monto": monto, "descripcion": descripcion,
                        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    guardar_datos(datos)
                    
                    embed = discord.Embed(title="✅ Gasto Registrado (vía IA)", description=f"Entendido. Se registró un gasto de **${monto:,.2f}**.", color=discord.Color.red())
                    embed.add_field(name="Concepto", value=descripcion, inline=False)
                    embed.add_field(name="Nuevo Saldo", value=f"${datos['saldo']:,.2f}", inline=False)
                    await message.channel.send(embed=embed)
                else:
                    await message.channel.send("Entendí que quieres registrar un gasto, pero no pude identificar el monto o la descripción. ¿Puedes ser más específico?")

            # --- LÓGICA PARA REGISTRAR INGRESO ---
            elif intent_name == 'registrar_ingreso':
                monto_list = entities.get('wit$amount_of_money:amount_of_money', [])
                desc_list = entities.get('descripcion:descripcion', [])

                if monto_list and desc_list:
                    monto = float(monto_list[0]['value'])
                    descripcion = desc_list[0]['body'].capitalize()

                    # (El resto de la lógica de guardar el ingreso es igual)
                    datos = cargar_datos()
                    datos['saldo'] += monto
                    datos['transacciones'].append({
                        "tipo": "ingreso", "monto": monto, "descripcion": descripcion,
                        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    guardar_datos(datos)
                    
                    embed = discord.Embed(title="💰 Ingreso Registrado (vía IA)", description=f"¡Perfecto! Se registró un ingreso de **${monto:,.2f}**.", color=discord.Color.green())
                    embed.add_field(name="Concepto", value=descripcion, inline=False)
                    embed.add_field(name="Nuevo Saldo", value=f"${datos['saldo']:,.2f}", inline=False)
                    await message.channel.send(embed=embed)
                else:
                    await message.channel.send("Entendí que quieres añadir un ingreso, pero me faltó el monto o la descripción.")

            # --- LÓGICA PARA CONSULTAR SALDO ---
            elif intent_name == 'consultar_saldo':
                # (Esta parte no necesita cambios porque no extrae de listas)
                datos = cargar_datos()
                saldo_actual = datos.get('saldo', 0.0)
                embed = discord.Embed(title="Balance General", description="Claro, aquí tienes tu saldo actual:", color=discord.Color.gold())
                embed.add_field(name="Saldo", value=f"**${saldo_actual:,.2f}**")
                await message.channel.send(embed=embed)

            # --- LÓGICA PARA VER HISTORIAL ---
            elif intent_name == 'ver_historial':
                # (Esta parte no necesita cambios)
                datos = cargar_datos()
                transacciones = datos.get('transacciones', [])
                
                if not transacciones:
                    await message.channel.send("Aún no tienes transacciones registradas para mostrar.")
                    return

                embed = discord.Embed(title="Últimas 10 Transacciones", description="Con gusto, aquí está tu historial más reciente:", color=discord.Color.purple())
                
                for transaccion in reversed(transacciones[-10:]):
                    tipo_emoji = "🔴" if transaccion['tipo'] == 'gasto' else "🟢"
                    monto = transaccion['monto']
                    descripcion = transaccion['descripcion']
                    embed.add_field(name=f"{tipo_emoji} {transaccion['tipo'].capitalize()}: ${monto:,.2f}", value=f"_{descripcion}_", inline=False)
                await message.channel.send(embed=embed)

        except Exception as e:
            # Mantener el bloque de excepción por si ocurre cualquier otro error inesperado.
            print(f"Ocurrió un error inesperado: {e}")
            await message.channel.send("Lo siento, tuve un problema interno. Inténtalo de nuevo.")


# --- INICIAR EL BOT ---
try:
    client.run(TOKEN)
except discord.errors.LoginFailure:
    print("Error: El token proporcionado no es válido. Revisa el valor en tu archivo .env.")
