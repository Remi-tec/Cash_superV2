#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DÉMARRAGE RAPIDE - Clash Game
Suivez ces étapes pour lancer le jeu
"""

import os
import sys

def print_header():
    """Affiche un en-tête"""
    print("\n" + "=" * 70)
    print(" " * 15 + "CLASH GAME - GUIDE DE DÉMARRAGE RAPIDE")
    print("=" * 70 + "\n")

def check_requirements():
    """Vérifie si pygame est installé"""
    print("1️⃣  VÉRIFICATION DES DÉPENDANCES")
    print("-" * 70)
    
    try:
        import pygame
        print("✅ Pygame est installé")
        return True
    except ImportError:
        print("❌ Pygame n'est pas installé!")
        print("\n   Pour installer pygame, exécutez:")
        print("   > pip install pygame")
        print("\n   Puis relancez ce script.")
        return False

def check_images():
    """Vérifie la présence des images"""
    print("\n2️⃣  VÉRIFICATION DES IMAGES")
    print("-" * 70)
    
    images = [
        ("../images/back/Chevalier.png", "Image du Chevalier"),
        ("../images/front/Archer.png", "Image de l'Archer"),
        ("../images/other/bg.png", "Fond du combat")
    ]
    
    all_present = True
    for path, desc in images:
        if os.path.exists(path):
            print(f"✅ {desc}")
        else:
            print(f"❌ {desc} - MANQUANT")
            all_present = False
    
    if not all_present:
        print("\n⚠️  ATTENTION: Des images manquent!")
        print("   Consultez: ../images/README_IMAGES.md")
        return False
    
    return True

def check_data():
    """Vérifie les fichiers de données"""
    print("\n3️⃣  VÉRIFICATION DES DONNÉES")
    print("-" * 70)
    
    if os.path.exists("data/stats.json"):
        print("✅ Fichier data/stats.json trouvé")
        try:
            import json
            with open("data/stats.json", 'r', encoding='utf-8') as f:
                data = json.load(f)
            fighters = list(data.get("fighters", {}).keys())
            print(f"   Combattants: {', '.join(fighters)}")
            return True
        except Exception as e:
            print(f"❌ Erreur dans stats.json: {e}")
            return False
    else:
        print("❌ Fichier data/stats.json MANQUANT")
        return False

def main():
    """Fonction principale"""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    print_header()
    
    # Vérifications
    req_ok = check_requirements()
    if not req_ok:
        print("\n" + "=" * 70)
        return 1
    
    img_ok = check_images()
    data_ok = check_data()
    
    # Résultat
    print("\n" + "=" * 70)
    if data_ok:
        print("✅ CONFIGURATION OK - Prêt à lancer!")
        print("\nPour lancer le jeu, exécutez:")
        print("   > python main.py")
        print("\n" + "=" * 70)
        return 0
    else:
        print("❌ CONFIGURATION INCOMPLÈTE")
        if not img_ok:
            print("\nImages manquantes!")
            print("Consultez: ../images/README_IMAGES.md")
        print("\n" + "=" * 70)
        return 1

if __name__ == "__main__":
    sys.exit(main())
