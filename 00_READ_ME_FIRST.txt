================================================================================
                    STARK LOG - SYSTÈME DE MONITORING
                         Version 1.0.0
================================================================================

BIENVENUE !

Vous avez reçu "Stark Log", une application desktop complète de monitoring
et gestion de système développée en Python avec CustomTkinter et Supabase.

================================================================================
DÉMARRAGE RAPIDE (10 minutes)
================================================================================

1. Lisez d'abord: START_HERE.md

2. Configuration Supabase:
   - Allez sur https://supabase.com
   - Créez un compte gratuit
   - Créez un nouveau projet
   - Copiez les credentials (voir START_HERE.md)

3. Remplissez le fichier .env:
   - Ouvrez: .env
   - Collez vos credentials Supabase
   - Sauvegardez

4. Lancez l'application:
   - Windows: Double-cliquez run.bat
   - macOS/Linux: Lancez bash run.sh

5. Créez un compte et explorez!

================================================================================
FICHIERS IMPORTANTS
================================================================================

DOCUMENTATION (Lisez dans cet ordre):
  1. START_HERE.md           ← COMMENCEZ ICI
  2. QUICKSTART.md           Démarrage 60 secondes
  3. INSTALL.md              Guide d'installation
  4. GUIDE.md                Guide complet
  5. README.md               Vue d'ensemble
  6. PROJECT_SUMMARY.md      Détails techniques
  7. INDEX.md                Index de tous les fichiers

CONFIGURATION:
  - .env                     À REMPLIR avec Supabase credentials
  - .env.example             Exemple de configuration

DÉMARRAGE:
  - main.py                  Lance l'application
  - verify.py                Vérifie les dépendances
  - test_imports.py          Teste les imports
  - run.sh / run.bat         Scripts de démarrage

DÉPENDANCES:
  - requirements.txt         Packages Python

================================================================================
STRUCTURE DU PROJET
================================================================================

config/              → Configuration et paramètres
services/            → Services métier (monitoring, auth, chat)
ui/                  → Interface utilisateur
  ├── frames/        → Pages principales
  └── widgets/       → Composants réutilisables

================================================================================
FONCTIONNALITÉS PRINCIPALES
================================================================================

✅ Dashboard
   - Monitoring RAM en temps réel
   - Graphiques avec Matplotlib
   - Codes couleurs (bleu→jaune→rouge)
   - Liste processus actifs

✅ Optimisation
   - Nettoyer la RAM
   - Arrêter processus
   - Vider caches

✅ Cache DNS
   - Visualiser cache DNS
   - Vider le cache

✅ Gestionnaire de Fichiers
   - Navigation complète
   - Aperçu fichiers
   - Gestion disques

✅ Chat Communauté
   - Chat temps réel
   - Synchronisation Supabase
   - Historique messages

✅ Authentification
   - Inscription
   - Connexion sécurisée

✅ Paramètres
   - Mode sombre/clair
   - Styles graphiques

================================================================================
PRÉREQUIS
================================================================================

- Python 3.8 ou supérieur
- pip (gestionnaire packages)
- Connexion internet
- Compte Supabase (gratuit)

================================================================================
PROBLÈMES?
================================================================================

Consultez les documents:
- INSTALL.md          → Problèmes d'installation
- GUIDE.md            → Questions d'utilisation
- START_HERE.md       → Configuration

================================================================================
COMMANDES UTILES
================================================================================

# Vérifier installation
python3 verify.py

# Tester imports
python3 test_imports.py

# Mettre à jour dépendances
pip install -r requirements.txt --upgrade

================================================================================
PROCHAINES ÉTAPES
================================================================================

1. [ ] Lire START_HERE.md
2. [ ] Créer compte Supabase
3. [ ] Récupérer credentials
4. [ ] Remplir .env
5. [ ] Installer dépendances
6. [ ] Lancer application
7. [ ] Créer compte utilisateur
8. [ ] Explorer Dashboard

================================================================================
                    👉 COMMENCEZ PAR: START_HERE.md 👈
================================================================================

Pour toute aide, consultez les fichiers .md dans ce répertoire.

Bon usage de Stark Log!

================================================================================
