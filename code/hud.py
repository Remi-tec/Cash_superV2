from settings import *

class BattleHUD:
    """Interface graphique du combat"""
    def __init__(self, display_surface, font_size=24):
        self.display_surface = display_surface
        self.font = pygame.font.Font(None, font_size)
        self.font_big = pygame.font.Font(None, int(font_size * 1.5))
        self.font_small = pygame.font.Font(None, int(font_size * 0.75))
        self.button_width = 200
        self.button_height = 50
        self.button_padding = 20
        self.selected_button = 0
        
        # État du menu
        self.menu_state = "main"  # "main" ou "attacks"
        self.main_menu_options = ["Attaques", "Object", "Switch", "Clashdex"]
        self.home_menu_options = ["Clashdex", "Combat", "Equipe", "Inventaire", "Boutique", "Quitter"]
        
        # Positions des boutons
        self.buttons = []
        self.update_button_positions()
    
    def update_button_positions(self):
        """Met à jour les positions des boutons"""
        start_x = WINDOW_WIDTH // 2 - (self.button_width * 2 + self.button_padding * 3) // 2
        start_y = WINDOW_HEIGHT - 145
        
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
    
    def draw_main_menu(self, selected=0):
        """Affiche le menu principal d'action"""
        # Dessiner le fond gris du menu
        if self.buttons:
            min_x = min(btn.x for btn in self.buttons) - 15
            min_y = min(btn.y for btn in self.buttons) - 15
            max_x = max(btn.right for btn in self.buttons) + 15
            max_y = max(btn.bottom for btn in self.buttons) + 15
            
            bg_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
            pygame.draw.rect(self.display_surface, (60, 60, 60), bg_rect, border_radius=10)
            pygame.draw.rect(self.display_surface, (100, 100, 100), bg_rect, 3, border_radius=10)
        
        for i, button in enumerate(self.buttons):
            # Couleur du bouton
            if i >= len(self.main_menu_options):
                color = (80, 80, 80)
                text_color = (200, 200, 200)
            else:
                if i == selected:
                    color = (0, 150, 255)
                    text_color = (255, 255, 255)
                else:
                    color = (70, 70, 150)
                    text_color = (255, 255, 255)
            
            # Dessiner le bouton
            pygame.draw.rect(self.display_surface, color, button, border_radius=5)
            pygame.draw.rect(self.display_surface, (200, 200, 200), button, 2, border_radius=5)
            
            # Texte du bouton
            if i < len(self.main_menu_options):
                option_text = self.main_menu_options[i]
                text_surf = self.font.render(option_text, True, text_color)
                text_rect = text_surf.get_rect(center=button.center)
                self.display_surface.blit(text_surf, text_rect)

    def draw_home_menu(self, options=None, selected=0):
        """Affiche le menu global d'accueil"""
        if options is None:
            options = self.home_menu_options

        # Titre
        title_surf = pygame.font.Font(None, 90).render("SuperClash", True, COLORS['black'])
        title_rect = title_surf.get_rect(center=(WINDOW_WIDTH // 2, 110))
        self.display_surface.blit(title_surf, title_rect)

        # Calcul des positions (colonne unique)
        total_width = self.button_width
        total_height = self.button_height * len(options) + self.button_padding * (len(options) - 1)
        start_x = WINDOW_WIDTH // 2 - total_width // 2
        start_y = WINDOW_HEIGHT // 2 - total_height // 2 + 40

        buttons = []
        for i in range(len(options)):
            x = start_x
            y = start_y + i * (self.button_height + self.button_padding)
            buttons.append(pygame.Rect(x, y, self.button_width, self.button_height))

        for i, button in enumerate(buttons):
            if i == selected:
                color = (0, 150, 255)
                text_color = (255, 255, 255)
            else:
                color = (60, 60, 60)
                text_color = (255, 255, 255)

            pygame.draw.rect(self.display_surface, color, button, border_radius=5)
            pygame.draw.rect(self.display_surface, (255, 255, 255), button, 2, border_radius=5)

            option_text = options[i]
            text_surf = self.font.render(option_text, True, text_color)
            text_rect = text_surf.get_rect(center=button.center)
            self.display_surface.blit(text_surf, text_rect)
    
    def draw_attack_buttons(self, attaques, pp, selected=0):
        """Affiche les boutons d'attaque"""
        # Dessiner le fond gris du menu d'action
        if self.buttons:
            # Calculer la zone englobant tous les boutons
            min_x = min(btn.x for btn in self.buttons) - 15
            min_y = min(btn.y for btn in self.buttons) - 15
            max_x = max(btn.right for btn in self.buttons) + 15
            max_y = max(btn.bottom for btn in self.buttons) + 15
            
            # Dessiner le fond gris
            bg_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
            pygame.draw.rect(self.display_surface, (60, 60, 60), bg_rect, border_radius=10)
            pygame.draw.rect(self.display_surface, (100, 100, 100), bg_rect, 3, border_radius=10)
        
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
        log_x, log_y = 20, WINDOW_HEIGHT - 150
        
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

    def draw_confirm_quit(self, selected=0):
        """Affiche la confirmation de sortie pendant un combat"""
        # Overlay sombre
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.display_surface.blit(overlay, (0, 0))

        # Cadre principal
        box_width, box_height = 700, 220
        box_x = WINDOW_WIDTH // 2 - box_width // 2
        box_y = WINDOW_HEIGHT // 2 - box_height // 2
        box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        pygame.draw.rect(self.display_surface, (60, 60, 60), box_rect, border_radius=10)
        pygame.draw.rect(self.display_surface, (255, 255, 255), box_rect, 2, border_radius=10)

        # Texte
        msg = "Un combat est en cours, etes vous sur de vouloir quitter?"
        msg_surf = self.font.render(msg, True, COLORS['white'])
        msg_rect = msg_surf.get_rect(center=(WINDOW_WIDTH // 2, box_y + 60))
        self.display_surface.blit(msg_surf, msg_rect)

        # Boutons Oui / Non
        btn_width, btn_height = 140, 50
        gap = 40
        yes_rect = pygame.Rect(WINDOW_WIDTH // 2 - btn_width - gap // 2, box_y + 120, btn_width, btn_height)
        no_rect = pygame.Rect(WINDOW_WIDTH // 2 + gap // 2, box_y + 120, btn_width, btn_height)

        # Oui
        yes_color = (0, 150, 255) if selected == 0 else (80, 80, 80)
        pygame.draw.rect(self.display_surface, yes_color, yes_rect, border_radius=5)
        pygame.draw.rect(self.display_surface, (255, 255, 255), yes_rect, 2, border_radius=5)
        yes_text = self.font.render("Oui", True, COLORS['white'])
        yes_text_rect = yes_text.get_rect(center=yes_rect.center)
        self.display_surface.blit(yes_text, yes_text_rect)

        # Non
        no_color = (0, 150, 255) if selected == 1 else (80, 80, 80)
        pygame.draw.rect(self.display_surface, no_color, no_rect, border_radius=5)
        pygame.draw.rect(self.display_surface, (255, 255, 255), no_rect, 2, border_radius=5)
        no_text = self.font.render("Non", True, COLORS['white'])
        no_text_rect = no_text.get_rect(center=no_rect.center)
        self.display_surface.blit(no_text, no_text_rect)

    def draw_team_menu(self, team, selected=0, view_mode="available"):
        """Affiche le menu d'équipe avec fighters disponibles et équipe"""
        from support import load_stats
        config = load_stats("data/stats.json")
        fighters_list = list(config["fighters"].keys())

        # Titre
        title_surf = pygame.font.Font(None, 60).render("Equipe", True, COLORS['white'])
        title_rect = title_surf.get_rect(center=(WINDOW_WIDTH // 2, 50))
        self.display_surface.blit(title_surf, title_rect)

        # Colonnes
        col_width = 500
        left_x = 50
        right_x = WINDOW_WIDTH - col_width - 50
        y_start = 150
        item_height = 35
        item_margin = 5

        # Colonne gauche: Fighters disponibles
        pygame.draw.line(self.display_surface, (200, 200, 200), (left_x, y_start - 20), (left_x + col_width, y_start - 20), 2)
        avail_title = self.font_big.render("Disponibles (FLECHE DROITE: équipe)", True, COLORS['white'])
        self.display_surface.blit(avail_title, (left_x, y_start - 50))

        for i, fighter_name in enumerate(fighters_list):
            y = y_start + i * (item_height + item_margin)
            is_selected = (view_mode == "available" and i == selected)
            is_in_team = fighter_name in team
            
            if is_selected:
                color = (0, 150, 255)
            elif is_in_team:
                color = (100, 100, 100)
            else:
                color = (70, 70, 150)
            
            # Fond
            pygame.draw.rect(self.display_surface, color, (left_x, y, col_width, item_height), border_radius=5)
            if is_selected:
                pygame.draw.rect(self.display_surface, (255, 255, 255), (left_x, y, col_width, item_height), 2, border_radius=5)
            
            # Texte
            status = " (EN EQUIPE)" if is_in_team else ""
            text_surf = self.font.render(f"{fighter_name}{status}", True, COLORS['white'])
            text_rect = text_surf.get_rect(center=((left_x + col_width) // 2, y + item_height // 2))
            self.display_surface.blit(text_surf, text_rect)

        # Colonne droite: Equipe
        pygame.draw.line(self.display_surface, (200, 200, 200), (right_x, y_start - 20), (right_x + col_width, y_start - 20), 2)
        team_title = self.font_big.render(f"Equipe ({len(team)}/6) (FLECHE GAUCHE: retour)", True, COLORS['white'])
        self.display_surface.blit(team_title, (right_x, y_start - 50))

        for i, fighter_name in enumerate(team):
            y = y_start + i * (item_height + item_margin)
            is_selected = (view_mode == "team" and i == selected)
            
            if is_selected:
                color = (255, 0, 0)  # Rouge pour retirer
            else:
                color = (50, 150, 50)  # Vert pour l'équipe
            
            # Fond
            pygame.draw.rect(self.display_surface, color, (right_x, y, col_width, item_height), border_radius=5)
            if is_selected:
                pygame.draw.rect(self.display_surface, (255, 255, 255), (right_x, y, col_width, item_height), 2, border_radius=5)
            
            # Texte
            text_surf = self.font.render(f"#{i+1} {fighter_name}", True, COLORS['white'])
            text_rect = text_surf.get_rect(center=((right_x + col_width) // 2, y + item_height // 2))
            self.display_surface.blit(text_surf, text_rect)

        # Instructions
        instructions = [
            "HAUT/BAS: Naviguer | ENTREE: Ajouter/Retirer | ECHAP: Retour"
        ]
        for i, instr in enumerate(instructions):
            instr_surf = self.font.render(instr, True, (150, 150, 150))
            instr_rect = instr_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50 + i * 25))
            self.display_surface.blit(instr_surf, instr_rect)

    def draw_switch_menu(self, team, team_fighters, current_fighter, selected=0):
        """Affiche le menu de changement de fighter en colonne"""
        # Calcul des positions (colonne unique)
        button_width = 250
        button_height = 50
        button_padding = 10
        total_height = button_height * len(team) + button_padding * (len(team) - 1)
        start_x = WINDOW_WIDTH // 2 - button_width // 2
        start_y = WINDOW_HEIGHT // 2 - total_height // 2
        
        buttons = []
        for i in range(len(team)):
            x = start_x
            y = start_y + i * (button_height + button_padding)
            buttons.append(pygame.Rect(x, y, button_width, button_height))
        
        # Fond gris du menu
        if buttons:
            min_x = min(btn.x for btn in buttons) - 15
            min_y = min(btn.y for btn in buttons) - 15
            max_x = max(btn.right for btn in buttons) + 15
            max_y = max(btn.bottom for btn in buttons) + 15
            
            bg_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
            pygame.draw.rect(self.display_surface, (60, 60, 60), bg_rect, border_radius=10)
            pygame.draw.rect(self.display_surface, (100, 100, 100), bg_rect, 3, border_radius=10)
        
        for i, button in enumerate(buttons):
            # Couleur du bouton
            fighter_name = team[i]
            fighter = team_fighters[fighter_name]
            is_dead = fighter.pv <= 0
            
            if is_dead:
                color = (50, 50, 50)  # Noir pour les morts
                text_color = (100, 100, 100)  # Texte grisé
            elif fighter_name == current_fighter:
                color = (100, 100, 100)  # Grisé car c'est le fighter actuel
                text_color = (150, 150, 150)
            elif i == selected:
                color = (0, 150, 255)
                text_color = (255, 255, 255)
            else:
                color = (70, 150, 70)
                text_color = (255, 255, 255)
            
            # Dessiner le bouton
            pygame.draw.rect(self.display_surface, color, button, border_radius=5)
            pygame.draw.rect(self.display_surface, (200, 200, 200), button, 2, border_radius=5)
            
            # Texte du bouton
            if is_dead:
                status = " (MORT)"
            elif fighter_name == current_fighter:
                status = " (ACTUEL)"
            else:
                status = ""
            text_surf = self.font.render(f"{fighter_name}{status}", True, text_color)
            text_rect = text_surf.get_rect(center=button.center)
            self.display_surface.blit(text_surf, text_rect)
    
    def draw_clashdex_popup(self, opponent, opponent_image):
        """Affiche un popup à droite avec les stats complètes du fighter adverse"""
        # Dimensions et position du popup
        popup_width = 350
        popup_height = 620
        popup_x = WINDOW_WIDTH - popup_width - 20
        popup_y = (WINDOW_HEIGHT - popup_height) // 2
        
        # Fond du popup
        popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
        pygame.draw.rect(self.display_surface, (40, 40, 40), popup_rect, border_radius=10)
        pygame.draw.rect(self.display_surface, (150, 150, 150), popup_rect, 3, border_radius=10)
        
        # Titre (nom du fighter)
        title_surf = self.font_big.render(opponent.name, True, (255, 215, 0))
        title_rect = title_surf.get_rect(centerx=popup_x + popup_width // 2, top=popup_y + 15)
        self.display_surface.blit(title_surf, title_rect)
        
        # Image du fighter (redimensionnée)
        img_width = 150
        img_height = 200
        scaled_img = pygame.transform.scale(opponent_image, (img_width, img_height))
        img_x = popup_x + (popup_width - img_width) // 2
        img_y = popup_y + 60
        self.display_surface.blit(scaled_img, (img_x, img_y))
        
        # Stats (PV et PP)
        stats_y = img_y + img_height + 20
        
        # Stats (PV et PP max depuis stats.json, sans barres)
        # PV
        pv_text = f"PV: {opponent.max_pv}"
        pv_surf = self.font.render(pv_text, True, (255, 255, 255))
        self.display_surface.blit(pv_surf, (popup_x + 20, stats_y))
        
        # PP
        pp_y = stats_y + 30
        pp_text = f"PP: {opponent.max_pp}"
        pp_surf = self.font.render(pp_text, True, (255, 255, 255))
        self.display_surface.blit(pp_surf, (popup_x + 20, pp_y))
        
        # Attaques
        attacks_y = pp_y + 40
        attacks_title = self.font_big.render("Attaques:", True, (255, 215, 0))
        self.display_surface.blit(attacks_title, (popup_x + 20, attacks_y))
        
        # Liste des attaques
        attack_y = attacks_y + 35
        for i, attaque in enumerate(opponent.attaques):
            attack_name = attaque["nom"]
            attack_damage = attaque["degat"]
            attack_pp_cost = attaque["cout_pp"]
            attack_effect = attaque.get("effet", "")
            
            # Ligne principale : nom, dégâts, PP
            attack_text = f"{attack_name} ({attack_damage} dgt, {attack_pp_cost} PP)"
            attack_surf = self.font_small.render(attack_text, True, (220, 220, 220))
            self.display_surface.blit(attack_surf, (popup_x + 25, attack_y))
            attack_y += 22
            
            # Effet (si present)
            if attack_effect:
                effect_surf = self.font_small.render(f"  -> {attack_effect}", True, (150, 200, 150))
                self.display_surface.blit(effect_surf, (popup_x + 25, attack_y))
                attack_y += 22
            
            attack_y += 8  # Espacement entre les attaques
        
        # Instruction de fermeture
        close_text = "Appuyez sur ECHAP pour fermer"
        close_surf = self.font_small.render(close_text, True, (180, 180, 180))
        close_rect = close_surf.get_rect(centerx=popup_x + popup_width // 2, bottom=popup_y + popup_height - 10)
        self.display_surface.blit(close_surf, close_rect)
    
    def draw_home_clashdex(self, fighter, fighter_image, current_index, total_fighters):
        """Affiche le Clashdex dans le menu d'accueil avec navigation"""
        # Dimensions du popup
        popup_width = 500
        popup_height = 620
        popup_x = (WINDOW_WIDTH - popup_width) // 2
        popup_y = (WINDOW_HEIGHT - popup_height) // 2
        
        # Fond du popup
        popup_surface = pygame.Surface((popup_width, popup_height))
        popup_surface.fill((40, 40, 40))
        popup_surface.set_alpha(240)
        self.display_surface.blit(popup_surface, (popup_x, popup_y))
        
        # Bordure
        pygame.draw.rect(self.display_surface, (100, 100, 100), 
                        (popup_x, popup_y, popup_width, popup_height), 3)
        
        # Titre avec compteur
        title_text = f"Clashdex - {current_index + 1}/{total_fighters}"
        title_surf = self.font_big.render(title_text, True, (255, 215, 0))
        title_rect = title_surf.get_rect(centerx=popup_x + popup_width // 2, top=popup_y + 15)
        self.display_surface.blit(title_surf, title_rect)
        
        # Nom du fighter
        name_y = popup_y + 55
        name_surf = self.font_big.render(fighter.name, True, (255, 255, 255))
        name_rect = name_surf.get_rect(centerx=popup_x + popup_width // 2, top=name_y)
        self.display_surface.blit(name_surf, name_rect)
        
        # Image du fighter
        image_y = name_y + 45
        scaled_image = pygame.transform.scale(fighter_image, (150, 200))
        image_rect = scaled_image.get_rect(centerx=popup_x + popup_width // 2, top=image_y)
        self.display_surface.blit(scaled_image, image_rect)
        
        # Stats
        stats_y = image_y + 215
        pv_text = f"PV: {fighter.max_pv}"
        pv_surf = self.font.render(pv_text, True, (255, 255, 255))
        pv_rect = pv_surf.get_rect(centerx=popup_x + popup_width // 2, top=stats_y)
        self.display_surface.blit(pv_surf, pv_rect)
        
        # PP
        pp_y = stats_y + 30
        pp_text = f"PP: {fighter.max_pp}"
        pp_surf = self.font.render(pp_text, True, (255, 255, 255))
        pp_rect = pp_surf.get_rect(centerx=popup_x + popup_width // 2, top=pp_y)
        self.display_surface.blit(pp_surf, pp_rect)
        
        # Attaques
        attacks_y = pp_y + 40
        attacks_title = self.font_big.render("Attaques:", True, (255, 215, 0))
        attacks_rect = attacks_title.get_rect(centerx=popup_x + popup_width // 2, top=attacks_y)
        self.display_surface.blit(attacks_title, attacks_rect)
        
        # Liste des attaques
        attack_y = attacks_y + 35
        for i, attaque in enumerate(fighter.attaques):
            attack_name = attaque["nom"]
            attack_damage = attaque["degat"]
            attack_pp_cost = attaque["cout_pp"]
            attack_effect = attaque.get("effet", "")
            
            # Ligne principale : nom, dégâts, PP
            attack_text = f"{attack_name} ({attack_damage} dgt, {attack_pp_cost} PP)"
            attack_surf = self.font_small.render(attack_text, True, (220, 220, 220))
            attack_rect = attack_surf.get_rect(centerx=popup_x + popup_width // 2, top=attack_y)
            self.display_surface.blit(attack_surf, attack_rect)
            attack_y += 22
            
            # Effet (si present)
            if attack_effect:
                effect_surf = self.font_small.render(f"-> {attack_effect}", True, (150, 200, 150))
                effect_rect = effect_surf.get_rect(centerx=popup_x + popup_width // 2, top=attack_y)
                self.display_surface.blit(effect_surf, effect_rect)
                attack_y += 22
            
            attack_y += 8
        
        # Flèches de navigation
        arrow_y = popup_y + popup_height // 2
        
        # Flèche gauche
        if current_index > 0:
            left_arrow = self.font_big.render("<", True, (255, 255, 255))
            left_rect = left_arrow.get_rect(centerx=popup_x + 30, centery=arrow_y)
            self.display_surface.blit(left_arrow, left_rect)
        
        # Flèche droite
        if current_index < total_fighters - 1:
            right_arrow = self.font_big.render(">", True, (255, 255, 255))
            right_rect = right_arrow.get_rect(centerx=popup_x + popup_width - 30, centery=arrow_y)
            self.display_surface.blit(right_arrow, right_rect)
        
        # Instructions (à l'extérieur en bas de la carte)
        instructions_text = "<- -> : Navigation | ECHAP : Fermer"
        instructions_surf = self.font_small.render(instructions_text, True, (0, 0, 0))
        instructions_rect = instructions_surf.get_rect(centerx=popup_x + popup_width // 2, top=popup_y + popup_height + 15)
        self.display_surface.blit(instructions_surf, instructions_rect)
