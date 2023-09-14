# -*- coding: utf-8 -*-
import subprocess

# Lancer le bot Discord dans un processus séparé
bot_process = subprocess.Popen(['python', 'bot.py'])

# Lancer le serveur web Flask dans un processus séparé
server_process = subprocess.Popen(['python', 'server_web.py'])

# Attendre que les deux processus se terminent (vous pouvez ajuster cela selon vos besoins)
bot_process.wait()
server_process.wait()