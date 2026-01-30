# Clash Royal - Jeu Pokémon Tour par Tour

Un jeu de combat tour par tour inspiré de Pokémon, utilisant les personnages de Clash Royale, développé avec Pygame.

## Structure du Projet

```
Clash_superV2/
│
├── main.py                          # Point d'entrée du jeu
│
├── assets/                          # Ressources du jeu
│   ├── images/                      # Images et sprites
│   │   ├── characters/              # Sprites des personnages
│   │   ├── backgrounds/             # Arrière-plans des combats
│   │   ├── ui/                      # Éléments d'interface
│   │   └── effects/                 # Effets visuels (attaques, etc.)
│   │
│   ├── sounds/                      # Effets sonores et musiques
│   │   ├── music/                   # Musiques de fond
│   │   └── sfx/                     # Effets sonores
│   │
│   └── fonts/                       # Polices de caractères
│
├── src/                             # Code source
│   ├── __init__.py
│   │
│   ├── characters/                  # Gestion des personnages
│   │   ├── __init__.py
│   │   ├── character.py             # Classe de base Character
│   │   ├── player_character.py      # Personnage du joueur
│   │   ├── enemy_character.py       # Personnage ennemi
│   │   └── character_data.py        # Données des personnages Clash Royale
│   │
│   ├── combat/                      # Système de combat
│   │   ├── __init__.py
│   │   ├── battle.py                # Logique du combat tour par tour
│   │   ├── moves.py                 # Attaques et capacités
│   │   └── battle_ai.py             # IA pour les ennemis
│   │
│   ├── ui/                          # Interface utilisateur
│   │   ├── __init__.py
│   │   ├── menu.py                  # Menu principal
│   │   ├── battle_ui.py             # Interface de combat
│   │   ├── character_selection.py   # Sélection de personnages
│   │   └── hud.py                   # Affichage PV, infos, etc.
│   │
│   ├── screens/                     # Différents écrans du jeu
│   │   ├── __init__.py
│   │   ├── title_screen.py          # Écran titre
│   │   ├── battle_screen.py         # Écran de combat
│   │   └── victory_screen.py        # Écran victoire/défaite
│   │
│   └── utils/                       # Utilitaires
│       ├── __init__.py
│       ├── config.py                # Configuration (résolution, FPS, etc.)
│       ├── assets_loader.py         # Chargement des ressources
│       └── animation.py             # Gestion des animations
│
├── data/                            # Données du jeu
│   ├── characters.json              # Stats des personnages
│   └── moves.json                   # Liste des attaques
│
├── requirements.txt                 # Dépendances Python
└── README.md                        # Ce fichier
```

## Modules Principaux

### 1. **Characters** (`src/characters/`)
- Gestion des personnages Clash Royale (Chevalier, Archer, Dragon, Géant, etc.)
- Stats : PV, Attaque, Défense, Vitesse
- Système de types/affinités

### 2. **Combat** (`src/combat/`)
- Système tour par tour
- Sélection d'attaques
- Calcul des dégâts
- IA pour les adversaires

### 3. **UI** (`src/ui/`)
- Menu principal
- Interface de combat (barres de vie, boutons d'action)
- Sélection de personnages
- Affichage des informations

### 4. **Screens** (`src/screens/`)
- Gestion des différents écrans (titre, combat, victoire)
- Transitions entre les écrans

## Installation

```bash
pip install -r requirements.txt
```

## Lancement du Jeu

```bash
python main.py
```

## Technologies Utilisées

- **Python 3.x**
- **Pygame** - Moteur de jeu
- **JSON** - Stockage des données