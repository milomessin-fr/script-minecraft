import minescript

def main():
    # Avec MineScript, on utilise minescript.echo() pour envoyer un message
    try:
        minescript.echo("§aBonjour depuis MineScript (Python) !")
    except Exception as e:
        # En cas d'erreur, on affiche dans la console de debug
        print(f"Erreur : {e}")

if __name__ == "__main__":
    main()