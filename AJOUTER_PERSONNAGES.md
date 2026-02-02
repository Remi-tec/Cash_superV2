# Ajouter un Nouveau Personnage

Guide complet pour ajouter un nouveau combattant au jeu Clash Royal.

## Processus en 3 Étapes

### Étape 1 : Ajouter les Données du Personnage dans stats.json

Le fichier `code/data/stats.json` contient tous les données des combattants.

#### Localisation du Fichier

```
code/data/stats.json
```

#### Format d'un Combattant

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
                },
                {
                    "nom": "Deuxième attaque",
                    "degat": 70,
                    "pp": 15,
                    "effet": "reduction_degat",
                    "critique": 10
                },
                {
                    "nom": "Troisième attaque",
                    "degat": 60,
                    "pp": 12,
                    "effet": "normal",
                    "critique": 8
                },
                {
                    "nom": "Quatrième attaque",
                    "degat": 100,
                    "pp": 8,
                    "effet": "poison",
                    "critique": 15
                }
            ]
        }
    }
}
```

**Important** : Chaque combattant DOIT avoir exactement 4 attaques.

#### Paramètres des Attaques

| Paramètre | Type | Description | Exemple |
|-----------|------|-------------|---------|
| **nom** | string | Nom de l'attaque | "Coup d'épée" |
| **degat** | number | Dégâts infligés | 45 |
| **pp** | number | Points de Pouvoir (limite d'utilisation) | 20 |
| **effet** | string | Type d'effet spécial | "normal" |
| **critique** | number | Pourcentage de chance de critique | 5 |

#### Valeurs de Référence pour les PV

- **Très Fort** : 800-1000 PV (ex: Chevalier)
- **Fort** : 600-700 PV (ex: Archer)
- **Équilibré** : 500-600 PV
- **Faible** : 300-400 PV (pour adversaire rapide)

#### Effets Disponibles

```
"normal"             → Attaque classique sans effet spécial
"reduction_degat"    → Réduit les dégâts reçus par 50% pendant 1 tour
"poison"             → Inflige 12.5% des PV max par tour
"brulure"            → Inflige 12.5% des PV max par tour
"paralysie"          → Réservé pour développement futur
"gelé"               → Réservé pour développement futur
"repousse"           → Repousse l'adversaire
"etourdi"            → Étourdissement réservé pour développement futur
```

#### Exemple Complet : Ajouter un Dragon

```json
{
    "fighters": {
        "Dragon": {
            "pv": 900,
            "attaques": [
                {
                    "nom": "Souffle de Feu",
                    "degat": 80,
                    "pp": 15,
                    "effet": "brulure",
                    "critique": 12
                },
                {
                    "nom": "Vol Piqué",
                    "degat": 60,
                    "pp": 18,
                    "effet": "normal",
                    "critique": 10
                },
                {
                    "nom": "Écailles de Cristal",
                    "degat": 0,
                    "pp": 10,
                    "effet": "reduction_degat",
                    "critique": 0
                },
                {
                    "nom": "Griffe Féroce",
                    "degat": 110,
                    "pp": 8,
                    "effet": "normal",
                    "critique": 20
                }
            ]
        }
    }
}
```

### Étape 2 : Ajouter l'Image du Personnage (Vue de Dos)

L'image du joueur (vue de dos du personnage).

#### Localisation

```
images/back/NomDuCombattant.png
```

#### Spécifications

- **Format** : PNG (avec ou sans transparence)
- **Nom** : Doit correspondre EXACTEMENT au nom dans stats.json
- **Exemple** : Pour "Dragon" → `images/back/Dragon.png`

#### Recommandations

- **Résolution** : Idéalement 256x384 pixels (sera redimensionné automatiquement)
- **Orientation** : Le personnage regarde vers la DROITE
- **Transparence** : Recommandée pour un meilleur rendu

### Étape 3 : Ajouter l'Image de l'Adversaire (Vue de Face)

L'image de l'adversaire (vue de face du personnage).

#### Localisation

```
images/front/NomDuCombattant.png
```

#### Spécifications

- **Format** : PNG (avec ou sans transparence)
- **Nom** : Doit correspondre EXACTEMENT au nom dans stats.json
- **Exemple** : Pour "Dragon" → `images/front/Dragon.png`

#### Recommandations

- **Résolution** : Idéalement 256x384 pixels (sera redimensionné automatiquement)
- **Orientation** : Le personnage regarde vers la GAUCHE
- **Transparence** : Recommandée pour un meilleur rendu

---

## Exemple Complet : Ajouter le Géant

### 1. Éditer `code/data/stats.json`

Ajouter à la section `"fighters"` :

```json
"Geant": {
    "pv": 1000,
    "attaques": [
        {
            "nom": "Coup de Massue",
            "degat": 90,
            "pp": 12,
            "effet": "normal",
            "critique": 8
        },
        {
            "nom": "Secousse Sismique",
            "degat": 70,
            "pp": 10,
            "effet": "repousse",
            "critique": 5
        },
        {
            "nom": "Armure de Pierre",
            "degat": 0,
            "pp": 15,
            "effet": "reduction_degat",
            "critique": 0
        },
        {
            "nom": "Tonnerre de Roche",
            "degat": 130,
            "pp": 6,
            "effet": "normal",
            "critique": 15
        }
    ]
}
```

### 2. Placer l'image du joueur

- Copier/créer l'image du Géant (vue de dos)
- Sauvegarder en PNG
- Placer dans : `images/back/Geant.png`

### 3. Placer l'image de l'adversaire

- Copier/créer l'image du Géant (vue de face)
- Sauvegarder en PNG
- Placer dans : `images/front/Geant.png`

### 4. Vérifier

Le personnage est maintenant disponible ! Vous pouvez:
- Le sélectionner comme joueur
- Le rencontrer comme adversaire

---

## Erreurs Courantes

### ❌ Les images ne s'affichent pas
- **Cause** : Le nom du fichier ne correspond pas au nom dans stats.json
- **Solution** : Vérifiez la casse et l'orthographe exactement

### ❌ Le jeu crash au démarrage
- **Cause** : Erreur de syntaxe dans stats.json
- **Solution** : Validez le JSON (utilisez jsonlint.com)

### ❌ L'attaque n'a pas d'effet
- **Cause** : Le type d'effet n'existe pas
- **Solution** : Utilisez uniquement les effets listés ci-dessus

### ❌ Le personnage a peu/trop de points de vie
- **Cause** : Valeur PV inadaptée au gameplay
- **Solution** : Ajustez entre 300-1000 PV selon la difficulté souhaitée

---

## Points à Retenir

✓ **Toujours** 4 attaques par personnage
✓ **Toujours** les mêmes noms dans stats.json et noms de fichiers
✓ **Vérifier** la syntaxe JSON après modification
✓ **Placer** une image vue de dos dans `images/back/`
✓ **Placer** une image vue de face dans `images/front/`
✓ **Format** PNG pour les images
✓ **Nom** du fichier correspond au nom du combattant
