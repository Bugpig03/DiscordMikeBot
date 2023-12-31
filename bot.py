﻿#-------- IMPORTED MODULES --------
import init
from init import *

import functions
from functions import *

import tokens
from tokens import *

import profiles
from profiles import *

import server_web
from server_web import *

import music
from music import *

#-------- BOT COMMANDS --------
@bot.command()
async def aide(ctx):
    await ctx.send("**Listes des commandes dispo (prefix *) :- **play [youtube url]** (Jouer un son depuis une vidéo youtube)\n- **next** (passe la musique)\n- **queue** (permet de voir la playlist) \n- **clear** (éfface la playlist) \n- **remove [music index]** (Enlève une musique de la playlist)\n- **profile [@user tag]** (permet de voir le profil d'une personne) \n- **meteo [ville]** (permet de voir la méteo dans ta ville bg)\n- **blague** (petite blague 'souvent rasiste')\n- **astro [votre signe]** (super signe astrologique...)\n- **mike [question pour mike]** (marche plus déso je suis pas assez riche btw)")

@bot.command()
async def tell(ctx, *, message):
    await ctx.message.delete()
    await ctx.send(message)
    
@bot.command()
async def mike(ctx):
    await ctx.send("Je suis désolé, mon ami, mais je n'ai plus cette capacité exubérante, c'est du passé, mec.")
    
@bot.command()
async def profile(ctx, user: discord.Member = None):
    await display_profile(ctx, user.id if user else ctx.author.id)
    
#-------- MUSIC COMMANDS --------

@bot.command()
async def play(ctx, url):
    await ctx.message.delete()
    await add_music_to_queue(ctx, url)
@play.error
async def play_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Tu dois mettre un url bg !")
        
@bot.command()
async def stop(ctx):
    await stop_music()
    
@bot.command()
async def next(ctx):
    await next_music()

@bot.command()
async def queue(ctx):
    if len(init.currentMusicQueue) > 0:
        await ctx.send(f"Queue: {len(init.currentMusicQueue)}")
    else:
        await ctx.send("La file d'attente est vide.")

@bot.command()
async def remove(ctx, index: int):
    index = index - 1
    if 0 <= index < len(queueMusic):
        queueMusic.pop(index)
        await ctx.send(f"La musique **{index}** a été enlevé à la file d'attente.")
    else:
        await ctx.send("Gros golmon.")
        
#-------- API COMMANDS --------

@bot.command()
async def blague(ctx):
    find_joke = False
    while find_joke == False :
        blague = await blagues.random()
        blague = str(blague)

        #trie reponses API
        joke_match = re.search(r"joke='([^']+)'", blague)
        # Utiliser une expression régulière pour capturer le texte entre les guillemets simples ou doubles après "joke="
        joke_match = re.search(r"joke='([^']+)'", blague)
        if joke_match:
            joke_value = joke_match.group(1)
        else:
            joke_value = "none"
            find_joke = False

        # Utiliser une expression régulière pour capturer le texte entre les guillemets simples ou doubles après "answer="
        answer_match = re.search(r"answer='([^']+)'", blague)
        if answer_match:
            answer_value = answer_match.group(1)
        else:
            answer_value = "none"
            find_joke = False

        if joke_value != "none" and answer_value != "none" :
            find_joke = True
            asyncio.sleep(0.5)

    print("joke:", joke_value)
    print("answer:", answer_value)
    await ctx.send(f"{joke_value} ||{answer_value}||")

@bot.command()
async def meteo(ctx, *, message):
    weather_info = functions.get_weather("8d1ab8eae7831e235463e85d63664aa7", message)
    temp_kph = round(int(weather_info['wind_speed'])*3,6)
    await ctx.send(f"**La méteo à {weather_info['city']} :**\n- Température : {weather_info['temperature']}°C\n- Description : {weather_info['description']}\n- Humidité : {weather_info['humidity']}%\n- Vitesse du vent : {temp_kph} km/h")

@bot.command()
async def astro(ctx, *, message):
    astro_info = functions.get_astro(message.lower())
    asyncio.sleep(1)
    await ctx.send(f"**Voici l'horoscope du jour pour les {message.lower()} :** {astro_info}") 
@astro.error
async def astro_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Idiot ! Tu dois spécifier un signe astrologique dans la commande !")
 
#-------- BOT EVENTS --------
@bot.event
async def on_ready():
    print(f"Connected as {bot.user.name}")
    await asyncio.sleep(1)
    while True:
        await check_if_music_in_queue()
        if functions.time_until_message() == 0:
            await asyncio.sleep(functions.time_until_message())
            await functions.send_message_matin()
        await asyncio.sleep(1)

@bot.event
async def on_message(message):
    if message.author == bot.user: # check if message was sent by the bot
        return
    #function.add_score(message.author)
    await add_score(message.author.id)

    #reponse directe 
    if 'quoi' in message.content:
        if random.randint(1,9) == 3:
            await message.channel.send('FEUR !')

    if 'oui' in message.content:
        if random.randint(1,9) == 3:
            await message.channel.send('stiti !')

    if ':d' in message.content:
        await message.channel.send('gros baveux')

    if 'CIAO' in message.content:
        if message.author.id == 301727996392505346: # id bugpig
            await message.channel.send('BELLIIIISIIIIMAAAA Y BELLIIISIIIMOOO !!!! ')      
      
    # RATIO SYSTEM      
    if message.author.id != 430067459131834368: #id mike brant
        if random.randint(1,200) == 4:
            await add_ratio_r(message.author.id)
            await message.channel.send("**[R]** menfou mec raconte pas ta vie **(1/200)**")
            print("triggered 1/200")

    if message.author.id != 430067459131834368: #id mike brant
        if random.randint(1,1500) == 500:
            await add_ratio_sr(message.author.id)
            await message.channel.send("**[SR]** menfou mec raconte pas ta vie de type SUPER RARE **(1/1500)**")
            print("menfou triggered 1/1500")

    if message.author.id != 430067459131834368: #id mike brant
        if random.randint(1,10000) == 1000:
            await add_ratio_lr(message.author.id)
            await message.channel.send("**[LR]** menfou mec raconte pas ta vie de type LEGENDARY RARE **(1/10000)**")
            print("menfou triggered 1/10000")

    await bot.process_commands(message)
    
def run_discord_bot():
    bot.run(botToken)