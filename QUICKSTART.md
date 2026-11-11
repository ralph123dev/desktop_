# Quick Start - Stark Log

## 60 secondes pour démarrer

### Étape 1: Préparation Supabase (2 min)

1. Allez sur https://supabase.com → Sign up
2. Créez un nouveau projet
3. Attendez le déploiement
4. Allez dans **Settings** → **API**
5. Copiez les 3 valeurs:
   - Project URL
   - anon public key
   - service_role secret key

### Étape 2: Configuration (1 min)

1. Ouvrez le fichier `.env`
2. Remplacez par vos valeurs:
```
SUPABASE_URL=votre_url
SUPABASE_ANON_KEY=votre_clé
SUPABASE_SERVICE_ROLE_KEY=votre_clé_service_role
```

### Étape 3: Installation & Démarrage

**Windows:**
```
run.bat
```

**macOS/Linux:**
```
bash run.sh
```

Ou manuellement:
```
python3 -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sur Windows
pip install -r requirements.txt
python3 main.py
```

### Étape 4: Utilisation (30 sec)

Explorez le Dashboard et les autres pages depuis le menu.

## Fonctionnalités Principales

| Fonctionnalité | Comment Accéder |
|---|---|
| **Monitor RAM** | Dashboard → Voyez l'utilisation en temps réel |
| **Nettoyer RAM** | Dashboard → Cliquez "Nettoyer la RAM" |
| **Cache DNS** | Dashboard → Cliquez "Cache DNS" |
| **Fichiers** | Onglet "Stockage" |
| **Chat** | Onglet "Chat" |
| **Paramètres** | Onglet "Paramètres" |

## Codes Couleur RAM

| Couleur | Signification | Utilisation |
|---|---|---|
| 🔵 Bleu | Utilisation faible | 0-30% |
| 🟡 Jaune | Modéré | 31-49% |
| 🔴 Rouge | Élevé | 50-80% |
| 🔴 Rouge clignotant | Critique | 80%+ |

## Problème?

- L'app ne démarre pas? → Consultez INSTALL.md
- Question sur une fonctionnalité? → Consultez GUIDE.md
- Erreur de configuration? → Vérifiez votre `.env`

## Prochaines Étapes

1. Explorez chaque onglet
2. Créez des amis dans le chat
3. Utilisez le nettoyage régulièrement
4. Consultez le gestionnaire de fichiers
5. Personnalisez dans les paramètres

Bon usage! 🚀
