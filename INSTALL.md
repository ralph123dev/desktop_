# Installation - Stark Log

## Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Un compte Supabase (gratuit)

## Installation Rapide

### Windows

1. Téléchargez et installez Python depuis https://python.org
2. Ouvrez PowerShell dans le dossier du projet
3. Exécutez:
   ```powershell
   python run.bat
   ```

### macOS

1. Ouvrez Terminal
2. Installez Python avec Homebrew (si nécessaire):
   ```bash
   brew install python3
   ```
3. Dans le dossier du projet:
   ```bash
   bash run.sh
   ```

### Linux

1. Installez Python et pip:
   ```bash
   sudo apt-get install python3 python3-pip python3-tk
   ```
2. Dans le dossier du projet:
   ```bash
   bash run.sh
   ```

## Installation Manuelle

### 1. Créer un environnement virtuel

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Configurer Supabase

1. Allez sur https://supabase.com
2. Créez un compte gratuit
3. Créez un nouveau projet
4. Dans **Settings** → **API**, copiez:
   - Project URL
   - anon public key
   - service_role secret key

5. Collez dans le fichier `.env`:

```
SUPABASE_URL=https://votre-url.supabase.co
SUPABASE_ANON_KEY=votre_clé_anon
SUPABASE_SERVICE_ROLE_KEY=votre_clé_service_role
```

### 4. Lancer l'application

```bash
python3 main.py
```

## Vérification

Pour vérifier que tout est correctement installé:

```bash
python3 verify.py
```

## Dépannage

### "python: command not found"
- Utilisez `python3` au lieu de `python`
- Vérifiez que Python est installé: `python3 --version`

### "No module named customtkinter"
- Les dépendances ne sont pas installées
- Exécutez: `pip install -r requirements.txt`

### "ModuleNotFoundError: No module named 'dotenv'"
- Installez python-dotenv: `pip install python-dotenv`

### L'app démarre mais pas de données
- Vérifiez votre fichier `.env`
- Vérifiez votre connexion internet
- Assurez-vous que Supabase est configuré

## Structure du Projet

```
stark-log/
├── main.py                 # Point d'entrée
├── verify.py              # Vérification d'installation
├── requirements.txt       # Dépendances
├── .env                   # Configuration (NE PAS COMMITER)
├── .env.example          # Exemple de configuration
├── README.md             # Documentation générale
├── GUIDE.md              # Guide utilisateur
├── INSTALL.md            # Ce fichier
├── run.sh                # Script de démarrage (macOS/Linux)
├── run.bat               # Script de démarrage (Windows)
├── config/               # Configuration
│   ├── settings.py
│   └── theme.py
├── services/             # Services
│   ├── system_monitor.py
│   ├── chat_service.py
│   └── supabase_client.py
└── ui/                   # Interface utilisateur
    ├── app.py
    ├── frames/
    │   ├── dashboard.py
    │   ├── storage.py
    │   ├── chat.py
    │   └── settings.py
    └── widgets/
        ├── ram_monitor.py
        ├── cleanup_popup.py
        ├── dns_popup.py
        └── process_list.py
```

## Après Installation

1. **Première utilisation**:
   - Explorez le Dashboard

2. **Activation des fonctionnalités avancées**:
   - Certaines opérations nécessitent les droits administrateur
   - Sur Windows: Lancez l'app en tant qu'administrateur
   - Sur macOS/Linux: Vous pouvez utiliser `sudo` si nécessaire

3. **Optimisation**:
   - Testez le nettoyage de RAM
   - Consultez le cache DNS
   - Naviguez dans vos fichiers

## Désinstallation

Pour désinstaller complètement:

1. Supprimez le dossier du projet
2. (Optionnel) Supprimez le dossier config:
   - Windows: `%USERPROFILE%\.starklog`
   - macOS/Linux: `~/.starklog`

## Mise à Jour

Pour mettre à jour les dépendances:

```bash
pip install -r requirements.txt --upgrade
```

## Support

Pour toute aide:
1. Consultez GUIDE.md
2. Vérifiez votre configuration Supabase
3. Vérifiez les logs de l'application

Bon usage de Stark Log !
