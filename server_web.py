import init
from init import *

async def hello_world(request):
    nbr_queue = len(queueMusic)
    return web.Response(text=f"En ce moment la queue est de {nbr_queue} musique(s)")

app.router.add_get('/', hello_world)

def run_flask_server():
    web.run_app(app, host='0.0.0.0', port=5000)
