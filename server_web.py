# -*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route("/")
def hello():
        return render_template("buttonclick.html")

@app.route('/start_function', methods=['POST'])
def start_function():
    # Exécutez la fonction que vous souhaitez déclencher ici
    result = "Mike bot viens de plop"
    print("plop here")
    return result

@app.route('/view_score', methods=['POST'])
def start_soundboard():
    # Exécutez la fonction que vous souhaitez déclencher ici
    return "TQT MALO TOP 1 avec un ratio LEGENDAIRE SHEESSHH!"

def lire_fichier(chemin_du_fichier):
    try:
        with open(chemin_du_fichier, 'r', encoding='utf-8') as fichier:
            contenu = fichier.read()
        return contenu
    except FileNotFoundError:
        return "TQT MALO TOP 1 avec un ratio LEGENDAIRE SHEESSHH!"
    except Exception as e:
        return f"Une erreur s'est produite : {str(e)}"
    

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
