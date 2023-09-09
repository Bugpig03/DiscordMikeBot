#-------- MIKE BOT --------
VERSION = "2.3.1"
CREATOR = "bugpig"
#--------------------------

#-------- IMPORTED MODULES --------
import mod_init as init
from mod_init import *

import mod_function as function
from mod_init import *

import mod_token as token
from mod_token import *

#-------- BOT COMMANDS --------
@bot.command()
async def aide(ctx):
    await ctx.send("**Listes des commandes dispo :**\n- *join -> (mike bot rejoint le salon) \n- *leave -> (mike bot quitte le salon) \n- *play -> [youtube url] (Jouer un son depuis une vidéo youtube)\n- *next -> (passe la chanson) \n- *sound [your sound] -> (Joue un son rigolo) \n- *soundslist -> (Permet de voir les sons rigolo dispo) \n- *queue -> (permet de voir la playlist) \n- *clear -> (éfface la playlist) \n- *remove [music index] -> (Enlève une musique de la playlist)\n- *score [user tag] -> (permet de voir le score d'une personne) \n- *meteo [ville] -> (permet de voir la méteo dans ta ville bg)\n- *blague -> (petite blague 'souvent rasiste')\n- *astro [votre signe] -> (super signe astrologique...)\n- *mike [question pour mike] -> (marche plus déso je suis pas assez riche btw)")

@bot.command()
async def info(ctx):
    info = f"**Informations sur MIKE BOT**\n- VERSION : {VERSION} \n- MADE BY : {CREATOR}"
    await ctx.send(info)

@bot.command()
async def soundslist(ctx):
    await ctx.send(function.liste_fichiers_mp3())

@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

@bot.command()
async def tell(ctx, *, message):
    await ctx.message.delete()
    await ctx.send(message)

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
    weather_info = function.get_weather("8d1ab8eae7831e235463e85d63664aa7", message)
    temp_kph = round(int(weather_info['wind_speed'])*3,6)
    await ctx.send(f"**La méteo à {weather_info['city']} :**\n- Température : {weather_info['temperature']}°C\n- Description : {weather_info['description']}\n- Humidité : {weather_info['humidity']}%\n- Vitesse du vent : {temp_kph} km/h")

@bot.command()
async def mike(ctx):
    await ctx.send("Je suis désolé, mon ami, mais je n'ai plus cette capacité exubérante, c'est du passé, mec.")

@bot.command()
async def astro(ctx, *, message):
    astro_info = function.get_astro(message.lower())
    asyncio.sleep(1)
    await ctx.send(f"**Voici l'horoscope du jour pour les {message.lower()} :** {astro_info}")

@bot.command()
async def sound(ctx, file):
    voice_client = get(bot.voice_clients, guild=ctx.guild)

    if not voice_client:
        channel = ctx.author.voice.channel
        voice_client = await channel.connect()

    if voice_client.is_playing():
        await ctx.send(f"**Déso mon gars mais je chante déja la.")
    else:
        await function.play_sound(ctx, file)

@bot.command()
async def play(ctx, urlOrTitle):
    voice_client = get(bot.voice_clients, guild=ctx.guild)

    if not voice_client:
        channel = ctx.author.voice.channel
        voice_client = await channel.connect()

    if voice_client.is_playing():
        queueMusic.append(urlOrTitle)
        await ctx.send(f"Votre musique a été ajouté à la file d'attente. [{len(queueMusic)}]")
    else:
        await function.play_youtube_music(ctx, urlOrTitle)

@bot.command()
async def next(ctx):
    await function.music_next(ctx)

@bot.command()
async def clear(ctx):
    queueMusic.clear()
    await ctx.send("La file d'attente a été reset.")

@bot.command()
async def queue(ctx):
    if queueMusic:
        await ctx.send(f"Queue: {len(queueMusic)}")
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

@bot.command()
async def score(ctx, user: discord.Member = None):
    if user is None:
        user = ctx.author
    if user.id not in scores:
        await ctx.send(f'{user.mention} n\'a pas de score pour le moment.')
    else:
        await ctx.send(f'{user.mention} a un score de {scores[user.id]}.')

#-------- BOT EVENTS --------
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    while True:
        if function.time_until_message() == 0:
            await asyncio.sleep(function.time_until_message())
            await function.send_message_matin()

@bot.event
async def on_ready():
    while True:
        if function.time_until_message() == 0:
            await asyncio.sleep(function.time_until_message())
            await function.send_message_matin()
        await asyncio.sleep(1)

@bot.event
async def on_message(message):
    if message.author == bot.user: # check if message was sent by the bot
        return
    function.add_score(message.author)

    global danmachi_trigger
    if 'quoi' in message.content:
        if random.randint(1,3) == 3:
            await message.channel.send('FEUR + RATIO !')

    if 'oui' in message.content:
        if random.randint(1,3) == 3:
            await message.channel.send('stiti !')

    if ':d' in message.content:
        await message.channel.send('gros baveux')

    if 'CIAO' in message.content:
        if message.author.id == 301727996392505346: # id bugpig
            await message.channel.send('BELLIIIISIIIIMAAAA Y BELLIIISIIIMOOO !!!! ')

    if 'danmachi' in message.content:
        if message.author.id == 398141917495558168: #398141917495558168 # id elu
            print("danmachi triggered : ", danmachi_trigger)
            if danmachi_trigger == 0:
                await message.channel.send('oh non il parle de danmachi...')
            if danmachi_trigger == 1:
                await message.channel.send('par pitié elu arrête de parler de danmachi')
            if danmachi_trigger == 2:
                await message.channel.send('TG ELU AVEC TON DANMACHI DE MERDE OMG')
            if danmachi_trigger == 3:
                await message.channel.send('Bon t a gagné petit con je regarderai... un jour')
            if danmachi_trigger == 4:
                await message.channel.send('Oui mec !')
            if danmachi_trigger == 5:
                await message.channel.send('Ouiiii Aiz la plus forte !')
            if danmachi_trigger == 6:
                await message.channel.send('Trop hâte de lire les prochains chapitres la ^^')
            if danmachi_trigger == 7:
                await message.channel.send('oui...')
            danmachi_trigger = danmachi_trigger + 1
            
        
    rnd_trigger = random.randint(1,200)
    if message.author.id != 430067459131834368: #id mike brant
        if rnd_trigger == 4:
            await message.channel.send("[R] menfou mec raconte pas ta vie **(1/200)**")
            print("triggered 1/200")

    rnd_trigger = random.randint(1,1500)
    if message.author.id != 430067459131834368: #id mike brant
        if rnd_trigger == 500:
            await message.channel.send("**[SR] menfou de type ultra rare OMG **(1/1500)**")
            print("menfou triggered 1/1500")

    rnd_trigger = random.randint(1,10000)
    if message.author.id != 430067459131834368: #id mike brant
        if rnd_trigger == 1000:
            await message.channel.send("**[LR]** menfou de type LEGENDAIRE OMG GG BTW (1/10000)**")
            print("menfou triggered 1/10000")

    await bot.process_commands(message)

#-------- BEFORE STARTING BOT DO --------
function.load_scores() # lancement function pour lire de score

bot.run(token.token_mikebot)

