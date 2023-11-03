# -*- coding: utf-8 -*-
#-------- IMPORTED MODULES --------
import calendar
from mimetypes import init
from init import *
from tokens import *
from init import currentMusic

#-------- FUNCTIONS --------
async def connect_bot_to_channel(ctx):
    voice_client = get(bot.voice_clients, guild=ctx.guild)
    if not voice_client:
        channel = ctx.author.voice.channel
        if not channel:
             await ctx.send(f"Rejoint d'abord un salon vocal !")
        else:
            voice_client = await channel.connect()
 
async def add_music_to_queue(ctx, url):
    voice_client = await get_voice_client(bot)
    text_channel = bot.get_channel(mainTextChannel)
    
    if not is_valid_youtube_url(url):
        print("c'est pas un URL")
        url = search_youtube_video_url(url)
        if url is None:
            print("Aucun URL a été trouvé FIN")
            return
    yt = YouTube(url)
    if yt.length > 360:
        print("Musique trop longue plus de 6 min")
        return
    new_music = {
    "url" : str(url),
    "title" : str(yt.title),
    "length" : str(yt.length)
    }
    
    currentMusicQueue.append(new_music)
        
async def play_music():
    global currentMusic
    voice_client = await get_voice_client(bot)
    if not currentMusicQueue:
        return
    if voice_client.is_playing():
        return
    print("function play music : START")
    newMusic = currentMusicQueue.pop(0)

    currentMusic = {
        "title" : newMusic["title"],
        "length" : newMusic["length"]
    }
    currentMusic = "OKAY"
    yt = YouTube(newMusic["url"])
    if yt is None:
        return
    stream = yt.streams.filter(only_audio=True).first()
    # Téléchargez la piste audio
    stream.download(output_path=MUSIC_DIR_YT)
    nom_fichier_mp3 = "music" + str(random.randint(0,9999999999)) + ".mp3"
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

    voice_client.play(source)
    print("function play music : END") 
       
async def check_if_music_in_queue():
    if bot is None: #wait until bot is set
        return
    
    voice_client = await get_voice_client(bot)
     
    if currentMusicQueue is not None:
        if voice_client is None:
            voice_channel = bot.get_channel(mainVoiceChannel)
            voice_client = await voice_channel.connect()
        if voice_client.is_playing():
            return
        else:
            await play_music()
            
def is_valid_youtube_url(url):
    # Vérifier si l'URL commence par "https://www.youtube.com/"
    if not url.startswith("https://www.youtube.com/"):
        return False

    # Vérifier si l'URL est accessible en utilisant une requête HTTP
    response = requests.head(url)
    return response.status_code == 200
            
async def stop_music():
    voice_client = await get_voice_client(bot)
    if voice_client and voice_client.is_playing():
        # Arrêtez la diffusion audio
        init.currentMusicQueue = []
        voice_client.stop()
        
async def next_music():
    voice_client = await get_voice_client(bot)
    if voice_client and voice_client.is_playing():
        # Arrêtez la diffusion audio
        voice_client.stop()
 
async def get_voice_client(bot):
    for vc in bot.voice_clients:
        return vc  # Récupère le premier client vocal trouvé
    return None  # Aucun client vocal trouvé

def is_valid_youtube_url(url):
    # Analyser l'URL pour extraire l'identifiant vidéo
    video_id = None
    if "youtube.com" in url:
        video_id = url.split("v=")[1]
    elif "youtu.be" in url:
        video_id = url.split("/")[-1]

    if video_id:
        # Rechercher la vidéo en utilisant l'identifiant vidéo
        videos_search = VideosSearch(video_id, limit=1)
        results = videos_search.result()
        
        # Vérifier si la vidéo existe
        if len(results['result']) > 0:
            return True

    return False

def search_youtube_video_url(keywords):
    # Créer une instance de VideosSearch
    videos_search = VideosSearch(" ".join(keywords), limit = 1)
    
    # Obtenir les résultats de recherche
    results = videos_search.result()
    
    # Vérifier si des vidéos ont été trouvées
    if len(results['result']) > 0:
        # Obtenir l'URL de la première vidéo trouvée
        video_url = results['result'][0]['link']
        return video_url
    else:
        return None