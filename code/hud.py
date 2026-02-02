from settings import *

class BattleHUD:
    """Interface graphique du combat"""
    def __init__(self, display_surface, font_size=24):
        self.display_surface = display_surface
        self.font = pygame.font.Font(None, font_size)
        self.font_big = pygame.font.Font(None, int(font_size * 1.5))
        self.button_width = 200
        self.button_height = 50
        self.button_padding = 20
        self.selected_button = 0
        
        # Positions des boutons
        self.buttons = []
        self.update_button_positions()
    
    def update_button_positions(self):
        """Met à jour les positions des boutons"""
        start_x = WINDOW_WIDTH // 2 - (self.button_width * 2 + self.button_padding * 3) // 2
        start_y = WINDOW_HEIGHT - 120
        
        self.buttons = []
        for i in range(4):
            x = start_x + (i % 2) * (self.button_width + self.button_padding)
            y = start_y + (i // 2) * (self.button_height + self.button_padding)
            self.buttons.append(pygame.Rect(x, y, self.button_width, self.button_height))
    
    def draw_fighter_info(self, fighter, side="left"):
        """Affiche les infos d'un combattant"""
        if side == "left":
            x, y = 20, 20
        else:
            x, y = WINDOW_WIDTH - 300, 20
        
        # Fond semi-transparent
        pygame.draw.rect(self.display_surface, (0, 0, 0), (x - 10, y - 10, 280, 170), border_radius=10)
        pygame.draw.rect(self.display_surface, (100, 100, 100), (x - 10, y - 10, 280, 170), 3, border_radius=10)
        
        # Nom
        name_surf = self.font_big.render(fighter.name, True, COLORS['white'])
        self.display_surface.blit(name_surf, (x, y))
        
        # PV
        pv_text = f"PV: {fighter.pv}/{fighter.max_pv}"
        pv_surf = self.font.render(pv_text, True, COLORS['white'])
        self.display_surface.blit(pv_surf, (x, y + 35))
        
        # Barre de PV
        bar_width = 250
        bar_height = 20
        bar_x, bar_y = x, y + 60
        
        # Fond rouge
        pygame.draw.rect(self.display_surface, (139, 0, 0), (bar_x, bar_y, bar_width, bar_height), border_radius=5)
        # PV restants en vert
        pv_percentage = fighter.pv / fighter.max_pv
        pygame.draw.rect(self.display_surface, (0, 200, 0), (bar_x, bar_y, bar_width * pv_percentage, bar_height), border_radius=5)
        pygame.draw.rect(self.display_surface, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2, border_radius=5)
        
        # PP
        pp_text = f"PP: {fighter.pp}/{fighter.max_pp}"
        pp_surf = self.font.render(pp_text, True, COLORS['white'])
        self.display_surface.blit(pp_surf, (x, y + 85))
        
        # Barre de PP
        pp_bar_y = y + 110
        # Fond gris
        pygame.draw.rect(self.display_surface, (50, 50, 50), (bar_x, pp_bar_y, bar_width, bar_height), border_radius=5)
        # PP restants en bleu
        pp_percentage = fighter.pp / fighter.max_pp if fighter.max_pp > 0 else 0
        pygame.draw.rect(self.display_surface, (0, 100, 255), (bar_x, pp_bar_y, bar_width * pp_percentage, bar_height), border_radius=5)
        pygame.draw.rect(self.display_surface, (255, 255, 255), (bar_x, pp_bar_y, bar_width, bar_height), 2, border_radius=5)
        
        # Effets
        if fighter.effects:
            effects_text = f"Effets: {', '.join(fighter.effects)}"
            effects_surf = self.font.render(effects_text, True, COLORS['red'])
            self.display_surface.blit(effects_surf, (x, y + 135))
    
    def draw_attack_buttons(self, attaques, pp, selected=0):
        """Affiche les boutons d'attaque"""
        for i, button in enumerate(self.buttons):
            # Couleur du bouton
            if i >= len(attaques):
                color = (80, 80, 80)
                text_color = (200, 200, 200)
            else:
                attaque = attaques[i]
                if pp < attaque["cout_pp"]:
                    color = (100, 0, 0)
                    text_color = (255, 0, 0)
                elif i == selected:
                    color = (0, 150, 255)
                    text_color = (255, 255, 255)
                else:
                    color = (50, 150, 50)
                    text_color = (255, 255, 255)
            
            # Dessiner le bouton
            pygame.draw.rect(self.display_surface, color, button, border_radius=5)
            pygame.draw.rect(self.display_surface, (200, 200, 200), button, 2, border_radius=5)
            
            # Texte du bouton
            if i < len(attaques):
                attaque = attaques[i]
                text = f"{attaque['nom']}\nCoût: {attaque['cout_pp']} PP"
                
                # Afficher sur deux lignes
                lines = text.split('\n')
                for j, line in enumerate(lines):
                    line_surf = self.font.render(line, True, text_color)
                    line_rect = line_surf.get_rect(center=(button.centerx, button.centery - 5 + j * 15))
                    self.display_surface.blit(line_surf, line_rect)
    
    def draw_battle_log(self, log_messages, max_lines=3):
        """Affiche le log de combat"""
        log_x, log_y = 20, WINDOW_HEIGHT - 200
        
        # Fond semi-transparent
        pygame.draw.rect(self.display_surface, (0, 0, 0), (log_x - 10, log_y - 10, WINDOW_WIDTH *0.25, 150), border_radius=10)
        pygame.draw.rect(self.display_surface, (100, 100, 100), (log_x - 10, log_y - 10, WINDOW_WIDTH *0.25, 150), 3, border_radius=10)
        
        # Afficher les derniers messages
        for i, message in enumerate(log_messages[-max_lines:]):
            msg_surf = self.font.render(message, True, COLORS['white'])
            self.display_surface.blit(msg_surf, (log_x, log_y + i * 35))
    
    def draw_turn_indicator(self, current_turn):
        """Affiche l'indicateur de tour"""
        text = f"Tour du {current_turn}"
        text_color = COLORS['white'] if current_turn == "joueur" else COLORS['red']
        turn_surf = self.font_big.render(text, True, text_color)
        turn_rect = turn_surf.get_rect(center=(WINDOW_WIDTH // 2, 50))
        self.display_surface.blit(turn_surf, turn_rect)
    
    def draw_game_over(self, winner):
        """Affiche l'écran de fin de jeu"""
        # Fond semi-transparent
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.display_surface.blit(overlay, (0, 0))
        
        # Texte de victoire
        if winner == "joueur":
            text = "VICTOIRE!"
            color = COLORS['green'] if 'green' in COLORS else (0, 255, 0)
        else:
            text = "DEFAITE!"
            color = COLORS['red']
        
        text_surf = pygame.font.Font(None, 80).render(text, True, color)
        text_rect = text_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        self.display_surface.blit(text_surf, text_rect)
        
        # Message de redémarrage
        restart_text = "Appuyez sur ESPACE pour recommencer"
        restart_surf = self.font.render(restart_text, True, COLORS['white'])
        restart_rect = restart_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        self.display_surface.blit(restart_surf, restart_rect)
