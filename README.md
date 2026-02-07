
# Lier Minecraft (Java) à VSCode avec Minescript Client — Guide Python

Ce guide montre comment configurer `minescript client` (édition Minecraft Java, dernière version) pour exécuter des scripts Python depuis VSCode, et comment créer une première commande `/hello` en Python.

Prérequis
- Minecraft Java installé.
- `minescript client` installé côté client (mod/extension). Suivez la doc officielle du client pour l'installation.
- Visual Studio Code (VSCode).
- Python 3 installé (version 3.8+ recommandée).

1) Installer et localiser `minescript client`
- Installez le client selon sa documentation (Fabric/Forge ou autre).
- Recherchez le dossier de scripts du client — par exemple `~/.minecraft/minescript/scripts` (le chemin peut varier selon le client). C'est là où placer vos scripts Python.

2) Ouvrir le projet dans VSCode
- Ouvrez ce dossier de projet dans VSCode pour éditer vos scripts (`hello.py` existe déjà dans le dépôt).

3) Exemple Python — `hello.py`
- Placez (ou éditez) le fichier `hello.py` dans le dossier du projet. Exemple générique fourni :

```python
# hello.py — exemple Minescript (Python)
# Handler simple pour une commande `/hello`

def on_hello(player, args):
    """Envoyer un message au joueur. Adaptez au nom de méthode disponible dans votre client."""
    try:
        player.send_message("§aBonjour depuis Minescript (Python) !")
    except Exception:
        try:
            player.sendMessage("§aBonjour depuis Minescript (Python) !")
        except Exception:
            print("Bonjour depuis Minescript (Python) ! (fallback)")

# Enregistrement de la commande — adaptez selon l'API du client
command("hello", on_hello)
```

Remarque : la forme exacte d'enregistrement d'une commande (`command(...)`) et les méthodes disponibles sur `player` dépendent de la version du `minescript client` — adaptez-les si nécessaire.

4) Déployer le script dans Minecraft
- Copiez `hello.py` vers le dossier de scripts du client (ex. `~/.minecraft/minescript/scripts/`).

Exemple de copie (Linux) :

```bash
cp hello.py ~/.minecraft/minescript/scripts/hello.py
```

- Redémarrez Minecraft si nécessaire ou utilisez la commande de rechargement fournie par le client (ex. `/ms reload`).

5) Ajouter une tâche VSCode pour copier automatiquement (optionnel)
- Créez `.vscode/tasks.json` dans ce projet avec une tâche simple pour copier `hello.py` :

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Copier hello.py vers Minecraft",
      "type": "shell",
      "command": "cp",
      "args": ["${workspaceFolder}/hello.py", "~/.minecraft/minescript/scripts/hello.py"],
      "group": "none",
      "problemMatcher": []
    }
  ]
}
```

Vous pouvez exécuter cette tâche depuis la palette de commandes (Ctrl+Shift+P → Tasks: Run Task).

6) Tester en jeu
- Ouvrez un monde ou serveur local.
- Exécutez la commande que vous avez enregistrée, par exemple : `/hello`.
- Attendez le message dans le chat : "Bonjour depuis Minescript (Python) !".

Dépannage rapide
- Rien ne s'affiche : vérifiez la console client Minecraft pour les erreurs de parsing ou d'import.
- Erreur liée à `command` ou `player` : consultez la documentation du `minescript client` pour connaître les noms exacts des fonctions et méthodes Python.

Besoin d'aide pour adapter l'exemple
- Si vous me fournissez le lien du dépôt ou de la documentation du `minescript client` (ou son API Python), j'adapterai `hello.py` et les instructions pour être exacts et compatibles.

---
Fichiers notables : `hello.py` (exemple Python)
