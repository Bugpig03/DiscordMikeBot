import profile
from tkinter import CURRENT
import init
from init import *

from profiles import get_top_10_users_by_score

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

def run_web_server():
    app.run(host="0.0.0.0", port=5000)
