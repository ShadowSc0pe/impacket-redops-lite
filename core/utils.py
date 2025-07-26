import os
import json
import time
def ensure_results_dir():
    """
    Vérifie si le dossier 'results/' existe. Le crée si nécessaire.
    Utilisé pour stocker les résultats d'exécution des modules.
    """
    os.makedirs("results", exist_ok=True)
def save_output(data, prefix):
    """
    Enregistre les résultats d'un module dans un fichier JSON horodaté.

    Arguments :
    - data : objet Python (liste ou dict) à enregistrer
    - prefix : préfixe du fichier (ex : 'credentials', 'users')

    Retourne :
    - Le chemin absolu du fichier sauvegardé
    """
    ensure_results_dir()
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"results/{prefix}_{timestamp}.json"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return filename
    except Exception as e:
        print(f"[ERREUR] Impossible de sauvegarder le fichier : {e}")
        return None
def print_banner(name):
    """
    Affiche une bannière simple avec le nom du module actif.

    Argument :
    - name : nom du module à afficher
    """
    print(f"\n====== Impacket RedOps Lite ======\nModule actif : {name}\n")
