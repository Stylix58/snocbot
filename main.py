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
    if (msg.author.name != "TGbot" and msg.content[-2:] == "??"):

        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize((msg.content[:-2]).lower())
        filtered_sentence = [w for w in word_tokens if not w in stop_words]
        filtered_sentence = list(set([w for w in filtered_sentence if not w in [
            '.', ',', '!', '?', ':', ';']]))

        possible_options = []
        for word in filtered_sentence:
            x = conn.runInstalledQuery("similarArticles", {"word": word})
            for opt in x[0]["blogs"]:
                possible_options.append(opt["attributes"]["url"])
            # print(x[0]["blogs"][0]["attributes"]["message"])

        word_counter = {}
        for word in possible_options:
            if word in word_counter:
                word_counter[word] += 1
            else:
                word_counter[word] = 1
        popular_words = sorted(
            word_counter, key=word_counter.get, reverse=True)

        print(word_counter)
        if len(popular_words) == 0 or word_counter[popular_words[0]] < len(filtered_sentence)/2:
            await msg.channel.send("I couldn't find anything like that.")
        elif len(popular_words) >= 2 and word_counter[popular_words[1]] >= word_counter[popular_words[0]]-2:
            await msg.channel.send("You might want to check out these:\n" + popular_words[0] + "\n" + popular_words[1])
        else:
            await msg.channel.send("You might want to check out this: " + popular_words[0])


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

client.run(token)
