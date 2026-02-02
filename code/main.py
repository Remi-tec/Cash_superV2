"""
Jeu de combat simple avec Pygame
"""

import pygame
import sys
from settings import *
from support import *
from timer import Timer
from Fighter import Fighter, Opponent
from battle import Battle
from hud import BattleHUD



class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Clash Game - Combat")
        self.clock = pygame.time.Clock()
        self.running = True
        print("1. Initialisation pygame OK")
        
        self.import_assets()
        print(f"2. Assets importés: {len(self.back_surfs)} back, {len(self.front_surfs)} front, {len(self.bg_surfs)} other")

        # Group
        self.all_sprites = pygame.sprite.Group()

        # Initialize timers et variables
        self.opponent_attack_timer = Timer(2000, func=self.execute_opponent_attack)
        self.selected_attack = 0
        self.battle = None
        self.game_over_sfx_played = False
        
        # Initialize fighters
        self.setup_battle()
        print("3. Battle setup OK")
        
        # HUD
        self.hud = BattleHUD(self.display_surface)
        print("4. HUD créé")

    def setup_battle(self):
        """Configure une nouvelle bataille"""
        try:
            self.game_over_sfx_played = False
            # Relancer la musique
            pygame.mixer.music.play(-1)
            # Joueur
            player_data = FIGHTER_CONFIG["Chevalier"]
            self.player_fighter = Fighter("Chevalier", self.back_surfs["Chevalier"], player_data)
            self.all_sprites.add(self.player_fighter)
            
            # Adversaire
            opponent_data = FIGHTER_CONFIG["Archer"]
            self.opponent = Opponent("Archer", self.front_surfs["Archer"], opponent_data, self.all_sprites)
            
            # Initialiser le combat
            self.battle = Battle(self.player_fighter, self.opponent)
            self.selected_attack = 0
        except Exception as e:
            print(f"Erreur lors de l'initialisation: {e}")
            import traceback
            traceback.print_exc()
            raise

    def import_assets(self):
        """Importer les ressources du jeu"""
        # Aller au répertoire parent pour accéder aux images
        import os
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        self.back_surfs = folder_importer(os.path.join(parent_dir, "images", "back"))
        self.front_surfs = folder_importer(os.path.join(parent_dir, "images", "front"))
        self.bg_surfs = folder_importer(os.path.join(parent_dir, "images", "other"))

        # Charger les bruitages (SFX)
        sfx_dir = os.path.join(parent_dir, "audio", "sfx")
        if os.path.exists(sfx_dir):
            self.sfx = audio_importer(sfx_dir)
            for sound in self.sfx.values():
                sound.set_volume(1.5)
        else:
            self.sfx = {}

        # Charger la musique
        music_path = os.path.join(parent_dir, "audio", "music.mp3")
        if os.path.exists(music_path):
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1)  # -1 = boucle infinie
            pygame.mixer.music.set_volume(0.2)  # Volume à 20%
            print("5. Musique chargée et lancée en boucle")

    def play_sfx(self, name):
        """Jouer un bruitage si présent"""
        sound = self.sfx.get(name)
        if sound:
            sound.play()
    
    def handle_events(self):
        """Gère les événements"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                # Navigation entre les boutons
                if event.key == pygame.K_LEFT and self.selected_attack > 0:
                    self.selected_attack -= 1
                elif event.key == pygame.K_RIGHT and self.selected_attack < 3:
                    self.selected_attack += 1
                elif event.key == pygame.K_UP and self.selected_attack >= 2:
                    self.selected_attack -= 2
                elif event.key == pygame.K_DOWN and self.selected_attack < 2:
                    self.selected_attack += 2
                
                # Confirmer l'attaque
                elif event.key == pygame.K_RETURN and not self.battle.game_over:
                    if self.battle.current_turn == "player":
                        if self.battle.player_attack(self.selected_attack):
                            self.play_sfx("explosion")
                            self.opponent_attack_timer.activate()
                
                # Recommencer après game over
                elif event.key == pygame.K_SPACE and self.battle.game_over:
                    self.all_sprites.empty()
                    self.setup_battle()
    
    def execute_opponent_attack(self):
        """Exécute l'attaque de l'adversaire"""
        if not self.battle.game_over:
            self.battle.opponent_attack()
            self.play_sfx("explosion")
    
    def update(self, dt):
        """Met à jour l'état du jeu"""
        self.all_sprites.update(dt)
        self.opponent_attack_timer.update()
    
    def draw(self):
        """Affiche le jeu"""
        # Fond
        self.display_surface.blit(self.bg_surfs["bg"], (0, 0))
        
        # Combattants
        self.all_sprites.draw(self.display_surface)
        
        # HUD
        turn_name = "joueur" if self.battle.current_turn == "player" else "adversaire"
        self.hud.draw_turn_indicator(turn_name)
        
        # Infos des combattants
        self.hud.draw_fighter_info(self.player_fighter, "left")
        self.hud.draw_fighter_info(self.opponent, "right")
        
        # Boutons d'attaque (seulement si c'est le tour du joueur et pas de game over)
        if not self.battle.game_over:
            self.hud.draw_attack_buttons(
                self.player_fighter.attaques,
                self.player_fighter.pp,
                self.selected_attack
            )
        
        # Log de combat
        self.hud.draw_battle_log(self.battle.battle_log)
        
        # Écran de fin
        if self.battle.game_over:
            winner = "joueur" if self.battle.winner == self.player_fighter.name else "adversaire"
            self.hud.draw_game_over(winner)
            if winner == "adversaire" and not self.game_over_sfx_played:
                pygame.mixer.music.stop()
                self.play_sfx("gameover")
                self.game_over_sfx_played = True
            elif winner == "joueur" and not self.game_over_sfx_played:
                pygame.mixer.music.stop()
                self.play_sfx("win")
                self.game_over_sfx_played = True
        
        pygame.display.flip()
    
    def run(self):
        """Boucle principale du jeu"""
        while self.running:
            dt = self.clock.tick(60) / 1000
            
            self.handle_events()
            self.update(dt)
            self.draw()
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
