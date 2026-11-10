@echo off
REM Script de démarrage pour Windows

if not exist "venv" (
    echo Création de l'environnement virtuel...
    python -m venv venv
)

echo Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

echo Installation des dépendances...
pip install -r requirements.txt -q

echo Lancement de Stark Log...
python main.py
pause
