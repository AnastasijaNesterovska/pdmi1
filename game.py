import pygame
import sys
from pygame.locals import *

# Pygame inicializācija
pygame.init()

# Loga izmēri
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Krāsas
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Fonts
font = pygame.font.Font(None, 36)

# Loga izveide
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("MaxLiga Game")

class Game:
    def __init__(self, start_number):
        self.current_number = start_number
        self.total_points = 0
        self.bank = 0
        self.game_over = False
        self.winner = None

    def make_move(self, multiplier):
        if self.game_over:
            return

        self.current_number *= multiplier
        if self.current_number % 2 == 0:
            self.total_points += 1
        else:
            self.total_points -= 1

        if self.current_number % 10 == 0 or self.current_number % 10 == 5:
            self.bank += 1

        if self.current_number >= 3000:
            self.game_over = True
            self.finalize_game()

    def finalize_game(self):
        if self.total_points % 2 == 0:
            self.total_points -= self.bank
        else:
            self.total_points += self.bank

        if self.total_points % 2 == 0:
            self.winner = "Player 1"
        else:
            self.winner = "Player 2"

# Minimaksa algoritms
def minimax(game_state, depth, maximizing_player):
    if depth == 0 or game_state.game_over:
        return heuristic(game_state)

    if maximizing_player:
        max_eval = -float('inf')
        for multiplier in [3, 4, 5]:
            new_state = simulate_move(game_state, multiplier)
            eval = minimax(new_state, depth - 1, False)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for multiplier in [3, 4, 5]:
            new_state = simulate_move(game_state, multiplier)
            eval = minimax(new_state, depth - 1, True)
            min_eval = min(min_eval, eval)
        return min_eval

# Heiristiskā novērtējuma funkcija
def heuristic(game_state):
    return game_state.total_points

# Simulē gājienu
def simulate_move(game_state, multiplier):
    new_state = Game(game_state.current_number)
    new_state.total_points = game_state.total_points
    new_state.bank = game_state.bank
    new_state.make_move(multiplier)
    return new_state

# Datora gājiens
def computer_move(game_state, algorithm):
    best_score = -float('inf')
    best_multiplier = 3
    for multiplier in [3, 4, 5]:
        new_state = simulate_move(game_state, multiplier)
        if algorithm == "minimax":
            score = minimax(new_state, depth=3, maximizing_player=False)
        elif algorithm == "alphabeta":
            score = minimax(new_state, depth=3, maximizing_player=False)  # Var aizstāt ar Alfa-beta
        if score > best_score:
            best_score = score
            best_multiplier = multiplier
    return best_multiplier

# Galvenā funkcija
def main():
    clock = pygame.time.Clock()
    game = None
    start_number = 0
    input_active = True
    input_text = ""
    algorithm = None
    player_turn = True  # True - cilvēks, False - dators

    while True:
        window.fill(WHITE)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if input_active:
                    if event.key == K_RETURN:
                        start_number = int(input_text)
                        game = Game(start_number)
                        input_active = False
                    elif event.key == K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode
                else:
                    if algorithm is None:
                        if event.key == K_1:
                            algorithm = "minimax"
                        elif event.key == K_2:
                            algorithm = "alphabeta"
                    else:
                        if player_turn:
                            if event.key == K_3:
                                game.make_move(3)
                                player_turn = False  # Pārslēdz uz datora gājienu
                            elif event.key == K_4:
                                game.make_move(4)
                                player_turn = False
                            elif event.key == K_5:
                                game.make_move(5)
                                player_turn = False
                        else:
                            # Dators veic gājienu
                            multiplier = computer_move(game, algorithm)
                            game.make_move(multiplier)
                            player_turn = True  # Pārslēdz atpakaļ uz spēlētāja gājienu

                            # Pēc datora gājiena atjaunina ekrānu
                            window.fill(WHITE)
                            draw_text(f"Pašreizējais skaitlis: {game.current_number}", 100, 100, BLACK)
                            draw_text(f"Kopējie punkti: {game.total_points}", 100, 150, BLACK)
                            draw_text(f"Banka: {game.bank}", 100, 200, BLACK)
                            draw_text("Dators veica gājienu. Spiediet 3, 4 vai 5, lai veiktu gājienu.", 100, 250, BLACK)
                            pygame.display.update()
                            pygame.time.delay(1000)  # Neliels aizkave, lai varētu redzēt datora gājienu

        if input_active:
            draw_text("Ievadiet sākuma skaitli (20-30):", 100, 100, BLACK)
            draw_text(input_text, 100, 150, BLACK)
        else:
            if algorithm is None:
                draw_text("Izvēlieties algoritmu: 1 - Minimaks, 2 - Alfa-beta", 100, 100, BLACK)
            else:
                draw_text(f"Pašreizējais skaitlis: {game.current_number}", 100, 100, BLACK)
                draw_text(f"Kopējie punkti: {game.total_points}", 100, 150, BLACK)
                draw_text(f"Banka: {game.bank}", 100, 200, BLACK)
                if player_turn:
                    draw_text("Spiediet 3, 4 vai 5, lai veiktu gājienu", 100, 250, BLACK)
                else:
                    draw_text("Dators veic gājienu...", 100, 250, BLACK)

                if game.game_over:
                    draw_text(f"Spēle beigusies! Uzvarētājs: {game.winner}", 100, 300, RED)

        pygame.display.update()
        clock.tick(30)

# Funkcija teksta zīmēšanai
def draw_text(text, x, y, color=BLACK):
    text_surface = font.render(text, True, color)
    window.blit(text_surface, (x, y))

if __name__ == "__main__":
    main()