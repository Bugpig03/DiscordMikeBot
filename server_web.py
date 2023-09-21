import profile
from tkinter import CURRENT
import init
from init import *

from profiles import get_top_10_users_by_score
from functions import play_youtube_music

@app.route('/')
async def index():
    return await render_template('index.html')

@app.route('/music')
async def render_music():
    return await render_template('music.html')

@app.route('/score')
async def render_score():
    currentTOP10 = await get_top_10_users_by_score() 
    return await render_template('score.html', top10=currentTOP10)

@app.route('/submit_url_music', methods=['POST'])
async def submit_text():
    form = await request.form # Récupère le texte soumis par l'utilisateur
    user_input = form['user_input']
    # Faites quelque chose avec user_input, par exemple, imprimez-le
    print(f"Texte soumis par l'utilisateur : {user_input}")
    # Redirigez l'utilisateur vers la page de musique ou effectuez une autre action souhaitée
    return redirect('/music')

def run_web_server():
    app.run(host="0.0.0.0", port=5000)
