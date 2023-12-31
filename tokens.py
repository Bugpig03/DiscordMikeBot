# -*- coding: utf-8 -*-
#-------- IMPORTED MODULES --------
from init import *
import json

#-------- READ TOKENS FROM JSON FILE DO NOT USE IF YOU DONT HAVE JSON FILE FOR YOUR TOKEN --------
with open(SECRET_JSON_DIR, 'r') as fichier:
    contenu_json = json.load(fichier)
tokens = contenu_json.get("tokens", {})

#-------- TOKENS AND KEYS --------
blagues = BlaguesAPI(tokens.get("tokenJoke"))
botToken = tokens.get("tokenDiscordBot")
openai.api_key = tokens.get("tokenOpenAI")