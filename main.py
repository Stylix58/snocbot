import discord
import pyTigerGraph as tg
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os

token = os.getenv("DISCORD_BOT_TOKEN")
client = discord.Client()

os.system('python setup.py')

conn = tg.TigerGraphConnection(host=os.getenv("TG_HOST"),
                               username=os.getenv("TG_USERNAME"), version="3.0.6",
                               password=os.getenv("TG_PASSWORD"), useCert=True)
conn.graphname = "ChatBot"
conn.apiToken = conn.getToken(conn.createSecret())


@client.event
async def on_message(msg):
    print(msg.content)


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

client.run(token)
