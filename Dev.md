# Guide de Développement - Clash Royal Pokémon

Ce fichier vous guide étape par étape dans le développement du jeu. Suivez les phases dans l'ordre et cochez les tâches accomplies.

---

## 📋 Phase 0 : Configuration de l'environnement

### Étape 0.1 : Installation des dépendances
**Fichier** : `requirements.txt`

**Objectif** : Installer les bibliothèques nécessaires

**Consignes** :
- [ ] Ajouter pygame dans requirements.txt
- [ ] Installer les dépendances avec pip
- [ ] Vérifier l'installation en important pygame dans Python

**Outils à utiliser** :
- pip (gestionnaire de paquets Python)
- Terminal/PowerShell

**Concepts à comprendre** :
- Gestion des dépendances Python
- Environnements virtuels (optionnel mais recommandé)

---

## 🎮 Phase 1 : Configuration de base du jeu

### Étape 1.1 : Fichier de configuration
**Fichier** : `src/utils/config.py`

**Objectif** : Définir les constantes globales du jeu

**Consignes** :
- [ ] Créer des constantes pour la résolution de l'écran (largeur, hauteur)
- [ ] Définir le FPS (images par seconde) du jeu
- [ ] Ajouter des constantes pour les couleurs principales (RGB)
- [ ] Définir le titre de la fenêtre

**Outils à utiliser** :
- Variables constantes en majuscules (convention Python)
- Tuples pour les couleurs RGB

**Concepts à comprendre** :
- Pourquoi centraliser les configurations
- Convention de nommage des constantes

---

### Étape 1.2 : Point d'entrée du jeu
**Fichier** : `main.py`

**Objectif** : Créer la boucle principale du jeu

**Consignes** :
- [ ] Initialiser pygame
- [ ] Créer une fenêtre de jeu avec les dimensions de config
- [ ] Créer une horloge pour contrôler le FPS
- [ ] Implémenter la boucle principale (game loop)
- [ ] Gérer la fermeture de la fenêtre (événement QUIT)
- [ ] Mettre à jour l'affichage et contrôler le FPS

**Outils à utiliser** :
- pygame.init()
- pygame.display.set_mode()
- pygame.time.Clock()
- Boucle while
- pygame.event.get()

**Concepts à comprendre** :
- Structure d'une game loop
- Gestion des événements
- FPS et delta time

---

## 🎨 Phase 2 : Système de gestion des écrans

### Étape 2.1 : Écran titre
**Fichier** : `src/screens/title_screen.py`

**Objectif** : Créer un écran d'accueil

**Consignes** :
- [ ] Créer une classe TitleScreen
- [ ] Ajouter une méthode pour afficher le titre du jeu
- [ ] Ajouter un bouton "Jouer" (rectangle cliquable)
- [ ] Gérer les clics de souris sur le bouton
- [ ] Retourner un état pour changer d'écran

**Outils à utiliser** :
- Classes Python
- pygame.draw (pour dessiner des formes)
- pygame.font (pour afficher du texte)
- pygame.mouse.get_pos()
- pygame.Rect.collidepoint()

**Concepts à comprendre** :
- POO : encapsulation dans des classes
- Détection de collision point/rectangle
- Machine à états (state management)

---

### Étape 2.2 : Gestionnaire d'écrans
**Fichier** : `main.py` (modification)

**Objectif** : Gérer les transitions entre écrans

**Consignes** :
- [ ] Créer une variable d'état (current_screen)
- [ ] Utiliser un dictionnaire ou des conditions pour switcher entre écrans
- [ ] Intégrer l'écran titre dans la boucle principale
- [ ] Tester la navigation

**Outils à utiliser** :
- Dictionnaires Python
- Conditions if/elif/else
- Imports de vos modules

**Concepts à comprendre** :
- Pattern State Machine
- Séparation des responsabilités

---

## 👤 Phase 3 : Système de personnages

### Étape 3.1 : Données des personnages
**Fichier** : `data/characters.json`

**Objectif** : Définir les stats des personnages Clash Royale

**Consignes** :
- [ ] Créer un JSON avec au moins 5 personnages
- [ ] Pour chaque personnage définir : nom, PV, attaque, défense, vitesse
- [ ] Ajouter éventuellement un type/élément

**Outils à utiliser** :
- Format JSON
- Éditeur de texte

**Concepts à comprendre** :
- Structure de données
- Format JSON (clés-valeurs)

**Exemple de structure** :
```
{
  "nom_personnage": {
    "nom": "...",
    "pv": 100,
    "attaque": 20,
    ...
  }
}
```

---

### Étape 3.2 : Classe Character de base
**Fichier** : `src/characters/character.py`

**Objectif** : Créer la classe mère pour tous les personnages

**Consignes** :
- [ ] Créer une classe Character avec __init__
- [ ] Définir les attributs : nom, pv_max, pv_actuel, attaque, défense, vitesse
- [ ] Créer une méthode pour recevoir des dégâts
- [ ] Créer une méthode pour vérifier si le personnage est KO
- [ ] Créer une méthode pour afficher les stats (optionnel)

**Outils à utiliser** :
- Classes Python
- __init__ (constructeur)
- self (référence à l'instance)
- Méthodes d'instance

**Concepts à comprendre** :
- POO : Classe et objets
- Encapsulation
- Méthodes vs fonctions

---

### Étape 3.3 : Chargement des données
**Fichier** : `src/characters/character_data.py`

**Objectif** : Charger les données JSON et créer des personnages

**Consignes** :
- [ ] Créer une fonction pour charger le fichier JSON
- [ ] Créer une fonction qui retourne un objet Character depuis le JSON
- [ ] Gérer les erreurs de fichier non trouvé

**Outils à utiliser** :
- Module json (json.load())
- Gestion des fichiers (open, with)
- try/except pour les erreurs

**Concepts à comprendre** :
- Lecture de fichiers
- Parsing JSON
- Gestion d'erreurs

---

### Étape 3.4 : Écran de sélection
**Fichier** : `src/ui/character_selection.py`

**Objectif** : Permettre au joueur de choisir son personnage

**Consignes** :
- [ ] Créer une classe CharacterSelection
- [ ] Afficher la liste des personnages disponibles
- [ ] Créer des boutons/cartes cliquables pour chaque personnage
- [ ] Afficher les stats du personnage survolé/sélectionné
- [ ] Retourner le personnage choisi

**Outils à utiliser** :
- pygame.draw pour les cartes
- pygame.font pour le texte
- Boucles for pour parcourir les personnages
- Événements de clic

**Concepts à comprendre** :
- Itération sur des collections
- Interface utilisateur
- Feedback visuel

---

## ⚔️ Phase 4 : Système de combat

### Étape 4.1 : Définir les attaques
**Fichier** : `data/moves.json`

**Objectif** : Créer une liste d'attaques utilisables

**Consignes** :
- [ ] Créer au moins 10 attaques différentes
- [ ] Pour chaque attaque : nom, puissance, type (physique/spécial)
- [ ] Optionnel : précision, effets spéciaux

**Outils à utiliser** :
- Format JSON

**Concepts à comprendre** :
- Game design : équilibrage

---

### Étape 4.2 : Classe Move
**Fichier** : `src/combat/moves.py`

**Objectif** : Représenter une attaque

**Consignes** :
- [ ] Créer une classe Move
- [ ] Définir les attributs (nom, puissance, type)
- [ ] Créer une fonction pour charger les attaques depuis JSON
- [ ] Créer une méthode pour calculer les dégâts

**Outils à utiliser** :
- Classes Python
- Formules mathématiques

**Concepts à comprendre** :
- Calcul de dégâts (attaque vs défense)
- Randomisation (random.randint pour les critiques)

---

### Étape 4.3 : Logique de combat
**Fichier** : `src/combat/battle.py`

**Objectif** : Gérer le déroulement d'un combat

**Consignes** :
- [ ] Créer une classe Battle
- [ ] Initialiser avec deux personnages (joueur vs ennemi)
- [ ] Créer une méthode pour gérer un tour de combat
- [ ] Alterner les tours selon la vitesse
- [ ] Vérifier les conditions de victoire/défaite
- [ ] Retourner le résultat du combat

**Outils à utiliser** :
- Classes
- Conditions
- Comparaisons

**Concepts à comprendre** :
- Tour par tour
- Système de priorité/vitesse
- Conditions de fin

---

### Étape 4.4 : IA ennemie basique
**Fichier** : `src/combat/battle_ai.py`

**Objectif** : Faire jouer l'adversaire automatiquement

**Consignes** :
- [ ] Créer une fonction qui choisit une attaque aléatoirement
- [ ] Optionnel : ajouter de la stratégie (choisir l'attaque la plus forte)

**Outils à utiliser** :
- random.choice()
- Listes

**Concepts à comprendre** :
- IA basique
- Prise de décision algorithmique

---

## 🖼️ Phase 5 : Interface de combat

### Étape 5.1 : HUD de combat
**Fichier** : `src/ui/hud.py`

**Objectif** : Afficher les informations pendant le combat

**Consignes** :
- [ ] Créer une classe HUD
- [ ] Afficher les PV des deux combattants (barres de vie)
- [ ] Afficher les noms
- [ ] Créer une zone de texte pour les messages de combat

**Outils à utiliser** :
- pygame.draw.rect (pour les barres)
- pygame.font.render (pour le texte)
- Proportions (PV actuel / PV max)

**Concepts à comprendre** :
- UI/UX : feedback visuel
- Calculs de proportions

---

### Étape 5.2 : Interface des attaques
**Fichier** : `src/ui/battle_ui.py`

**Objectif** : Permettre au joueur de choisir ses actions

**Consignes** :
- [ ] Créer une classe BattleUI
- [ ] Afficher les 4 attaques disponibles dans des boutons
- [ ] Gérer les clics sur les attaques
- [ ] Retourner l'attaque choisie

**Outils à utiliser** :
- pygame.Rect pour les zones cliquables
- Événements de souris

**Concepts à comprendre** :
- Interface utilisateur interactive
- Callback / retour d'information

---

### Étape 5.3 : Écran de combat complet
**Fichier** : `src/screens/battle_screen.py`

**Objectif** : Assembler tous les éléments du combat

**Consignes** :
- [ ] Créer une classe BattleScreen
- [ ] Intégrer le HUD
- [ ] Intégrer le BattleUI
- [ ] Intégrer la logique de Battle
- [ ] Gérer le déroulement : tour joueur → tour ennemi → vérifier fin
- [ ] Afficher les messages d'action
- [ ] Rediriger vers l'écran de victoire/défaite

**Outils à utiliser** :
- Composition de classes
- Machine à états pour les phases du combat

**Concepts à comprendre** :
- Architecture logicielle
- Flow d'un combat complet

---

## 🏆 Phase 6 : Écrans de fin

### Étape 6.1 : Écran victoire/défaite
**Fichier** : `src/screens/victory_screen.py`

**Objectif** : Afficher le résultat du combat

**Consignes** :
- [ ] Créer une classe VictoryScreen
- [ ] Afficher "VICTOIRE !" ou "DÉFAITE..."
- [ ] Ajouter un bouton "Recommencer"
- [ ] Ajouter un bouton "Menu principal"
- [ ] Gérer les clics

**Outils à utiliser** :
- pygame.font (texte grand format)
- Boutons cliquables

**Concepts à comprendre** :
- Feedback utilisateur
- Navigation

---

## 🎵 Phase 7 : Assets et polish (Optionnel)

### Étape 7.1 : Chargeur d'assets
**Fichier** : `src/utils/assets_loader.py`

**Objectif** : Centraliser le chargement des images/sons

**Consignes** :
- [ ] Créer une fonction pour charger une image
- [ ] Créer une fonction pour charger un son
- [ ] Gérer les erreurs si le fichier n'existe pas
- [ ] Créer un dictionnaire cache pour éviter de charger plusieurs fois

**Outils à utiliser** :
- pygame.image.load()
- pygame.mixer.Sound()
- Dictionnaires Python

**Concepts à comprendre** :
- Optimisation (cache)
- Gestion des ressources

---

### Étape 7.2 : Système d'animations
**Fichier** : `src/utils/animation.py`

**Objectif** : Créer des animations simples

**Consignes** :
- [ ] Créer une classe Animation
- [ ] Gérer une liste de frames (images)
- [ ] Créer une méthode update() pour changer de frame
- [ ] Créer une méthode get_current_frame()

**Outils à utiliser** :
- Listes d'images
- Compteurs et modulo (%)

**Concepts à comprendre** :
- Animation par sprite sheets
- Timing et frames

---

### Étape 7.3 : Intégration des sprites
**Consignes** :
- [ ] Trouver ou créer des sprites pour les personnages
- [ ] Les placer dans `assets/images/characters/`
- [ ] Modifier Character pour afficher un sprite au lieu d'un rectangle
- [ ] Ajouter des animations d'attaque (optionnel)

**Outils à utiliser** :
- Sites de sprites gratuits (OpenGameArt, itch.io)
- GIMP/Photoshop pour éditer

**Concepts à comprendre** :
- Formats d'image (PNG avec transparence)
- Échelle et résolution

---

### Étape 7.4 : Sons et musiques
**Consignes** :
- [ ] Trouver des musiques libres de droits
- [ ] Ajouter une musique de fond pour le menu
- [ ] Ajouter une musique pour les combats
- [ ] Ajouter des effets sonores (coups, victoire)

**Outils à utiliser** :
- pygame.mixer.music pour les musiques
- pygame.mixer.Sound pour les effets
- Sites : freesound.org, incompetech.com

**Concepts à comprendre** :
- Différence musique vs effets sonores
- Formats audio (MP3, OGG, WAV)

---

## ✨ Phase 8 : Améliorations et features supplémentaires

### Idées d'améliorations :
- [ ] Système de niveaux pour les personnages
- [ ] Plusieurs combats d'affilée (mode campagne)
- [ ] Système de types avec avantages/faiblesses
- [ ] Attaques avec effets de statut (poison, paralysie)
- [ ] Menu de pause pendant le combat
- [ ] Sauvegarde de progression
- [ ] Écran de statistiques
- [ ] Mode multijoueur local (2 joueurs sur le même PC)

---

## 📝 Bonnes pratiques à suivre

### Pendant tout le développement :

1. **Tester régulièrement**
   - Testez chaque fonctionnalité dès qu'elle est implémentée
   - Ne passez pas à l'étape suivante si la précédente ne fonctionne pas

2. **Commenter votre code**
   - Ajoutez des docstrings aux classes et fonctions
   - Commentez les parties complexes

3. **Nommage clair**
   - Variables : snake_case (ex: `vie_actuelle`)
   - Classes : PascalCase (ex: `CharacterSelection`)
   - Constantes : UPPERCASE (ex: `SCREEN_WIDTH`)

4. **Git et versioning**
   - Commitez après chaque étape importante
   - Messages de commit clairs

5. **Gestion d'erreurs**
   - Utilisez try/except pour les opérations risquées
   - Affichez des messages d'erreur utiles

---

## 🎓 Ressources utiles

### Documentation :
- Documentation officielle Pygame : https://www.pygame.org/docs/
- Tutoriels Pygame : https://www.youtube.com/results?search_query=pygame+tutorial

### Concepts à approfondir :
- Programmation orientée objet (POO)
- Game loops et delta time
- Gestion d'événements
- State machines
- Sprites et animations

---

## ✅ Checklist de progression

Cochez au fur et à mesure :

- [ ] Phase 0 : Configuration ✓
- [ ] Phase 1 : Base du jeu ✓
- [ ] Phase 2 : Écrans ✓
- [ ] Phase 3 : Personnages ✓
- [ ] Phase 4 : Combat ✓
- [ ] Phase 5 : Interface ✓
- [ ] Phase 6 : Fin de jeu ✓
- [ ] Phase 7 : Polish ✓
- [ ] Phase 8 : Améliorations ✓

---

**Bon courage pour votre développement ! 🚀**