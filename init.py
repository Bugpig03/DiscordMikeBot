#-------- LIBRARIES --------
import discord
import random
from discord.ext import commands
from discord.utils import get
import os
import re
import time
from datetime import datetime, time, timedelta
from dotenv import load_dotenv
import asyncio
import ffmpeg
import requests
from blagues_api import BlaguesAPI
import openai
from pytube import YouTube
from pydub import AudioSegment
import json
from flask import Flask, render_template, jsonify
from aiohttp import web
import threading

#-------- MIKE BOT --------
BOT_NAME : "CREATOR"
VERSION : "2.5-1"
CREATOR : "BUGPIG"
#--------------------------

#-------- VARIABLES DECLARATIONS --------
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='*', intents=intents) # instance bot discord
app = web.Application() #instance server flask
scores = {}
listProfiles = {}
newProfile = {}
MESSAGE_TIME = time(10, 30)
queueMusic = []

#-------- PATH CONFIGURATION --------
MUSIC_DIR = 'C:\Projet\Python\music'
MUSIC_DIR_YT = 'C:\Projet\Python\YTmusic'
SECRET_JSON_DIR = "C:\Projet\Python\DiscordMikeBot\secrets.json"
PROFILE_JSON_DIR = "C:\Projet\Python\DiscordMikeBot\profiles.json"


