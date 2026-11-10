#!/bin/bash

if [ ! -d "venv" ]; then
    echo "Création de l'environnement virtuel..."
    python3 -m venv venv
fi

echo "Activation de l'environnement virtuel..."
source venv/bin/activate

echo "Installation des dépendances..."
pip install -r requirements.txt -q

echo "Lancement de Stark Log..."
python3 main.py
