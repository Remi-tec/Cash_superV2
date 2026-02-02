# Clash Royal - Jeu de Combat Tour par Tour

Un jeu de combat tour par tour utilisant les personnages de Clash Royale, développé avec Pygame.

## 🚀 Démarrage Rapide

### 1. Installation
```bash
pip install -r requirements.txt
```

### 2. Lancement
```bash
cd code
python main.py
```

## 📖 Documentation

Ce projet dispose de deux guides principaux :

### 🎮 [LANCEMENT_DU_JEU.md](LANCEMENT_DU_JEU.md)
- Comment installer et lancer le jeu
- Structure des données (stats.json)
- Organisation des fichiers
- Préparation des images
- Contrôles du jeu
- Guide de dépannage

### 👥 [AJOUTER_PERSONNAGES.md](AJOUTER_PERSONNAGES.md)
- Comment ajouter un nouveau personnage
- Édition du fichier stats.json
- Préparation des images (vue de dos et de face)
- Exemples complets
- Erreurs courantes et solutions

## 📁 Structure du Projet

```
code/
├── main.py              # Point d'entrée du jeu
├── Fighter.py           # Classes Fighter et Opponent
├── battle.py            # Logique du combat
├── hud.py               # Interface graphique
├── settings.py          # Configuration
├── support.py           # Utilitaires
├── timer.py             # Système de timer
└── data/
    └── stats.json       # Données des combattants

images/
├── back/                # Images du joueur (vue de dos)
├── front/               # Images de l'adversaire (vue de face)
└── other/               # Images de fond
```

## ⚙️ Configuration

Tous les paramètres du jeu peuvent être ajustés dans `code/settings.py`:
- Résolution de la fenêtre
- FPS (images par seconde)
- Dimensions des sprites

## 🎮 Mécanique de Jeu

**Système de Combat Tour par Tour**
- Sélectionnez une attaque et confirmez
- L'IA de l'adversaire joue automatiquement
- Combat jusqu'à KO (PV = 0)

## 📋 Spécifications

- **Python** : 3.8+
- **Pygame** : 2.0+
- **Format données** : JSON
- **Format images** : PNG
