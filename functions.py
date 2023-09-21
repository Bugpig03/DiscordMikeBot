# -*- coding: utf-8 -*-
#-------- IMPORTED MODULES --------
from init import *
from tokens import *

#-------- FUNCTIONS --------

def load_scores(): # Read score file at lauch of the bot
    global scores
    try:
        with open(os.path.join(os.path.dirname(__file__), 'scores.txt'), 'r') as f:
            for line in f:
                user_id, score = line.strip().split(':')
                scores[int(user_id)] = int(score)
    except FileNotFoundError:
        # Si le fichier scores.txt n'existe pas, on crée un nouveau dictionnaire vide
        scores = {}

def add_score(user): # Permet d'ajouter un score à l'utilisateur référencé
    if user.id not in scores:
        scores[user.id] = 0
    scores[user.id] += 1
    with open(os.path.join(os.path.dirname(__file__), 'scores.txt'), 'w') as f:
        for user_id, score in scores.items():
            f.write(f'{user_id}:{score}\n')

def liste_fichiers_mp3(): # Permet de faire lire a Mike bot les fichiers MP3 situé dans le dossier MUSIC
    # Récupérer le chemin absolu du dossier "music" par rapport à l'emplacement du code
    dossier_music = MUSIC_DIR

    # Vérifier si le dossier "music" existe
    if not os.path.exists(dossier_music) or not os.path.isdir(dossier_music):
        return "Le dossier 'music' n'existe pas à cet emplacement."

    # Filtrer les fichiers MP3 dans le dossier et les ajouter à une liste
    fichiers_mp3 = [fichier for fichier in os.listdir(dossier_music) if fichier.lower().endswith(".mp3")]

    if not fichiers_mp3:
        return "Je n'ai malheuresement aucun fichier mp3 :('."
    else:
        texte_liste = "**Liste des fichiers MP3 dispo:**\n"
        for fichier_mp3 in fichiers_mp3:
            texte_liste += f"- {fichier_mp3}\n"
        return texte_liste

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

async def play_sound(ctx, file):
    print("plop from functions")
    if ctx == 0:
        ctx = bot.get_channel(893622097195204608)
    file_path = os.path.join(MUSIC_DIR, f'{file}.mp3')
    source = discord.FFmpegPCMAudio(file_path)
    ctx.voice_client.play(source)  # Use an 'after' callback to play the next sound

async def play_youtube_music(ctx, url_or_title):
    print("function play youtube music start")
    
    if ctx is None:
        channel_id = 426760269205602304  # L'ID du salon vocal par défaut si le contexte est None
        channel = bot.get_channel(channel_id)
        if channel:
            await channel.connect()
            ctx = channel

    yt = YouTube(url_or_title)
    stream = yt.streams.filter(only_audio=True).first()

    # Téléchargez la piste audio
    stream.download(output_path=MUSIC_DIR_YT)

    nom_fichier_mp3 = "temp_music" + ".mp3"
    chemin_fichier_mp3 = os.path.join(MUSIC_DIR_YT, nom_fichier_mp3)

    # Supprimez le fichier MP3 existant s'il existe déjà
    if os.path.exists(chemin_fichier_mp3):
        os.remove(chemin_fichier_mp3)

    os.rename(os.path.join(MUSIC_DIR_YT, stream.default_filename), chemin_fichier_mp3)

    # Chargez le fichier audio avec pydub
    audio = AudioSegment.from_file(chemin_fichier_mp3)
    # Normalisez le volume audio (ajuste le volume pour atteindre le niveau cible de -16 dB)
    audio = audio.normalize()
    # Exportez le fichier audio normalisé
    audio.export(chemin_fichier_mp3, format="mp3")

    source = discord.FFmpegPCMAudio(chemin_fichier_mp3)

    ctx.voice_client.play(source, after=lambda e: music_next(ctx))
    print("function play youtube music end")

async def music_next(ctx):
    print("function music_next start")
    ctx = await bot.get_context(ctx.message)
    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()
    if queueMusic:
        nextMusic = queueMusic.pop(0)
        bot.loop.create_task(play_youtube_music(ctx, nextMusic))
        print("function music_next if")
    else:
        bot.loop.create_task(ctx.voice_client.disconnect())
        print("function music_next else")
        