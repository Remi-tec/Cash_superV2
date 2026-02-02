from settings import *
import random

class Battle:
    """Gère la logique du combat tour par tour"""
    def __init__(self, player, opponent):
        self.player = player
        self.opponent = opponent
        self.current_turn = "player"
        self.turn_number = 1
        self.battle_log = []
        self.game_over = False
        self.winner = None
        self.selected_attack = None
    
    def player_attack(self, attack_index):
        """Le joueur attaque"""
        if self.current_turn != "player":
            return False
        
        attaque = self.player.attaques[attack_index]
        
        # Vérifier les PP disponibles
        if self.player.pp < attaque["cout_pp"]:
            self.battle_log.append(f"{self.player.name} n'a pas assez de PP pour {attaque['nom']}!")
            return False
        
        self.selected_attack = attack_index
        self.apply_attack(self.player, self.opponent, attack_index)
        
        # Vérifier si l'adversaire est KO (mais ne pas terminer le jeu ici)
        if self.opponent.pv <= 0:
            self.battle_log.append(f"{self.opponent.name} est KO!")
            # Le game_over sera géré par main.py qui vérifie s'il reste des fighters
            return True
        
        # Passer au tour de l'adversaire
        self.current_turn = "opponent"
        return True
    
    def skip_turn(self):
        """Le joueur passe son tour"""
        if self.current_turn != "player":
            return False
        
        self.battle_log.append(f"{self.player.name} passe son tour!")
        self.current_turn = "opponent"
        return True
    
    def opponent_attack(self):
        """L'adversaire attaque"""
        # IA simple : choisir une attaque aléatoire avec assez de PP
        available_attacks = [i for i, attaque in enumerate(self.opponent.attaques) 
                            if self.opponent.pp >= attaque["cout_pp"]]
        
        if not available_attacks:
            self.battle_log.append(f"{self.opponent.name} n'a plus assez de PP!")
            # Mettre les PP à 0 pour déclencher le switch
            self.opponent.pp = 0
            self.current_turn = "player"
            self.turn_number += 1
            return
        
        attack_index = random.choice(available_attacks)
        self.apply_attack(self.opponent, self.player, attack_index)
        
        # Vérifier si le joueur est KO (mais ne pas terminer le jeu ici)
        if self.player.pv <= 0:
            self.battle_log.append(f"{self.player.name} est KO!")
            # Le game_over sera géré par main.py qui vérifie s'il reste des fighters
        else:
            self.current_turn = "player"
            self.turn_number += 1
    
    def apply_attack(self, attacker, defender, attack_index):
        """Applique une attaque"""
        attaque = attacker.attaques[attack_index]
        
        # Réduire les PP
        attacker.pp -= attaque["cout_pp"]
        
        # Vérifier critique
        is_crit = random.randint(1, 100) <= attaque["critique"]
        damage = attaque["degat"]
        
        if is_crit:
            damage = int(damage * 1.5)
            self.battle_log.append(f"Coup critique! {attacker.name} utilise {attaque['nom']}!")
        else:
            self.battle_log.append(f"{attacker.name} utilise {attaque['nom']}!")
        
        # Appliquer les effets spéciaux
        if attaque["effet"] == "reduction_degat":
            defender.defense_active = True
            damage = 0
            self.battle_log.append(f"{defender.name} se met en défense!")
        elif attaque["effet"] == "poison":
            if "poison" not in defender.effects:
                defender.effects.append("poison")
                self.battle_log.append(f"{defender.name} est empoisonné!")
        elif attaque["effet"] == "brulure":
            if "brulure" not in defender.effects:
                defender.effects.append("brulure")
                self.battle_log.append(f"{defender.name} est brûlé!")
        elif attaque["effet"] == "paralysie":
            if "paralysie" not in defender.effects:
                defender.effects.append("paralysie")
                self.battle_log.append(f"{defender.name} est paralysé!")
        elif attaque["effet"] == "gelé":
            if "gelé" not in defender.effects:
                defender.effects.append("gelé")
                self.battle_log.append(f"{defender.name} est gelé!")
        
        # Réduire les dégâts si défense active
        if defender.defense_active:
            damage = int(damage * 0.5)
            defender.defense_active = False
        
        # Appliquer les dégâts
        defender.pv -= damage
        
        if damage > 0:
            self.battle_log.append(f"Dégâts: {damage} PV")
        
        # Appliquer les dégâts des effets persistants
        if "poison" in defender.effects:
            poison_damage = int(defender.max_pv * 0.125)
            defender.pv -= poison_damage
            self.battle_log.append(f"Poison: -{poison_damage} PV")
        
        if "brulure" in defender.effects:
            burn_damage = int(defender.max_pv * 0.125)
            defender.pv -= burn_damage
            self.battle_log.append(f"Brûlure: -{burn_damage} PV")
        
        # S'assurer que les PV ne vont pas en dessous de 0
        if defender.pv < 0:
            defender.pv = 0
    
    def reset_battle(self):
        """Réinitialise le combat"""
        self.current_turn = "player"
        self.turn_number = 1
        self.battle_log = []
        self.game_over = False
        self.winner = None
        self.selected_attack = None
