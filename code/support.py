from settings import *
 
import json
import os

def folder_importer(*path):
    surfs = {}
    # Accepter à la fois (*path) et un seul argument
    if len(path) == 1 and os.path.isdir(path[0]):
        folder_path = path[0]
    else:
        folder_path = join(*path)
    
    # Charger uniquement les fichiers PNG
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith('.png'):
            full_path = join(folder_path, file_name)
            if os.path.isfile(full_path):
                img = pygame.image.load(full_path)
                try:
                    img = img.convert_alpha()
                except:
                    pass  # Si convert_alpha échoue, utiliser l'image brute
                surfs[file_name.split('.')[0]] = img
    return surfs

def audio_importer(*path):
    audio_dict = {}
    for folder_path, _, file_names in walk(join(*path)):
        for file_name in file_names:
            audio_dict[file_name.split('.')[0]] = pygame.mixer.Sound(join(folder_path, file_name))
    return audio_dict


def load_stats(filepath="data/stats.json"):
    """Charge les stats depuis un fichier JSON"""
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)