.PHONY: a5 helman main help

a5:
@printf "a5.py est un module de bibliothèque. Utilisez 'make main' ou 'python3 main.py'.\n"

helman:
@printf "helman.py est un module de bibliothèque. Utilisez 'make main' ou 'python3 main.py'.\n"

main:
python3 main.py

help:
@printf "Usage:\n  make main     # exécute le script de démonstration\n  make a5       # rappel : a5.py est un module de bibliothèque\n  make helman   # rappel : helman.py est un module de bibliothèque\n"
