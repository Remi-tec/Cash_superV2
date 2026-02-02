# Lancement du Jeu - Clash Royal Combat Tour par Tour

## Installation des Dépendances

Avant de lancer le jeu, assurez-vous que toutes les dépendances sont installées :

```bash
pip install -r requirements.txt
```

Cela installera les packages nécessaires, principalement **Pygame**.

## Structure des Données

### Organisation des Fichiers

```
Clash_superV2/
├── code/
│   ├── main.py                 # Point d'entrée du jeu
│   ├── Fighter.py              # Classes Fighter et Opponent
│   ├── battle.py               # Logique du combat
│   ├── hud.py                  # Interface graphique
│   ├── settings.py             # Configuration (résolution, dimensions, etc.)
│   ├── support.py              # Fonctions utilitaires
│   ├── timer.py                # Système de timer
│   ├── start.py                # Initialisation
│   ├── __init__.py
│   └── data/
│       └── stats.json          # Données des combattants et attaques
├── images/
│   ├── back/                   # Images des combattants (vue de dos)
│   ├── front/                  # Images des adversaires (vue de face)
│   └── other/                  # Images de fond
└── audio/                      # Ressources audio (réservé pour évolution future)
```

### Fichier de Configuration : stats.json

Le fichier `code/data/stats.json` contient tous les données des combattants au format JSON.

#### Structure d'un Combattant

```json
{
    "fighters": {
        "NomDuCombattant": {
            "pv": 800,
            "attaques": [
                {
                    "nom": "Nom de l'attaque",
                    "degat": 45,
                    "pp": 20,
                    "effet": "normal",
                    "critique": 5
                }
            ]
        }
    }
}
```

#### Paramètres Expliqués

- **pv** : Points de vie maximum du combattant
- **attaques** : Tableau des 4 attaques disponibles
  - **nom** : Nom de l'attaque
  - **degat** : Dégâts infligés par l'attaque
  - **pp** : Points de Pouvoir (limite d'utilisation)
  - **effet** : Type d'effet spécial (voir section Effets)
  - **critique** : Pourcentage de chance de coup critique

#### Types d'Effets Disponibles

- **normal** : Attaque classique sans effet spécial
- **reduction_degat** : Réduit les dégâts reçus par 50% pendant 1 tour
- **poison** : Inflige 12.5% des PV max par tour
- **brulure** : Inflige 12.5% des PV max par tour
- **paralysie** : Réservé pour développement futur
- **gelé** : Réservé pour développement futur
- **repousse** : Repousse l'adversaire
- **etourdi** : Étourdissement réservé pour développement futur

## Préparation des Images

**IMPORTANT** : Vous devez placer les images des combattants avant de lancer le jeu.

### Emplacements Requis

1. **Images du Joueur** (vue de dos)
   - Placez dans : `images/back/`
   - Format : PNG
   - Exemple : `images/back/Chevalier.png`

2. **Images de l'Adversaire** (vue de face)
   - Placez dans : `images/front/`
   - Format : PNG
   - Exemple : `images/front/Archer.png`

3. **Image de Fond**
   - Placez dans : `images/other/`
   - Fichier : `bg.png`
   - Format : PNG

### Nommage

Le nom du fichier image (sans extension) doit correspondre exactement au nom du combattant défini dans `stats.json`.

**Exemple** :
- Combattant nommé "Chevalier" dans stats.json
- Image requise : `images/back/Chevalier.png`
- Image requise : `images/front/Chevalier.png`

## Lancement du Jeu

### Depuis le répertoire racine

```bash
cd code
python main.py
```

Ou directement depuis la racine du projet si vous avez configuré le chemin Python :

```bash
python code/main.py
```

### Vérification du Lancement

À la première exécution, le jeu affichera des messages de démarrage :
```
1. Initialisation pygame OK
2. Assets importés: X back, Y front, Z other
```

Si vous voyez ces messages, le jeu est prêt à démarrer.

## Contrôles du Jeu

### En Combat
- **Flèches Gauche (←) / Droite (→)** : Naviguer les attaques horizontalement
- **Flèches Haut (↑) / Bas (↓)** : Naviguer les attaques verticalement
- **ENTRÉE** : Confirmer et exécuter l'attaque sélectionnée
- **ESPACE** : Recommencer une partie après victoire/défaite

## Mécanique de Combat

### Déroulement

1. Le **joueur** sélectionne une attaque et la confirme
2. L'**adversaire** (IA) effectue une attaque automatique après 2 secondes
3. Les effets des attaques sont appliqués
4. Le combat continue jusqu'à ce qu'un combattant soit KO (PV = 0)
5. L'écran affiche le résultat (Victoire ou Défaite)

### Interface de Combat

L'écran affiche en permanence :
- **Infos du Joueur** : Nom, PV actuels/max, barre de vie, effets actifs
- **Infos de l'Adversaire** : Nom, PV actuels/max, barre de vie, effets actifs
- **Boutons d'Attaque** : 4 attaques avec leurs PP restants
- **Indicateur de Tour** : Indique à qui est le tour
- **Log de Combat** : Affiche les 3 derniers événements

## Dépannage

### Les images ne s'affichent pas
- Vérifiez que les fichiers PNG sont dans les bons dossiers
- Vérifiez que les noms correspondent exactement

### Le jeu crash au démarrage
- Vérifiez que Pygame est correctement installé : `pip install pygame`
- Vérifiez que le fichier `stats.json` existe et est valide

### Le jeu se ferme immédiatement
- Vérifiez les erreurs en exécutant depuis le terminal
- Assurez-vous que les images de fond (`bg.png`) existent

## Configuration Avancée

Les paramètres du jeu peuvent être ajustés dans `code/settings.py` :
- Résolution de la fenêtre
- FPS (images par seconde)
- Dimensions des sprites
- Autres constantes
