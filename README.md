# Stark Log - Système de Monitoring Avancé

Une application desktop complète pour surveiller et gérer votre ordinateur en temps réel.

## Fonctionnalités

### 📊 Dashboard
- Surveillance RAM en temps réel avec graphiques dynamiques
- Indicateurs visuels de l'utilisation (bleu 0-30%, jaune 31-49%, rouge 50-80%, clignotant 80%+)
- Liste des processus actifs avec consommation mémoire
- Gestion des applications ouvertes

### 🧹 Optimisation
- **Nettoyer la RAM**:
  - Option pour fermer TOUS les logiciels
  - Option pour sélectionner les logiciels à fermer
  - Nettoyage des caches système

### 🔍 Cache DNS
- Visualisation du cache DNS sauvegardé
- Fonction de vidage du cache DNS complet

### 💾 Gestionnaire de Fichiers
- Navigation complète du système de fichiers
- Aperçu des fichiers texte
- Gestion des disques et stockage
- Visualisation du contenu des dossiers

### 💬 Chat Communauté
- Chat en temps réel avec les autres utilisateurs
- Messages synchronisés en direct

### ⚙️ Paramètres
- Mode sombre/clair
- Styles de graphiques (courbe/cercle)

## Installation

### Prérequis
- Python 3.8+
- pip

### Étapes

1. **Clonez ou téléchargez le projet**

2. **Créez un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. **Installez les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurez les variables d'environnement**
Modifiez le fichier `.env` avec vos credentials Supabase:
```
SUPABASE_URL=votre_url_supabase
SUPABASE_ANON_KEY=votre_clé_anonyme
SUPABASE_SERVICE_ROLE_KEY=votre_clé_service_role
```

5. **Lancez l'application**
```bash
python main.py
```

## Architecture

```
project/
├── main.py                 # Point d'entrée
├── config/
│   └── settings.py        # Gestion des paramètres locaux
├── services/
│   ├── system_monitor.py  # Monitoring système
│   ├── chat_service.py    # Service chat
│   └── supabase_client.py # Client Supabase
├── ui/
│   ├── app.py            # Application principale
│   ├── frames/
│   │   ├── dashboard.py  # Dashboard principal
│   │   ├── storage.py    # Gestionnaire de fichiers
│   │   ├── chat.py       # Chat
│   │   ├── settings.py   # Paramètres
│   └── widgets/
│       ├── ram_monitor.py      # Widget RAM
│       ├── cleanup_popup.py    # Popup nettoyage
│       ├── dns_popup.py        # Popup DNS
│       └── process_list.py     # Liste processus
└── requirements.txt

```

## Technologies Utilisées

- **CustomTkinter**: Interface utilisateur moderne
- **Psutil**: Monitoring système
- **Matplotlib**: Graphiques temps réel
- **Supabase**: Backend
- **Python 3.8+**: Langage principal

## Utilisation

### Dashboard
- Consultez l'utilisation RAM en temps réel
- Cliquez sur "Nettoyer la RAM" pour optimiser
- Consultez les processus actifs

### Cache DNS
- Cliquez sur "Cache DNS" pour voir les entrées
- Cliquez "Vider le Cache" pour nettoyer

### Chat
- Accédez au chat communauté depuis le menu
- Envoyez des messages aux autres utilisateurs
- Les messages se synchronisent en temps réel

## Notes Importantes

- Certaines opérations (fermeture d'applications, vidage DNS) peuvent nécessiter les droits administrateur
- L'application sauvegarde votre session localement
- Les données sont synchronisées avec Supabase en temps réel

## Licence

Libre d'utilisation
# desktop_
