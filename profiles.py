# -*- coding: utf-8 -*-
#-------- IMPORTED MODULES --------
from bdb import GENERATOR_AND_COROUTINE_FLAGS
from cgi import print_exception
from re import U
from init import *

# Fonction pour charger les profils depuis un fichier JSON
def get_all_profiles():
    try:
        with open(PROFILE_JSON_DIR, 'r') as data:
            return json.load(data)
    except FileNotFoundError:
        return {}

# Fonction pour sauvegarder les profils dans un fichier JSON

def save_profile(newProfile):
    listProfiles = get_all_profiles()
    # Fusionner les anciens profils avec les nouveaux profils
    listProfiles.update(newProfile)
    # Sauvegarder les profils mis à jour dans le fichier JSON
    with open(PROFILE_JSON_DIR, 'w') as data:
        json.dump(listProfiles, data, indent=4)

def get_user_data(userID):
    data = get_all_profiles()
    if str(userID) in data:
        return data[str(userID)]
    else:
        return None
    
def user_exist(userID):
    data = get_all_profiles()
    if str(userID) in data:
        return True
    else:
        return False
    
async def create_new_user(userID):
    pseudo = await get_pseudo(userID)
    newProfile[str(userID)] = {
        "username" : pseudo,
        "score": 0,
        "nbr_ratio_r": 0,
        "nbr_ratio_sr": 0,
        "nbr_ratio_lr": 0
        }
    save_profile(newProfile)

        
async def display_profile(ctx, userID):
    if user_exist(userID) == True:
        data = get_user_data(userID)
        temp_pseudo = data["username"]
        temp_score = data["score"]  # Obtient le score ou 0 s'il n'existe pas
        temp_ratio_r = data["nbr_ratio_r"]  # Obtient le ratio_r ou 0 s'il n'existe pas
        temp_ratio_sr = data["nbr_ratio_sr"]  # Obtient le ratio_sr ou 0 s'il n'existe pas
        temp_ratio_lr = data["nbr_ratio_lr"]  # Obtient le ratio_lr ou 0 s'il n'existe pas
        await ctx.send(f"**Profil de {temp_pseudo}** :\n- score : {temp_score}\n- ratio RARE : {temp_ratio_r}\n- ratio SUPER RARE : {temp_ratio_sr}\n- ratio LEGENDARY RARE : {temp_ratio_lr}")
    else:
        await ctx.send("L'utilisateur n'existe pas sorry --'")
        
async def get_pseudo(userID):
    try:
        user = await bot.fetch_user(userID)
        if user:
            return user.name
        else:
            return None
    except discord.errors.NotFound:
        return None
    
async def add_score(userID):
    
    if not user_exist(userID): # check if user exist
        await create_new_user(userID)
        
    data = get_all_profiles()
       
    # Modifier le score de l'utilisateur
    data[str(userID)]["score"] = data[str(userID)]["score"] + 1
    
    # MAJ pseudo when talking
    pseudo = str(await get_pseudo(userID))
    data[str(userID)]["username"] = pseudo

    save_profile(data)

    print(f"Score de l'utilisateur {str(userID)} mis a jour avec succes")
        
async def add_ratio_r(userID):
    if not user_exist(userID): # check if user exist
        await create_new_user(userID)

    data = get_all_profiles()

    # Modifier le score de l'utilisateur
    data[str(userID)]["nbr_ratio_r"] = data[str(userID)]["nbr_ratio_r"] + 1

    save_profile(data)

    print(f"Le nombre de ratio R de l'utilisateur {str(userID)} mis a jour avec succes")
      
async def add_ratio_sr(userID):
    if not user_exist(userID): # check if user exist
        await create_new_user(userID)

    data = get_all_profiles()

    # Modifier le score de l'utilisateur
    data[str(userID)]["nbr_ratio_sr"] = data[str(userID)]["nbr_ratio_sr"] + 1

    save_profile(data)

    print(f"Le nombre de ratio SR de l'utilisateur {str(userID)} mis a jour avec succes")
        
async def add_ratio_lr(userID):
    if not user_exist(userID): # check if user exist
        await create_new_user(userID)

    data = get_all_profiles()

    # Modifier le score de l'utilisateur
    data[str(userID)]["nbr_ratio_lr"] = data[str(userID)]["nbr_ratio_lr"] + 1

    save_profile(data)

    print(f"Le nombre de ratio LR de l'utilisateur {str(userID)} mis a jour avec succes")

async def get_top_10_users_by_score():
    data = get_all_profiles()
    # Trier les données en fonction du score, en ordre décroissant
    sorted_data = sorted(data.items(), key=lambda x: x[1]['score'], reverse=True)

    # Sélectionner les 10 premiers éléments avec les noms d'utilisateur et les scores correspondants
    top_10_users = [(user[1]['username'], user[1]['score']) for user in sorted_data[:10]]
    
    return top_10_users


