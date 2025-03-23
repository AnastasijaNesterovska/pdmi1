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
GRAY = (200, 200, 200)

# Fonts
font = pygame.font.Font(None, 36)

# Loga izveide
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("MaxLiga Game")

# Pogu izmēri un pozīcijas
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50
BUTTON_GAP = 20

# Spēles stāvokļa klase
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

# Funkcija, lai zīmētu pogas
def draw_button(text, x, y, width, height, color):
    pygame.draw.rect(window, color, (x, y, width, height))
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
    window.blit(text_surface, text_rect)

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

            if event.type == KEYDOWN and input_active:
                if event.key == K_RETURN:
                    if input_text.strip():  # Pārbauda, vai input_text nav tukšs
                        try:
                            start_number = int(input_text)
                            if 20 <= start_number <= 30:
                                game = Game(start_number)
                                input_active = False
                            else:
                                print("Skaitlim jābūt no 20 līdz 30!")
                        except ValueError:
                            print("Ievadiet derīgu skaitli!")
                    else:
                        print("Ievadiet skaitli!")
                elif event.key == K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if event.unicode.isdigit():  # Pārbauda, vai ievadītais simbols ir cipars
                        input_text += event.unicode

            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if not input_active:
                    if algorithm is None:
                        # Pārbauda, vai noklikšķināts uz algoritma pogām
                        if 200 <= mouse_pos[0] <= 350 and 200 <= mouse_pos[1] <= 250:
                            algorithm = "minimax"
                        elif 450 <= mouse_pos[0] <= 600 and 200 <= mouse_pos[1] <= 250:
                            algorithm = "alphabeta"
                    else:
                        if player_turn:
                            # Pārbauda, vai noklikšķināts uz gājiena pogām
                            if 200 <= mouse_pos[0] <= 300 and 400 <= mouse_pos[1] <= 450:
                                game.make_move(3)
                                player_turn = False
                            elif 350 <= mouse_pos[0] <= 450 and 400 <= mouse_pos[1] <= 450:
                                game.make_move(4)
                                player_turn = False
                            elif 500 <= mouse_pos[0] <= 600 and 400 <= mouse_pos[1] <= 450:
                                game.make_move(5)
                                player_turn = False
                        else:
                            # Dators veic gājienu
                            multiplier = computer_move(game, algorithm)
                            game.make_move(multiplier)
                            player_turn = True

                            # Pēc datora gājiena atjaunina ekrānu
                            window.fill(WHITE)
                            draw_text(f"Pašreizējais skaitlis: {game.current_number}", 100, 100, BLACK)
                            draw_text(f"Kopējie punkti: {game.total_points}", 100, 150, BLACK)
                            draw_text(f"Banka: {game.bank}", 100, 200, BLACK)
                            draw_text("Dators veica gājienu. Izvēlieties gājienu.", 100, 250, BLACK)
                            pygame.display.update()
                            pygame.time.delay(1000)  # Neliels aizkave, lai varētu redzēt datora gājienu

        if input_active:
            draw_text("Ievadiet sākuma skaitli (20-30):", 100, 100, BLACK)
            draw_text(input_text, 100, 150, BLACK)
            draw_button("Enter", 300, 200, 200, 50, GRAY)
        else:
            if algorithm is None:
                draw_text("Izvēlieties algoritmu:", 100, 100, BLACK)
                draw_button("Minimaks", 200, 200, 150, 50, GRAY)
                draw_button("Alfa-beta", 450, 200, 150, 50, GRAY)
            else:
                draw_text(f"Pašreizējais skaitlis: {game.current_number}", 100, 100, BLACK)
                draw_text(f"Kopējie punkti: {game.total_points}", 100, 150, BLACK)
                draw_text(f"Banka: {game.bank}", 100, 200, BLACK)
                if player_turn:
                    draw_text("Izvēlieties gājienu:", 100, 300, BLACK)
                    draw_button("3", 200, 400, 100, 50, GRAY)
                    draw_button("4", 350, 400, 100, 50, GRAY)
                    draw_button("5", 500, 400, 100, 50, GRAY)
                else:
                    draw_text("Dators veic gājienu...", 100, 300, BLACK)

                if game.game_over:
                    draw_text(f"Spēle beigusies! Uzvarētājs: {game.winner}", 100, 500, RED)

        pygame.display.update()
        clock.tick(30)

# Funkcija teksta zīmēšanai
def draw_text(text, x, y, color=BLACK):
    text_surface = font.render(text, True, color)
    window.blit(text_surface, (x, y))

if __name__ == "__main__":
    main()