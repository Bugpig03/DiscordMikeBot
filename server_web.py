from multiprocessing.pool import INIT
import profile
from tkinter import CURRENT
import init
from init import *

from profiles import get_top_10_users_by_score
from music import add_music_to_queue

@app.route('/')
async def index():
    print(f"Nouvel update : {currentAnecdote}")
    return await render_template('index.html', currentAnecdote= init.currentAnecdote)

@app.route('/music')
async def render_music():
    return await render_template('music.html', current_music= init.currentMusic, current_playlist= currentMusicQueue)

@app.route('/score')
async def render_score():
    currentTOP10 = await get_top_10_users_by_score() 
    return await render_template('score.html', top10=currentTOP10)

@app.route('/submit_url_music', methods=['POST'])
async def submit_text():
    form = await request.form # R�cup�re le texte soumis par l'utilisateur
    user_input = form['user_input']
    ctx = None
    #await add_music_to_queue(ctx, user_input)
    asyncio.create_task(add_music_to_queue(None, user_input))
    #new_music = {
    #"url" : str(user_input),
    ##"title" : str("website"),
    ###"length" : str("69")
    #}
    
    #init.currentMusicQueue.append(new_music)
    
    # Faites quelque chose avec user_input, par exemple, imprimez-le
    print(f"Texte soumis par l'utilisateur : {user_input}")
    # Redirigez l'utilisateur vers la page de musique ou effectuez une autre action souhait�e
    return redirect('/music')

def run_web_server():
    app.run(host="0.0.0.0", port=5000)
