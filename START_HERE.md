# 🚀 COMMENCEZ ICI - Stark Log

Bienvenue dans **Stark Log**, votre système de monitoring avancé !

## ⚡ Étape 1: Configuration (5 minutes)

### A. Créer un compte Supabase

1. Allez sur **https://supabase.com**
2. Cliquez **Sign up** → Créez un compte gratuit
3. Créez un nouveau **Project**
4. ⏳ Attendez le déploiement (1-2 minutes)

### B. Récupérer vos Credentials

1. Allez dans **Settings** → **API**
2. Copiez:
   - `Project URL`
   - `anon public` key
   - `service_role secret` key

### C. Configurer le Fichier `.env`

1. Ouvrez le fichier `.env` à la racine du projet
2. Remplacez par vos valeurs:

```
SUPABASE_URL=https://votre-url-supabase.supabase.co
SUPABASE_ANON_KEY=votre_clé_anon_ici
SUPABASE_SERVICE_ROLE_KEY=votre_clé_service_role_ici
```

3. Sauvegardez le fichier

## 🔧 Étape 2: Installation (3 minutes)

### Option 1: Démarrage Automatique (Recommandé)

**Windows:**
1. Double-cliquez `run.bat`
2. Laissez faire l'installation automatique

**macOS/Linux:**
1. Ouvrez Terminal
2. Lancez: `bash run.sh`

### Option 2: Installation Manuelle

```bash
# Créer environnement virtuel
python3 -m venv venv

# Activer l'environnement
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python3 main.py
```

## ✅ Étape 3: Première Utilisation (2 minutes)

1. **Explorez!** 🎉
   - Consultez le Dashboard
   - Essayez le nettoyage de RAM
   - Visitez le Chat
   - Gérez vos fichiers

## 📚 Ressources Utiles

| Document | Pour... |
|----------|---------|
| **QUICKSTART.md** | Démarrer en 60 secondes |
| **GUIDE.md** | Comprendre chaque fonctionnalité |
| **INSTALL.md** | Résoudre les problèmes d'installation |
| **README.md** | Vue d'ensemble générale |

## ⚠️ Problèmes Courants?

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "SUPABASE_URL not found"
Vérifiez que le fichier `.env` est bien rempli (voir Étape 1.C)

### "Connection refused"
- Vérifiez votre connexion internet
- Vérifiez que Supabase est actif
- Vérifiez vos credentials

### Permissions refusées
- Sur Windows: Lancez en tant qu'administrateur
- Sur macOS/Linux: Utilisez `sudo` si nécessaire

## 🎯 Commandes Utiles

```bash
# Vérifier que tout est installé
python3 verify.py

# Tester les imports
python3 test_imports.py

# Mettre à jour les dépendances
pip install -r requirements.txt --upgrade

# Désactiver l'environnement virtuel
deactivate
```

## 🎓 Tutoriel Rapide

### Dashboard
- 📊 Voyez votre RAM en temps réel
- 🔵🟡🔴 Les couleurs indiquent l'utilisation
- ⚙️ Cliquez sur les processus pour détails

### Optimisation
- 🧹 Nettoyez la RAM en un clic
- 🛑 Fermez les apps qui consomment trop
- ⚡ Améliorez les performances

### Chat
- 💬 Échangez avec les autres utilisateurs
- 🔄 Synchronisation temps réel
- 📝 Historique conservé

### Fichiers
- 📁 Naviguez votre système
- 👁️ Prévisualisez les fichiers texte
- 📊 Visualisez l'usage disque

## ✨ Conseils d'Utilisation

1. ✅ Nettoyez la RAM régulièrement
2. ✅ Consultez le dashboard quotidiennement
3. ✅ Participez au chat communautaire
4. ✅ Surveillez votre stockage disque

## 🚀 Prochaines Étapes

1. [ ] Configuration Supabase complète
2. [ ] Installation des dépendances
3. [ ] Créer votre compte
4. [ ] Explorer le Dashboard
5. [ ] Essayer le nettoyage
6. [ ] Utiliser le Chat
7. [ ] Consulter les paramètres

## 📞 Besoin d'Aide?

1. Consultez **GUIDE.md** pour les détails
2. Consultez **INSTALL.md** pour l'installation
3. Vérifiez votre configuration `.env`
4. Assurez-vous que Python 3.8+ est installé

## 🎉 C'est Prêt!

Vous êtes maintenant prêt à utiliser **Stark Log**!

Lancez l'application et commencez à monitorer votre système.

---

**Questions?** Consultez la documentation complète dans les fichiers `.md`

**Bonne chance!** 🚀
