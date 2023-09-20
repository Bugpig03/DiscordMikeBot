import threading
import asyncio
from bot import run_discord_bot
from server_web import run_web_server
from init import app

if __name__ == "__main__":

    flask_thread_bot = threading.Thread(target= run_discord_bot)
    flask_thread_bot.start()
   
app.run(host="0.0.0.0", port=5000)