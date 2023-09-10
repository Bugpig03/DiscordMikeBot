#-------- IMPORTED MODULES --------
from bdb import GENERATOR_AND_COROUTINE_FLAGS
from mod_init import *

# Fonction pour charger les profils depuis un fichier JSON
def get_loaded_profiles():
    try:
        with open(PROFILE_JSON_DIR, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Fonction pour sauvegarder les profils dans un fichier JSON
def save_profile(newProfile):
    listProfiles = get_loaded_profiles()
    # Fusionner les anciens profils avec les nouveaux profils
    listProfiles.update(newProfile)
    # Sauvegarder les profils mis à jour dans le fichier JSON
    with open(PROFILE_JSON_DIR, 'w') as file:
        json.dump(listProfiles, file, indent=4)

def user_exist(userID):
    listProfiles = get_loaded_profiles()
    if str(userID) in listProfiles:
        return True
    else:
        return False

def create_new_user(userID):
    newProfile[str(userID)] = {
        "score": 1,
        "nbr_ratio_r": 0,
        "nbr_ratio_sr": 0,
        "nbr_ratio_lr": 0
        }
    save_profile(newProfile)

        
async def display_profile(ctx, userID):
    if user_exist(userID) == True:
        userKey = get_user_infos(userID)
        temp_pseudo = await get_pseudo(userID)
        temp_score = userKey["score"]  # Obtient le score ou 0 s'il n'existe pas
        temp_ratio_r = userKey["nbr_ratio_r"]  # Obtient le ratio_r ou 0 s'il n'existe pas
        temp_ratio_sr = userKey["nbr_ratio_sr"]  # Obtient le ratio_sr ou 0 s'il n'existe pas
        temp_ratio_lr = userKey["nbr_ratio_lr"]  # Obtient le ratio_lr ou 0 s'il n'existe pas
        await ctx.send(f"**Profile de {temp_pseudo}** :\n- score : {temp_score}\n- ratio RARE : {temp_ratio_r}\n- ratio SUPER RARE : {temp_ratio_sr}\n- ratio LEGENDARY RARE : {temp_ratio_lr}")
    else:
        await ctx.send("L'utilisateur n'existe pas sorry --'")
        
async def get_pseudo(userID):
    try:
        user = await bot.fetch_user(userID)
        if user:
            return user.name  # Vous pouvez retourner le nom d'utilisateur ici
        else:
            return None
    except discord.errors.NotFound:
        return None  # L'utilisateur n'a pas été trouvé


id_utilisateur = "301727996392505346"

def get_user_infos(userID):
    print(f"Voici l'id pour le get user infos : {userID}")
    listProfiles = get_loaded_profiles()
    if str(userID) in listProfiles:
        return listProfiles[str(userID)]
    else:
        return None  # Retourne None si l'utilisateur n'est pas trouvé
    
      
def add_score(userID):
    try:
        # Ouvrir le fichier JSON en mode lecture
        with open(PROFILE_JSON_DIR, 'r') as fichier:
            data = json.load(fichier)

        # Vérifier si l'utilisateur existe dans le fichier JSON
        if str(userID) in data:
            # Modifier le score de l'utilisateur
            data[str(userID)]["score"] = data[str(userID)]["score"] + 1
        else:
            # Créer un nouvel utilisateur avec un score de 1
            data[str(userID)] = {
                "score": 1,
                "nbr_ratio_r": 0,
                "nbr_ratio_sr": 0,
                "nbr_ratio_lr": 0
            }

        # Ouvrir le fichier JSON en mode écriture pour enregistrer les modifications
        with open(PROFILE_JSON_DIR, 'w') as fichier:
            json.dump(data, fichier, indent=4)
        print(f"Score de l'utilisateur {str(userID)} mis a jour avec succes")

    except FileNotFoundError:
        print("Le fichier JSON n a pas ete trouve.")
    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")
        
def add_ratio_r(userID):
    try:
        # Ouvrir le fichier JSON en mode lecture
        with open(PROFILE_JSON_DIR, 'r') as fichier:
            data = json.load(fichier)

        # Vérifier si l'utilisateur existe dans le fichier JSON
        if str(userID) in data:
            # Modifier le score de l'utilisateur
            data[str(userID)]["nbr_ratio_r"] = data[str(userID)]["nbr_ratio_r"] + 1
        else:
            # Créer un nouvel utilisateur avec un score de 1
            data[str(userID)] = {
                "score": 0,
                "nbr_ratio_r": 1,
                "nbr_ratio_sr": 0,
                "nbr_ratio_lr": 0
            }

        # Ouvrir le fichier JSON en mode écriture pour enregistrer les modifications
        with open(PROFILE_JSON_DIR, 'w') as fichier:
            json.dump(data, fichier, indent=4)
        print(f"Le nombre de ratio R de l'utilisateur {str(userID)} mis a jour avec succes")

    except FileNotFoundError:
        print("Le fichier JSON n a pas ete trouve.")
    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")
        
def add_ratio_sr(userID):
    try:
        # Ouvrir le fichier JSON en mode lecture
        with open(PROFILE_JSON_DIR, 'r') as fichier:
            data = json.load(fichier)

        # Vérifier si l'utilisateur existe dans le fichier JSON
        if str(userID) in data:
            # Modifier le score de l'utilisateur
            data[str(userID)]["nbr_ratio_sr"] = data[str(userID)]["nbr_ratio_sr"] + 1
        else:
            # Créer un nouvel utilisateur avec un score de 1
            data[str(userID)] = {
                "score": 0,
                "nbr_ratio_r": 0,
                "nbr_ratio_sr": 1,
                "nbr_ratio_lr": 0
            }

        # Ouvrir le fichier JSON en mode écriture pour enregistrer les modifications
        with open(PROFILE_JSON_DIR, 'w') as fichier:
            json.dump(data, fichier, indent=4)
        print(f"Le nombre de ratio SR de l'utilisateur {str(userID)} mis a jour avec succes")

    except FileNotFoundError:
        print("Le fichier JSON n a pas ete trouve.")
    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")
        
def add_ratio_lr(userID):
    try:
        # Ouvrir le fichier JSON en mode lecture
        with open(PROFILE_JSON_DIR, 'r') as fichier:
            data = json.load(fichier)

        # Vérifier si l'utilisateur existe dans le fichier JSON
        if str(userID) in data:
            # Modifier le score de l'utilisateur
            data[str(userID)]["nbr_ratio_lr"] = data[str(userID)]["nbr_ratio_lr"] + 1
        else:
            # Créer un nouvel utilisateur avec un score de 1
            data[str(userID)] = {
                "score": 0,
                "nbr_ratio_r": 0,
                "nbr_ratio_sr": 0,
                "nbr_ratio_lr": 1
            }

        # Ouvrir le fichier JSON en mode écriture pour enregistrer les modifications
        with open(PROFILE_JSON_DIR, 'w') as fichier:
            json.dump(data, fichier, indent=4)
        print(f"Le nombre de ratio LR de l'utilisateur {str(userID)} mis a jour avec succes")

    except FileNotFoundError:
        print("Le fichier JSON n a pas ete trouve.")
    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")