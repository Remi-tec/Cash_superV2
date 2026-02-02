# CONFIGURATION DES IMAGES

## Images Requises

Le jeu nécessite les images suivantes. Placez-les dans les dossiers indiqués :

### 1. Images des Personnages

#### Joueur - Chevalier (Vue de Dos)
- **Chemin**: `images/back/Chevalier.png`
- **Dimensions recommandées**: 200x300 pixels ou plus
- **Format**: PNG avec transparence (RGBA)
- **Description**: Chevalier vu de dos, en pose de combat

#### Adversaire - Archer (Vue de Face)
- **Chemin**: `images/front/Archer.png`
- **Dimensions recommandées**: 200x300 pixels ou plus
- **Format**: PNG avec transparence (RGBA)
- **Description**: Archer vu de face, en pose de combat

### 2. Image de Fond

#### Arrière-plan du Combat
- **Chemin**: `images/other/bg.png`
- **Dimensions requises**: 1280x720 pixels
- **Format**: PNG
- **Description**: Décor de champ de bataille, arène de combat

## Structure des Dossiers

```
images/
├── back/
│   └── Chevalier.png          (À ajouter)
├── front/
│   └── Archer.png             (À ajouter)
├── other/
│   └── bg.png                 (À ajouter)
├── attacks/                   (Pour développement futur)
└── simple/                    (Pour développement futur)
```

## Résolution Minimale

Les images peuvent être de taille différente, elles seront redimensionnées automatiquement par le jeu à:
- Combattants: 200x300 pixels
- Fond: 1280x720 pixels (résolution de la fenêtre)

## Sources Possibles

Vous pouvez créer les images à partir de:
- Assets de Clash Royale (avec permission)
- Spritesheet RPG gratuits
- Outils de génération d'art (Aseprite, Krita, etc.)
- Assets 2D gratuits (OpenGameArt, itch.io, etc.)

## Dépannage

### Erreur: "No such file or directory"
- Vérifiez que les fichiers PNG sont dans les bons dossiers
- Vérifiez que les noms de fichiers correspondent exactement (sensible à la casse)

### Erreur: "cannot identify image file"
- Assurez-vous que les fichiers sont des images PNG valides
- Essayez de convertir l'image à PNG avec un outil approprié

### Les images ne s'affichent pas
- Vérifiez les dimensions recommandées
- Assurez-vous que l'image a une couche alpha (transparence)
