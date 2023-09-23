# -*- coding: utf-8 -*-
#-------- IMPORTED MODULES --------
from init import *
from tokens import *

#-------- FUNCTIONS --------
def get_weather(api_key, city_name): # Permet d'avoir la méteo d'une ville via l'API open weather map
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city_name, "appid": api_key, "units": "metric"}
    
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        
        if data["cod"] == 200:
            weather_info = {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"],
            }
            return weather_info
        else:
            print("Erreur : Impossible de récupérer les informations météorologiques.")
    except requests.exceptions.RequestException as e:
        print(f"Erreur de connexion : {e}")
    except KeyError:
        print("Erreur : Données météorologiques manquantes dans la réponse.")

def get_astro(signe): # Permet d'avoir l'astrologie quotidienne via l'api de kayoo123
    base_url = "https://kayoo123.github.io/astroo-api/jour.json"
    try:
        response = requests.get(base_url)
        data = response.json()

        target_data = data[signe]
        return target_data
        
    except requests.exceptions.RequestException as e:
        print(f"Erreur de connexion : {e}")
    except KeyError:
        print("Erreur : Données manquantes dans la réponse.")

def gpt_ask(gpt_prompt, engine = "text-davinci-003",max_tokens=150, temperature= 0.5):

    response = openai.Completion.create(
        engine=engine,
        prompt=gpt_prompt, # temperature is the randomness where 1 is the most random
        temperature=temperature, # maximum numbers of tokens to generate a prompt for
        max_tokens=max_tokens, # a token is approximately 4 characters of text
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    
    return response['choices'][0]['text']

def get_anecdote():
    response = gpt_ask("Donne une anecdote réel dans le domaine du jeux-vidéo ou de la pop culture")
    currentAnecdote = response
    return response

#MESSAGE AUTOMATIQUE
async def send_message_matin():
    channel = bot.get_channel(479958977472364555) #ID TRESORIE
    response = get_anecdote()
    await channel.send(response)
    print("Info : Anecdote envoyé !")
    
def time_until_message():
    now = datetime.now().time()
    message_datetime = datetime.combine(datetime.today(), MESSAGE_TIME)
    if now > MESSAGE_TIME:
        message_datetime += timedelta(days=1)
    return (message_datetime - datetime.now()).seconds

        