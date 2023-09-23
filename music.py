# -*- coding: utf-8 -*-
#-------- IMPORTED MODULES --------
from init import *
from tokens import *

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
    voice_client = get(bot.voice_clients, guild=ctx.guild)
    yt = YouTube(url)
    
    new_music = {
    "url" : str(url),
    "title" : str(yt.title),
    "length" : str(yt.length)
    }
    
    currentMusicQueue.append(new_music)
    
    if voice_client.is_playing():
        await ctx.send(f"J'ai ajouté **{yt.title}** à la playlist")
    else:
        await play_music(ctx)
        
async def play_music(ctx):
    voice_client = get(bot.voice_clients, guild=ctx.guild)
    if not currentMusicQueue:
        return
    print("function play music : START")
    newMusic = currentMusicQueue.pop(0)

    currentMusic = {
        "title" : newMusic["title"],
        "length" : newMusic["length"]
    }
    yt = YouTube(newMusic["url"])
    stream = yt.streams.filter(only_audio=True).first()
    # Téléchargez la piste audio
    stream.download(output_path=MUSIC_DIR_YT)
    nom_fichier_mp3 = newMusic['title'] + ".mp3"
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

    ctx.voice_client.play(source,after=lambda e: auto_next_music(ctx) )
    print("function play music : END") 
    
def auto_next_music(ctx):
    if currentMusicQueue:
        asyncio.run(next_music(ctx))
        
async def next_music(ctx):
    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()
    if currentMusicQueue:
        await play_music(ctx)
      
# SOUND SYSTEM
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

async def play_sound(ctx, file):
    print("plop from functions")
    if ctx == 0:
        ctx = bot.get_channel(893622097195204608)
    file_path = os.path.join(MUSIC_DIR, f'{file}.mp3')
    source = discord.FFmpegPCMAudio(file_path)
    ctx.voice_client.play(source)  # Use an 'after' callback to play the next sound