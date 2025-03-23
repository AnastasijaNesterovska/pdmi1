import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spēle: Reizināšana")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Шрифт для текста
font = pygame.font.Font(None, 36)

class Game:
    def __init__(self):
        self.start_number = 0
        self.current_number = 0
        self.total_points = 0
        self.bank = 0
        self.running = True

    def start_game(self, start_number):
        if 20 <= start_number <= 30:
            self.start_number = start_number
            self.current_number = start_number
            self.total_points = 0
            self.bank = 0
        else:
            print("Ievadiet skaitli no 20 līdz 30")

    def make_move(self, multiplier):
        current = self.current_number
        new_number = current * multiplier
        
        # Ранжирование очков
        if new_number % 2 == 0:
            self.total_points += 1
        else:
            self.total_points -= 1
        
        if new_number % 10 == 0 or new_number % 10 == 5:
            self.bank += 1
        
        self.current_number = new_number

        if new_number >= 3000:
            self.end_game()

    def end_game(self):
        final_score = self.total_points
        if final_score % 2 == 0:
            final_score -= self.bank
        else:
            final_score += self.bank
        
        winner = "Pirmais spēlētājs" if final_score % 2 == 0 else "Otrais spēlētājs"
        print(f"Spēle beigusies! Uzvarētājs: {winner}")
        self.running = False

    def reset_game(self):
        self.start_number = 0
        self.current_number = 0
        self.total_points = 0
        self.bank = 0

# Основной игровой цикл
game = Game()
game.start_game(25)  # Пример начала игры с числа 25

while game.running:
    screen.fill(WHITE)

    # Отображаем текущие данные
    start_text = font.render(f"Start number: {game.start_number}", True, BLACK)
    screen.blit(start_text, (20, 20))

    current_text = font.render(f"Current number: {game.current_number}", True, BLACK)
    screen.blit(current_text, (20, 60))

    points_text = font.render(f"Total points: {game.total_points}", True, BLACK)
    screen.blit(points_text, (20, 100))

    bank_text = font.render(f"Bank: {game.bank}", True, BLACK)
    screen.blit(bank_text, (20, 140))

    # Кнопки для игры
    button_font = pygame.font.Font(None, 28)

    button_3 = pygame.draw.rect(screen, GREEN, (20, 200, 150, 40))
    button_4 = pygame.draw.rect(screen, GREEN, (20, 250, 150, 40))
    button_5 = pygame.draw.rect(screen, GREEN, (20, 300, 150, 40))

    screen.blit(button_font.render("Multiply by 3", True, BLACK), (50, 210))
    screen.blit(button_font.render("Multiply by 4", True, BLACK), (50, 260))
    screen.blit(button_font.render("Multiply by 5", True, BLACK), (50, 310))

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if button_3.collidepoint(mouse_x, mouse_y):
                game.make_move(3)
            elif button_4.collidepoint(mouse_x, mouse_y):
                game.make_move(4)
            elif button_5.collidepoint(mouse_x, mouse_y):
                game.make_move(5)

    pygame.display.update()

pygame.quit()
sys.exit()
