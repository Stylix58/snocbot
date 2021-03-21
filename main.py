import discord, random, os

token = os.getenv("DISCORD_BOT_TOKEN")
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    messages = await message.history(limit=200)
    await message.channel.send(random.choice(messages) + random.choice(messages))

client.run(token)