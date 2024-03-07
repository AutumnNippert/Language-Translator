# bot.py
import os
from ai_interaction import query

from dotenv import load_dotenv
from langdetect import detect, detect_langs
import discord

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    
    game = discord.Game("with Translating Languages!")
    await client.change_presence(activity=game)

@client.event
async def on_message(message):
    # if not a message
    if message.type != discord.MessageType.default and message.type != discord.MessageType.reply:
        return
    
    # if message is from bot
    if message.author == client.user:
        return
    
    # if message has attachments, die
    if len(message.attachments) > 0:
        return

    lang = detect(message.content)

    if lang == 'en':
        return
    
    # if content has a non latin character or number, and is super short, die
    if message.content.isalnum() and len(message.content.split(" ")) < 2:
        return
    
    print(detect_langs(message.content))
    
    print(f"Message from {message.author}: {message.content} ({lang})")

    async with message.channel.typing():
        # Generate Response
        print('generating response...')
        response = query(f"Respond with only the translation of this message from {lang} to english: {message.content}")
        print('response generated')
        if response == '':
            response = "shitted"

        await message.channel.send(f"Lang: {lang}\n{response}")
    
client.run(TOKEN)