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
        self.selected_home = 0
        self.confirm_quit_active = False
        self.confirm_quit_selected = 0  # 0 = Oui, 1 = Non
        self.team = []  # Liste des fighters dans l'équipe (max 6)
        self.team_menu_active = False
        self.selected_fighter = 0  # Index du fighter sélectionné dans le menu équipe
        self.team_view_mode = "available"  # "available" pour voir les fighters disponibles, "team" pour voir l'équipe
        self.team_fighters = {}  # Dict pour stocker les instances des fighters d'équipe avec leurs PV et PP
        self.player_fighter = None
        self.battle = None
        self.game_over_sfx_played = False
        self.app_state = "home"  # "home" ou "battle"
        self.home_menu_options = ["Clashdex", "Combat", "Equipe", "Inventaire", "Boutique", "Quitter"]
        self.clashdex_active = False  # Pour afficher le popup Clashdex en combat
        self.home_clashdex_active = False  # Pour afficher le popup Clashdex à l'accueil
        self.home_clashdex_index = 0  # Index du fighter affiché dans le Clashdex d'accueil
        
        # HUD
        self.hud = BattleHUD(self.display_surface)
        print("4. HUD créé")

    def setup_battle(self):
        """Configure une nouvelle bataille"""
        try:
            import random
            self.game_over_sfx_played = False
            self.all_sprites.empty()
            # Relancer la musique
            pygame.mixer.music.play(-1)
            
            # Créer tous les fighters de l'équipe et les stocker
            self.team_fighters = {}
            if self.team:
                for fighter_name in self.team:
                    fighter_data = FIGHTER_CONFIG[fighter_name]
                    fighter = Fighter(fighter_name, self.back_surfs[fighter_name], fighter_data)
                    self.team_fighters[fighter_name] = fighter
                first_fighter = self.team[0]
            else:
                first_fighter = "Chevalier"
                fighter_data = FIGHTER_CONFIG[first_fighter]
                fighter = Fighter(first_fighter, self.back_surfs[first_fighter], fighter_data)
                self.team_fighters[first_fighter] = fighter
            
            # Utiliser le premier fighter comme joueur
            self.player_fighter = self.team_fighters[first_fighter]
            self.all_sprites.add(self.player_fighter)
            
            # Créer une équipe aléatoire pour l'adversaire (1 à 6 fighters)
            # Uniquement parmi les fighters qui ont une image front
            available_opponents = [name for name in FIGHTER_CONFIG.keys() if name in self.front_surfs]
            opponent_team_size = random.randint(1, min(6, len(available_opponents)))
            self.opponent_team = random.sample(available_opponents, opponent_team_size)
            
            # Créer tous les fighters adverses et les stocker
            self.opponent_fighters = {}
            for fighter_name in self.opponent_team:
                fighter_data = FIGHTER_CONFIG[fighter_name]
                # Ne PAS ajouter au groupe all_sprites lors de la création
                fighter = Opponent(fighter_name, self.front_surfs[fighter_name], fighter_data, groups=None)
                self.opponent_fighters[fighter_name] = fighter
            
            # Utiliser le premier fighter adverse et l'ajouter au groupe
            first_opponent = self.opponent_team[0]
            self.opponent = self.opponent_fighters[first_opponent]
            self.all_sprites.add(self.opponent)
            
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
                if self.team_menu_active:
                    # Menu équipe (prioritaire)
                    fighters_list = list(FIGHTER_CONFIG.keys())
                    
                    if event.key == pygame.K_RIGHT and self.team_view_mode == "available":
                        self.team_view_mode = "team"
                        self.selected_fighter = min(self.selected_fighter, len(self.team) - 1) if self.team else 0
                    elif event.key == pygame.K_LEFT and self.team_view_mode == "team":
                        self.team_view_mode = "available"
                    
                    if self.team_view_mode == "available":
                        # Navigation dans les fighters disponibles
                        if event.key == pygame.K_UP and self.selected_fighter > 0:
                            self.selected_fighter -= 1
                            self.play_sfx("navigation")
                        elif event.key == pygame.K_DOWN and self.selected_fighter + 1 < len(fighters_list):
                            self.selected_fighter += 1
                            self.play_sfx("navigation")
                        
                        # Ajouter à l'équipe
                        elif event.key == pygame.K_RETURN:
                            fighter_name = fighters_list[self.selected_fighter]
                            if len(self.team) < 6 and fighter_name not in self.team:
                                self.team.append(fighter_name)
                                self.play_sfx("selection")
                    
                    else:  # team_view_mode == "team"
                        # Navigation dans l'équipe
                        if event.key == pygame.K_UP and self.selected_fighter > 0:
                            self.selected_fighter -= 1
                            self.play_sfx("navigation")
                        elif event.key == pygame.K_DOWN and self.selected_fighter + 1 < len(self.team):
                            self.selected_fighter += 1
                            self.play_sfx("navigation")
                        
                        # Retirer de l'équipe
                        elif event.key == pygame.K_RETURN:
                            if self.selected_fighter < len(self.team):
                                self.team.pop(self.selected_fighter)
                                if self.selected_fighter >= len(self.team) and self.selected_fighter > 0:
                                    self.selected_fighter -= 1
                                self.play_sfx("selection")
                    
                    # Fermer le menu équipe
                    if event.key == pygame.K_ESCAPE:
                        self.team_menu_active = False
                
                elif self.app_state == "home":
                    if self.home_clashdex_active:
                        # Navigation dans le Clashdex d'accueil
                        fighters_list = list(FIGHTER_CONFIG.keys())
                        if event.key == pygame.K_LEFT and self.home_clashdex_index > 0:
                            self.home_clashdex_index -= 1
                            self.play_sfx("navigation")
                        elif event.key == pygame.K_RIGHT and self.home_clashdex_index + 1 < len(fighters_list):
                            self.home_clashdex_index += 1
                            self.play_sfx("navigation")
                        elif event.key == pygame.K_ESCAPE:
                            self.home_clashdex_active = False
                            self.play_sfx("selection")
                    else:
                        # Navigation menu accueil (colonne unique)
                        if event.key == pygame.K_UP and self.selected_home > 0:
                            self.selected_home -= 1
                            self.play_sfx("navigation")
                        elif event.key == pygame.K_DOWN and self.selected_home + 1 < len(self.home_menu_options):
                            self.selected_home += 1
                            self.play_sfx("navigation")
                        
                        # Confirmer la sélection (menu accueil)
                        elif event.key == pygame.K_RETURN:
                            self.play_sfx("selection")
                            selected_option = self.home_menu_options[self.selected_home]
                            if selected_option == "Combat":
                                self.app_state = "battle"
                                self.hud.menu_state = "main"
                                self.selected_attack = 0
                                self.setup_battle()
                            elif selected_option == "Quitter":
                                self.running = False
                            elif selected_option == "Equipe":
                                self.team_menu_active = True
                                self.selected_fighter = 0
                                self.team_view_mode = "available"
                            elif selected_option == "Clashdex":
                                self.home_clashdex_active = True
                                self.home_clashdex_index = 0
                
                elif self.app_state == "battle":
                    # Fenêtre de confirmation (prioritaire)
                    if self.confirm_quit_active:
                        if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                            self.confirm_quit_selected = 1 - self.confirm_quit_selected
                            self.play_sfx("navigation")
                        elif event.key == pygame.K_RETURN:
                            self.play_sfx("selection")
                            if self.confirm_quit_selected == 0:  # Oui
                                self.app_state = "home"
                                self.all_sprites.empty()
                                self.battle = None
                                self.player_fighter = None
                                self.opponent = None
                                self.opponent_attack_timer.deactivate()
                                self.selected_home = 0
                                self.hud.menu_state = "main"
                                self.confirm_quit_active = False
                                pygame.mixer.music.play(-1)
                            else:  # Non
                                self.confirm_quit_active = False
                        elif event.key == pygame.K_ESCAPE:
                            self.confirm_quit_active = False
                    else:
                        # Navigation et actions (menu combat)
                        if event.key == pygame.K_UP and self.hud.menu_state == "switch" and self.selected_attack > 0:
                            # Chercher le fighter vivant précédent
                            new_index = self.selected_attack - 1
                            while new_index >= 0 and self.team_fighters[self.team[new_index]].pv <= 0:
                                new_index -= 1
                            if new_index >= 0:
                                self.selected_attack = new_index
                                self.play_sfx("navigation")
                        elif event.key == pygame.K_DOWN and self.hud.menu_state == "switch" and self.selected_attack + 1 < len(self.team):
                            # Chercher le fighter vivant suivant
                            new_index = self.selected_attack + 1
                            while new_index < len(self.team) and self.team_fighters[self.team[new_index]].pv <= 0:
                                new_index += 1
                            if new_index < len(self.team):
                                self.selected_attack = new_index
                                self.play_sfx("navigation")
                        elif event.key == pygame.K_LEFT and self.hud.menu_state != "switch" and self.selected_attack > 0:
                            self.selected_attack -= 1
                            self.play_sfx("navigation")
                        elif event.key == pygame.K_RIGHT and self.hud.menu_state != "switch" and self.selected_attack < 3:
                            self.selected_attack += 1
                            self.play_sfx("navigation")
                        elif event.key == pygame.K_UP and self.hud.menu_state != "switch" and self.selected_attack >= 2:
                            self.selected_attack -= 2
                            self.play_sfx("navigation")
                        elif event.key == pygame.K_DOWN and self.hud.menu_state != "switch" and self.selected_attack < 2:
                            self.selected_attack += 2
                            self.play_sfx("navigation")
                        
                        # Confirmer la sélection
                        elif event.key == pygame.K_RETURN and not self.battle.game_over:
                            if self.hud.menu_state == "main":
                                self.play_sfx("selection")
                                # Menu principal : sélectionner une option (autorisé tout le temps)
                                if self.selected_attack == 0:  # Attaques
                                    self.hud.menu_state = "attacks"
                                    self.selected_attack = 0
                                elif self.selected_attack == 2:  # Switch
                                    if len(self.team) > 1:  # Au moins 1 autre fighter dans l'équipe
                                        self.hud.menu_state = "switch"
                                        self.selected_attack = 0
                                elif self.selected_attack == 3:  # Clashdex
                                    self.clashdex_active = True
                                # Autres options à implémenter plus tard
                            elif self.hud.menu_state == "attacks":
                                # Menu attaques : lancer l'attaque (seulement si c'est le tour du joueur)
                                if self.battle.current_turn == "player":
                                    self.play_sfx("selection")
                                    if self.battle.player_attack(self.selected_attack):
                                        self.play_sfx("explosion")
                                        # Vérifier si l'adversaire est KO
                                        if self.opponent.pv <= 0:
                                            self.check_opponent_ko()
                                        else:
                                            self.opponent_attack_timer.deactivate()
                                            self.opponent_attack_timer.activate()
                                        self.hud.menu_state = "main"
                                        self.selected_attack = 0
                            elif self.hud.menu_state == "switch":
                                # Switch de fighter (seulement si c'est le tour du joueur)
                                if self.battle.current_turn == "player":
                                    fighter_name = self.team[self.selected_attack]
                                    # Vérifier que le fighter est vivant et n'est pas l'actuel
                                    if self.team_fighters[fighter_name].pv > 0 and fighter_name != self.player_fighter.name:
                                        self.play_sfx("selection")
                                        # Retirer l'ancien fighter
                                        self.all_sprites.remove(self.player_fighter)
                                        # Utiliser le fighter stocké avec ses PV et PP actuels
                                        self.player_fighter = self.team_fighters[fighter_name]
                                        self.all_sprites.add(self.player_fighter)
                                        # Mettre à jour la bataille avec le nouveau fighter
                                        self.battle.player = self.player_fighter
                                        # Passer immédiatement au tour de l'adversaire
                                        self.battle.current_turn = "opponent"
                                        self.hud.menu_state = "main"
                                        self.selected_attack = 0
                                        # Le switch compte comme un tour, donc c'est maintenant au tour de l'adversaire
                                        self.opponent_attack_timer.deactivate()
                                        self.opponent_attack_timer.activate()
                                    else:
                                        self.play_sfx("error")
                        
                        # Retour au menu principal / confirmation de sortie
                        elif event.key == pygame.K_ESCAPE and not self.battle.game_over:
                            if self.clashdex_active:
                                self.clashdex_active = False
                            elif self.hud.menu_state == "attacks":
                                self.hud.menu_state = "main"
                                self.selected_attack = 0
                            elif self.hud.menu_state == "switch":
                                self.hud.menu_state = "main"
                                self.selected_attack = 0
                            elif self.hud.menu_state == "main":
                                self.confirm_quit_active = True
                                self.confirm_quit_selected = 1  # défaut sur "Non"
                                self.play_sfx("selection")
                        
                        # Passer son tour
                        elif event.key == pygame.K_TAB and not self.battle.game_over:
                            if self.battle.current_turn == "player":
                                if self.battle.skip_turn():
                                    self.opponent_attack_timer.deactivate()
                                    self.opponent_attack_timer.activate()
                                    self.hud.menu_state = "main"
                                    self.selected_attack = 0
                        
                        # Recommencer après game over
                        elif event.key == pygame.K_SPACE and self.battle.game_over:
                            self.all_sprites.empty()
                            self.setup_battle()
                            self.hud.menu_state = "main"
                            self.selected_attack = 0
                        
                        # Retour à l'accueil après game over
                        elif event.key == pygame.K_ESCAPE and self.battle.game_over:
                            self.app_state = "home"
                            self.all_sprites.empty()
                            self.battle = None
                            self.player_fighter = None
                            self.opponent = None
                            self.opponent_attack_timer.deactivate()
                            self.selected_home = 0
                            self.hud.menu_state = "main"
                            pygame.mixer.music.play(-1)
    
    def check_opponent_no_pp(self):
        """Vérifie si l'adversaire n'a plus de PP et gère le switch"""
        # Vérifier si le fighter actuel a encore des PP
        if self.opponent.pp > 0:
            return
        
        # Sauvegarder le nom de l'ancien fighter
        old_fighter_name = self.opponent.name
        
        # Ajouter un message indiquant le manque de PP
        self.battle.battle_log.append(f"{old_fighter_name} n'a plus de PP!")
        
        # Chercher un fighter vivant avec des PP (dans toute l'équipe)
        next_opponent = None
        for fighter_name in self.opponent_team:
            if fighter_name != old_fighter_name:
                fighter = self.opponent_fighters[fighter_name]
                if fighter.pv > 0 and fighter.pp > 0:
                    next_opponent = fighter_name
                    break
        
        # Si aucun fighter avec PP trouvé, chercher le premier vivant disponible
        if not next_opponent:
            for fighter_name in self.opponent_team:
                if fighter_name != old_fighter_name:
                    fighter = self.opponent_fighters[fighter_name]
                    if fighter.pv > 0:
                        next_opponent = fighter_name
                        break
        
        if next_opponent:
            # Il reste des fighters adverses, switch automatique
            self.all_sprites.remove(self.opponent)
            self.opponent = self.opponent_fighters[next_opponent]
            self.all_sprites.add(self.opponent)
            self.battle.opponent = self.opponent
            self.battle.battle_log.append(f"{next_opponent} entre en combat!")
            print(f"DEBUG: Switch effectué de {old_fighter_name} vers {next_opponent}")
        else:
            # Vérifier s'il reste des fighters vivants
            alive_fighters = [f for f in self.opponent_team if self.opponent_fighters[f].pv > 0]
            
            if alive_fighters:
                # Il y a des fighters vivants mais aucun n'a de PP
                self.battle.game_over = True
                self.battle.winner = self.player_fighter.name
                self.battle.battle_log.append(f"Victoire! L'équipe adverse n'a plus de PP!")
                print(f"DEBUG: Victoire - Aucun fighter avec PP parmi les vivants")
            else:
                # Tous les fighters sont KO (géré par check_opponent_ko)
                print(f"DEBUG: Aucun fighter vivant")
    
    def execute_opponent_attack(self):
        """Exécute l'attaque de l'adversaire"""
        # Vérifier que c'est bien le tour de l'adversaire et que la bataille n'est pas finie
        if self.battle and not self.battle.game_over and self.battle.current_turn == "opponent":
            print(f"DEBUG execute_opponent_attack: PP adversaire = {self.opponent.pp}")
            
            # Vérifier si l'adversaire doit changer par manque de PP
            if self.opponent.pp <= 0:
                print(f"DEBUG: Adversaire n'a plus de PP, appel de check_opponent_no_pp()")
                self.check_opponent_no_pp()
                # Après le switch, passer au tour du joueur
                if self.battle.current_turn == "opponent":
                    self.battle.current_turn = "player"
                return
            
            # Attaquer
            self.battle.opponent_attack()
            self.play_sfx("explosion")
            print(f"DEBUG après attaque: PP adversaire = {self.opponent.pp}")
            
            # Vérifier si le joueur est KO
            if self.player_fighter.pv <= 0:
                self.check_player_ko()
            else:
                # Vérifier à nouveau si l'adversaire n'a plus de PP après l'attaque
                if self.opponent.pp <= 0:
                    print(f"DEBUG: Adversaire n'a plus de PP après attaque, appel de check_opponent_no_pp()")
                    self.check_opponent_no_pp()
                    # Après le switch, passer au tour du joueur
                    if self.battle.current_turn == "opponent":
                        self.battle.current_turn = "player"
                else:
                    # Passer au tour du joueur normalement
                    self.battle.current_turn = "player"
    
    def check_opponent_ko(self):
        """Vérifie si l'adversaire est KO et gère le switch ou la victoire"""
        # Trouver l'index du fighter actuel dans l'équipe adverse
        current_index = self.opponent_team.index(self.opponent.name)
        
        # Chercher le prochain fighter vivant
        next_opponent = None
        for i in range(current_index + 1, len(self.opponent_team)):
            fighter_name = self.opponent_team[i]
            if self.opponent_fighters[fighter_name].pv > 0:
                next_opponent = fighter_name
                break
        
        if next_opponent:
            # Il reste des fighters adverses, switch automatique
            self.all_sprites.remove(self.opponent)
            self.opponent = self.opponent_fighters[next_opponent]
            self.all_sprites.add(self.opponent)
            self.battle.opponent = self.opponent
            self.battle.battle_log.append(f"{next_opponent} entre en combat!")
            # Passer au tour de l'adversaire après le switch
            self.battle.current_turn = "opponent"
            self.opponent_attack_timer.deactivate()
            self.opponent_attack_timer.activate()
        else:
            # Plus de fighters adverses, victoire du joueur
            self.battle.game_over = True
            self.battle.winner = self.player_fighter.name
            self.battle.battle_log.append(f"Victoire! L'équipe adverse est éliminée!")
    
    def check_player_ko(self):
        """Vérifie si le joueur est KO et gère le switch ou la défaite"""
        # Trouver l'index du fighter actuel dans l'équipe joueur
        current_index = self.team.index(self.player_fighter.name)
        
        # Chercher le prochain fighter vivant
        next_fighter = None
        for i in range(current_index + 1, len(self.team)):
            fighter_name = self.team[i]
            if self.team_fighters[fighter_name].pv > 0:
                next_fighter = fighter_name
                break
        
        if next_fighter:
            # Il reste des fighters, switch automatique
            self.all_sprites.remove(self.player_fighter)
            self.player_fighter = self.team_fighters[next_fighter]
            self.all_sprites.add(self.player_fighter)
            self.battle.player = self.player_fighter
            self.battle.battle_log.append(f"{next_fighter} entre en combat!")
            # Le joueur peut jouer après le switch
            self.battle.current_turn = "player"
        else:
            # Plus de fighters, défaite du joueur
            self.battle.game_over = True
            self.battle.winner = self.opponent.name
            self.battle.battle_log.append(f"Défaite! Toute votre équipe est éliminée!")
    
    def update(self, dt):
        """Met à jour l'état du jeu"""
        if self.app_state == "battle" and self.battle:
            self.all_sprites.update(dt)
            self.opponent_attack_timer.update()
    
    def draw(self):
        """Affiche le jeu"""
        # Fond
        self.display_surface.blit(self.bg_surfs["bg"], (0, 0))
        
        if self.app_state == "home":
            if self.team_menu_active:
                self.hud.draw_team_menu(self.team, self.selected_fighter, self.team_view_mode)
            elif self.home_clashdex_active:
                # Afficher le Clashdex avec le fighter sélectionné
                fighters_list = list(FIGHTER_CONFIG.keys())
                fighter_name = fighters_list[self.home_clashdex_index]
                fighter_data = FIGHTER_CONFIG[fighter_name]
                
                # Créer un fighter temporaire pour afficher ses stats
                from Fighter import Opponent
                temp_fighter = Opponent(fighter_name, self.front_surfs[fighter_name], fighter_data, groups=None)
                
                self.hud.draw_home_clashdex(temp_fighter, self.front_surfs[fighter_name], self.home_clashdex_index, len(fighters_list))
            else:
                self.hud.draw_home_menu(self.home_menu_options, self.selected_home)
        else:
            # Combattants
            self.all_sprites.draw(self.display_surface)
            
            # HUD
            turn_name = "joueur" if self.battle.current_turn == "player" else "adversaire"
            self.hud.draw_turn_indicator(turn_name)
            
            # Infos des combattants
            self.hud.draw_fighter_info(self.player_fighter, "left")
            self.hud.draw_fighter_info(self.opponent, "right")
            
            # Menu (seulement si c'est le tour du joueur et pas de game over)
            if not self.battle.game_over:
                if self.hud.menu_state == "main":
                    self.hud.draw_main_menu(self.selected_attack)
                elif self.hud.menu_state == "attacks":
                    self.hud.draw_attack_buttons(
                        self.player_fighter.attaques,
                        self.player_fighter.pp,
                        self.selected_attack
                    )
                elif self.hud.menu_state == "switch":
                    # Afficher le menu principal en arrière-plan (visuel seulement)
                    self.hud.draw_main_menu(2)  # Switch option (index 2) est mise en évidence
                    # Puis afficher le menu switch par-dessus
                    self.hud.draw_switch_menu(self.team, self.team_fighters, self.player_fighter.name, self.selected_attack)
            
            # Popup Clashdex (afficher par-dessus tout)
            if self.clashdex_active:
                self.hud.draw_clashdex_popup(self.opponent, self.front_surfs[self.opponent.name])
            
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

            # Confirmation de sortie
            if self.confirm_quit_active:
                self.hud.draw_confirm_quit(self.confirm_quit_selected)
        
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
