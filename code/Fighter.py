from settings import *
import random

class Fighters():
    """Classe de base pour les combattants"""
    def __init__(self, name, fighter_data):
        self.name = name
        self.max_pv = fighter_data["pv"]
        self.pv = fighter_data["pv"]
        self.max_pp = fighter_data["pp"]
        self.pp = fighter_data["pp"]
        self.attaques = fighter_data["attaques"]
        self.effects = []  # Liste des effets actifs (brûlure, paralysie, etc.)
        self.defense_active = False
    
    def get_data(self):
        return {
            "name": self.name,
            "pv": self.pv,
            "max_pv": self.max_pv,
            "attaques": self.attaques,
            "pp": self.pp,
            "effects": self.effects
        }


class Fighter(pygame.sprite.Sprite, Fighters):
    """Le combattant joueur"""
    def __init__(self, name, surface, fighter_data, width=200, height=300):
        pygame.sprite.Sprite.__init__(self)
        Fighters.__init__(self, name, fighter_data)
        self.image = pygame.transform.scale(surface, (width, height))
        self.rect = self.image.get_rect(bottomleft=(100, WINDOW_HEIGHT - 150))
        self.surface = surface
        self.width = width
        self.height = height

    def update(self, dt):
        pass


class Opponent(pygame.sprite.Sprite, Fighters):
    """L'adversaire (bot)"""
    def __init__(self, name, surface, fighter_data, groups=None, width=200, height=300):
        pygame.sprite.Sprite.__init__(self)
        Fighters.__init__(self, name, fighter_data)
        self.image = pygame.transform.scale(surface, (width, height))
        self.rect = self.image.get_rect(bottomright=(WINDOW_WIDTH - 100, WINDOW_HEIGHT - 150))
        self.surface = surface
        self.width = width
        self.height = height
        if groups:
            self.add(groups)

    def update(self, dt):
        pass