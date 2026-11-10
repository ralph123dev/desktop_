# Guide Complet - Stark Log

## Configuration Initiale

### 1. Créer un compte Supabase

1. Allez sur https://supabase.com
2. Créez un compte gratuit
3. Créez un nouveau projet
4. Attendez que le projet soit déployé

### 2. Récupérer les Credentials

1. Allez dans **Project Settings** → **API**
2. Copiez:
   - **Project URL** → `SUPABASE_URL`
   - **anon public** key → `SUPABASE_ANON_KEY`
   - **service_role secret** key → `SUPABASE_SERVICE_ROLE_KEY`

3. Collez-les dans le fichier `.env`:
```
SUPABASE_URL=https://lvyuwrrdjeihbriblpcp.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 3. Installer les Dépendances

**macOS/Linux:**
```bash
bash run.sh
```

**Windows:**
```bash
run.bat
```

Ou manuellement:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

## Guide Utilisateur

### Première Connexion

1. **Créer un compte**:
   - Cliquez sur "Créer un compte"
   - Entrez un email valide
   - Choisissez un mot de passe (min 6 caractères)
   - Entrez un nom d'utilisateur unique
   - Cliquez "S'inscrire"

2. **Se connecter**:
   - Entrez votre email et mot de passe
   - Cliquez "Connexion"

### Dashboard

#### Surveillance RAM
- **Graphique en temps réel**: Affiche l'utilisation RAM
- **Codes couleurs**:
  - 🔵 Bleu (0-30%): Utilisation faible
  - 🟡 Jaune (31-49%): Utilisation modérée
  - 🔴 Rouge (50-80%): Utilisation élevée
  - 🔴 Rouge clignotant (80%+): Critique

#### Liste des Disques
- Affiche tous les disques connectés
- Barre de progression pour chaque disque
- Espace utilisé/total en GB

### Optimisation

#### Nettoyer la RAM
Trois options:

1. **Fermer TOUS les logiciels**
   - ⚠️ Attention: Ferme tous les processus actifs sauf le système
   - Utiliser en dernier recours

2. **Sélectionner les logiciels**
   - Choisissez les processus à fermer
   - Cochez les processus à arrêter
   - Cliquez "Arrêter Sélectionnés"

3. **Vider les caches**
   - Nettoie tous les caches système
   - Récupère de la mémoire

### Cache DNS

1. Cliquez sur "Cache DNS"
2. Consultez les entrées en cache
3. Cliquez "Vider le Cache" pour nettoyer

### Gestionnaire de Fichiers

1. **Navigation**:
   - Double-cliquez sur un dossier pour l'ouvrir
   - "← Retour" pour revenir au dossier parent
   - "🏠 Accueil" pour revenir au répertoire utilisateur

2. **Aperçu des fichiers**:
   - Cliquez sur un fichier pour voir son aperçu
   - Affiche la taille, le chemin, et l'extension
   - Pour les fichiers texte: affiche les 1000 premiers caractères

### Chat Communauté

1. Connectez-vous
2. Allez dans l'onglet "Chat"
3. Tapez votre message
4. Appuyez sur "Entrée" ou cliquez "📤 Envoyer"
5. Les messages se synchronisent en temps réel

### Paramètres

#### Thème
- **Mode Sombre**: Interface noire (par défaut)
- **Mode Clair**: Interface blanche

#### Style des Courbes
- **Courbe**: Graphique ligne lissée
- **Cercle**: Affichage circulaire (à venir)

## Dépannage

### L'app ne démarre pas
- Vérifiez que Python 3.8+ est installé
- Vérifiez que toutes les dépendances sont installées: `pip install -r requirements.txt`
- Vérifiez votre fichier `.env`

### Erreur de connexion
- Vérifiez votre connexion internet
- Vérifiez vos credentials Supabase
- Vérifiez que le projet Supabase est actif

### Pas de données dans le Chat
- Vérifiez que vous êtes connecté
- Attendez quelques secondes (synchronisation)
- Rafraîchissez en changeant d'onglet

### Permissions refusées
- Certaines opérations nécessitent les droits administrateur
- Sur Windows: Lancez l'app en tant qu'administrateur
- Sur macOS/Linux: Utilisez `sudo` si nécessaire

## Limitations Connues

- Les opérations administrateur (fermeture processus, vidage DNS) peuvent nécessiter les droits administrateur
- Le chat peut avoir un léger délai de synchronisation
- La lecture de fichiers volumineux peut être lente

## Architecture

```
Stark Log
├── Frontend: CustomTkinter (UI Desktop)
├── Backend: Supabase (Base de données)
├── Monitoring: Psutil (Système d'exploitation)
└── Real-time: Graphiques Matplotlib
```

## Fichiers Importants

- `main.py`: Point d'entrée
- `.env`: Credentials Supabase
- `requirements.txt`: Dépendances Python
- `config/settings.py`: Configuration locale
- `services/system_monitor.py`: Monitoring système
- `ui/app.py`: Application principale

## Améliorations Futures

- Historique des performances
- Export de rapports
- Notifications d'alerte
- Support multi-écran
- Mode portable

## Support

Pour toute question ou problème:
1. Consultez ce guide
2. Vérifiez votre configuration Supabase
3. Vérifiez votre connexion internet
