import pygame
import random
import time

# Inicializē Pygame
pygame.init()

# Krāsas
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Spēles loga izmēri
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Spēle")

# Fonts
font = pygame.font.SysFont(None, 36)

# Spēles klase
class Game:
    def __init__(self):
        self.start_number = 0
        self.current_number = 0
        self.total_points = 0
        self.bank = 0
        self.players_turn = True  # True = Player's turn, False = Computer's turn
        self.running = True

    def start_game(self, start_number):
        self.start_number = start_number
        self.current_number = start_number
        self.total_points = 0
        self.bank = 0

    def make_move(self, multiplier):
        current = self.current_number
        new_number = current * multiplier
        self.current_number = new_number

        # Pāra vai nepāra skaitlis
        if new_number % 2 == 0:
            self.total_points += 1
        else:
            self.total_points -= 1

        # Skaitlis beidzas ar 0 vai 5
        if new_number % 10 == 0 or new_number % 10 == 5:
            self.bank += 1

        if new_number >= 3000:
            self.end_game()

    def end_game(self):
        if self.total_points % 2 == 0:
            self.total_points -= self.bank
        else:
            self.total_points += self.bank
        self.running = False

    def reset_game(self):
        self.start_number = 0
        self.current_number = 0
        self.total_points = 0
        self.bank = 0

# Minimaksa algoritms
def minimax(game, depth, is_maximizing_player):
    if depth == 0 or game.current_number >= 3000:
        return game.total_points

    if is_maximizing_player:
        max_eval = float('-inf')
        for multiplier in [3, 4, 5]:
            game.make_move(multiplier)
            eval = minimax(game, depth - 1, False)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for multiplier in [3, 4, 5]:
            game.make_move(multiplier)
            eval = minimax(game, depth - 1, True)
            min_eval = min(min_eval, eval)
        return min_eval

# Alfa-beta algoritms
def alpha_beta(game, depth, alpha, beta, is_maximizing_player):
    if depth == 0 or game.current_number >= 3000:
        return game.total_points

    if is_maximizing_player:
        max_eval = float('-inf')
        for multiplier in [3, 4, 5]:
            game.make_move(multiplier)
            eval = alpha_beta(game, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for multiplier in [3, 4, 5]:
            game.make_move(multiplier)
            eval = alpha_beta(game, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

# GUI funkcija, lai attēlotu tekstu uz ekrāna
def display_text(text, x, y, color=BLACK):
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, (x, y))

# Galvenais spēles cikls
def main():
    game = Game()
    clock = pygame.time.Clock()

    # Spēles sākums
    playing = True
    while playing:
        screen.fill(WHITE)

        # Spēlētāja izvēles izvēlne
        display_text("Izvēlies skaitli no 20 līdz 30, lai sāktu:", 50, 50)
        pygame.display.update()

        # Gaidām spēlētāja izvēli
        start_number = 0
        while start_number < 20 or start_number > 30:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Spēlētājs apstiprina izvēli
                        game.start_game(start_number)
                        break
                    elif event.key in range(pygame.K_1, pygame.K_9 + 1):
                        start_number = int(chr(event.key))
                    elif event.key == pygame.K_0:
                        start_number = 0

        # Parādām spēles statusu
        display_text(f"Starta skaitlis: {start_number}", 50, 150)
        display_text(f"Skaitlis: {game.current_number}", 50, 200)
        display_text(f"Totālie punkti: {game.total_points}", 50, 250)
        display_text(f"Bankas punkti: {game.bank}", 50, 300)

        pygame.display.update()

        # Spēlētāja vai datora gājiens
        if game.players_turn:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_3:
                        game.make_move(3)
                    elif event.key == pygame.K_4:
                        game.make_move(4)
                    elif event.key == pygame.K_5:
                        game.make_move(5)

        # Datora gājiens (Minimaksa vai Alfa-beta algoritms)
        else:
            best_move = minimax(game, 3, True)  # Vai izmantot Alfa-beta šeit, atkarībā no izvēles
            game.make_move(best_move)
            game.players_turn = True  # Mainām gājienus

        # Spēles beigas
        if not game.running:
            display_text("Spēle beigusies", 50, 350)
            pygame.display.update()
            time.sleep(3)  # Parāda rezultātus uz 3 sekundēm
            playing = False

        clock.tick(30)

# Spēles sākšana
main()

# Aizveram Pygame
pygame.quit()
