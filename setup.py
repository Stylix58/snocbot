import pyTigerGraph as tg
import requests
import json
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

conn = tg.TigerGraphConnection(host=os.getenv("TG_HOST"),
                               username=os.getenv("TG_USERNAME"), version="3.0.6",
                               password=os.getenv("TG_PASSWORD"), useCert=True)
conn.gsql('''
CREATE VERTEX Word(primary_id word STRING) with primary_id_as_attribute="true"
CREATE VERTEX Message(primary_id id INT, message STRING, url STRING)
CREATE UNDIRECTED EDGE WORD_MESSAGE(FROM Message, To Word)
CREATE GRAPH ChatBot(Word, Message, WORD_MESSAGE)
''')
conn.graphname = "ChatBot"
conn.apiToken = conn.getToken(conn.createSecret())
x = requests.get("https://community.tigergraph.com/posts.json")
data = json.loads(x.text)["latest_posts"]
stop_words = set(stopwords.words('english'))
for msg in data:
    raw_msg = "<br>".join(("".join(msg["raw"].split(","))).split("\n"))
    individual_words = raw_msg.split()
    word_tokens = word_tokenize(raw_msg.lower())
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    filtered_sentence = [w for w in filtered_sentence if not w in [
        '.', ',', '!', '?', ':', ';']]
    url = "https://community.tigergraph.com/t/" + \
        msg["topic_slug"] + "/" + str(msg["topic_id"])
    conn.upsertVertex("Message", msg["id"], attributes={
                      "id": msg["id"], "message": msg["raw"], "url": url})
    for word in filtered_sentence:
        conn.upsertVertex("Word", word, attributes={"word": word})
        conn.upsertEdge("Word", word, "WORD_MESSAGE", "Message", msg["id"])
