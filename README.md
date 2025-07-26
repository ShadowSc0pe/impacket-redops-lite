# Impacket RedOps Lite

**Impacket RedOps Lite** est une version légère, modulaire et furtive de certains outils issus du projet [Impacket](https://github.com/fortra/impacket), pensée pour la Red Team et les environnements embarqués (Raspberry Pi, Mini-PC, VMs, etc.).

## Objectif

Fournir une interface simplifiée pour exécuter des actions offensives classiques sur des systèmes Windows, avec un impact réduit, une installation minimale et un usage rapide.  
Tous les modules prennent en charge une configuration centralisée via un fichier `config.ini`.

## Fonctionnalités

Modules inclus :

- `redshell` : Exécution de commandes à distance via SMB (similaire à psexec)
- `redcreds` : Extraction locale de hachages utilisateur depuis les registres SAM/SYSTEM
- `redenum` : Enumération distante des utilisateurs via RPC/SAMR

## Configuration

Le fichier `config.ini` permet de définir des paramètres globaux :

```ini
[DEFAULT]
stealth = true
timeout = 5
results_directory = results
smb_service_name = RedOpsSvc
```

## Installation

1. Cloner le dépôt :

```bash
git clone https://github.com/ShadowSc0pe/impacket-redops-lite.git
cd impacket-redops-lite
```

2. Installer les dépendances :

```bash
pip install -r requirements.txt
```

## Utilisation

Commandes de base :

```bash
python3 redops.py <module> [options]
```

Exemples :

```bash
python3 redops.py redenum -t 192.168.1.10 -u admin -p password
python3 redops.py redshell -t 192.168.1.10 -u admin -p password -c "whoami"
sudo python3 redops.py redcreds
```

Les résultats sont automatiquement enregistrés dans le dossier `results/`.

## Configuration

Vous pouvez ajuster le fichier `config.ini` pour modifier le mode furtif ou le timeout par défaut.

## Avertissement

Ce projet est fourni à des fins éducatives et professionnelles uniquement.  
L'utilisation sur des systèmes sans autorisation explicite est illégale.

## Crédits

Ce projet est basé en partie sur le code de la suite [Impacket](https://github.com/fortra/impacket), distribuée sous licence Apache 2.0.

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENCE](/LICENSE) pour plus d'informations.