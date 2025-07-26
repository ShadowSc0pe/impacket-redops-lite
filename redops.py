import argparse
import configparser
from modules import redshell, redcreds, redenum

# Point d'entrée principal du programme CLI
# Ce script permet de lancer les modules RedOps en fonction des paramètres fournis
# et de charger dynamiquement les configurations à partir du fichier config.ini

def main():
    # Chargement de la configuration globale depuis config.ini
    config = configparser.ConfigParser()
    config.read("config.ini")
    # Lecture des valeurs globales avec valeurs par défaut en cas d'absence
    stealth = config.getboolean("DEFAULT", "stealth", fallback=True)
    timeout = config.getint("DEFAULT", "timeout", fallback=5)

    # Argument parser pour les modules
    parser = argparse.ArgumentParser(description="Impacket RedOps Lite - Outils Red Team légers et modulaires")
    # Argument principal : choix du module à exécuter
    parser.add_argument("module", help="Module à exécuter : redshell, redcreds ou redenum")
    # Options communes pour les modules distants
    parser.add_argument("-t", "--target", help="Adresse IP ou nom d'hôte de la cible")
    parser.add_argument("-u", "--user", help="Nom d'utilisateur pour l'authentification")
    parser.add_argument("-p", "--password", help="Mot de passe associé à l'utilisateur")
    parser.add_argument("-d", "--domain", default="", help="Nom du domaine (optionnel)")
    # Option spécifique au module redshell (commande à exécuter)
    parser.add_argument("-c", "--cmd", default="whoami", help="Commande à exécuter via SMB (module redshell seulement)")

    args = parser.parse_args()
    # Dispatch vers le module sélectionné
    if args.module == "redshell":
        redshell.run(args.target, args.user, args.password, args.domain, args.cmd, stealth, timeout)
    elif args.module == "redcreds":
        redcreds.run(stealth)
    elif args.module == "redenum":
        redenum.run(args.target, args.user, args.password, args.domain, stealth, timeout)
    else:
        print("[ERREUR] Module inconnu. Veuillez choisir parmi : redshell, redcreds ou redenum.")
if __name__ == "__main__":
    main()