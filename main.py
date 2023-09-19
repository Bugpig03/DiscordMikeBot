import threading

from bot import run_discord_bot
from server_web import run_flask_server

if __name__ == "__main__":

    flask_thread = threading.Thread(target=run_flask_server)
    flask_thread.start()

    run_discord_bot()