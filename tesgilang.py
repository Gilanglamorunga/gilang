import pygame
import random
import sys

# Inisialisasi Pygame dan Mixer
pygame.init()
pygame.mixer.init()

# Konstanta
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PLAYER_SIZE = 50
ENEMY_SIZE = 50
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
ORANGE = (255, 120, 0)
BLACK = (0, 0, 0)
FPS = 60

# Set up layar
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Polisi vs Penjahat")
font = pygame.font.SysFont("Arial", 30)
clock = pygame.time.Clock()

# Load gambar latar belakang (ganti dengan file Anda jika perlu)
background = pygame.image.load(r"C:\Users\MyPC One Pro K-24\aiuw\gabywarna.jpg")

background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Fungsi menampilkan teks di tengah layar
def draw_text(text, size, color, surface, y_offset=0):
    font_obj = pygame.font.SysFont("Arial", size)
    text_surface = font_obj.render(text, True, color)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + y_offset))
    surface.blit(text_surface, text_rect)
def main_menu():
    # Setup tombol menu
    button_texts = ["Mulai Game", "Pengaturan", "Credits", "Keluar"]
    button_actions = [game_loop, None, show_credits, sys.exit]

    buttons = []

    button_width, button_height = 250, 50
    gap = 20
    start_y = (SCREEN_HEIGHT - ((button_height + gap) * len(button_texts))) // 2

    for i, text in enumerate(button_texts):
        rect = pygame.Rect(
            (SCREEN_WIDTH - button_width) // 2,
            start_y + i * (button_height + gap),
            button_width,
            button_height
        )
        buttons.append((text, rect, button_actions[i]))

    while True:
        screen.blit(background, (0, 0))

        # Judul Game
        title_font = pygame.font.SysFont("Arial", 60, bold=True)
        title_text = title_font.render("Polisi vs Penjahat", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_text, title_rect)

        # Tombol-tombol
        for text, rect, _ in buttons:
            pygame.draw.rect(screen, (0, 0, 0), rect, border_radius=10)
            pygame.draw.rect(screen, (0, 200, 255), rect, 3, border_radius=10)

            font_btn = pygame.font.SysFont("Arial", 28, bold=True)
            txt = font_btn.render(text, True, WHITE)
            txt_rect = txt.get_rect(center=rect.center)
            screen.blit(txt, txt_rect)

        pygame.display.update()

        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for _, rect, action in buttons:
                    if rect.collidepoint(event.pos) and action:
                        action()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
def show_credits():
    running = True
    while running:
        screen.blit(background, (0, 0))

        # Judul "Credits"
        title_font = pygame.font.SysFont("Arial", 48, bold=True)
        title_text = title_font.render("Credits", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_text, title_rect)

        # Isi credits
        credit_font = pygame.font.SysFont("Arial", 28)
        credit_lines = [
            "Dibuat oleh:",
            "Gilang Farrel",
            "dan",
            "Gaby"
        ]

        for i, line in enumerate(credit_lines):
            text = credit_font.render(line, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 180 + i * 40))
            screen.blit(text, text_rect)

        # Tombol kembali
        back_button = pygame.Rect((SCREEN_WIDTH - 200) // 2, SCREEN_HEIGHT - 100, 200, 50)
        pygame.draw.rect(screen, (0, 0, 0), back_button, border_radius=10)
        pygame.draw.rect(screen, (0, 200, 255), back_button, 3, border_radius=10)

        back_text = credit_font.render("Kembali", True, WHITE)
        back_text_rect = back_text.get_rect(center=back_button.center)
        screen.blit(back_text, back_text_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    running = False

# Membuat kotak
def create_rect(x=None, y=None, size=PLAYER_SIZE):
    if x is None:
        x = random.randint(0, SCREEN_WIDTH - size)
    if y is None:
        y = random.randint(0, SCREEN_HEIGHT - size)
    return pygame.Rect(x, y, size, size)

# Fungsi utama
def game_loop():
    player = create_rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    enemy = create_rect()
    walls = [pygame.Rect(300, 200, 200, 20), pygame.Rect(100, 400, 600, 20)]

    score = 0
    lives = 3
    level = 1
    enemy_speed = 2

    running = True
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        old_x, old_y = player.x, player.y
        if keys[pygame.K_LEFT]:
            player.x -= 5
        if keys[pygame.K_RIGHT]:
            player.x += 5
        if keys[pygame.K_UP]:
            player.y -= 5
        if keys[pygame.K_DOWN]:
            player.y += 5

        for wall in walls:
            if player.colliderect(wall):
                player.x, player.y = old_x, old_y

        player.clamp_ip(screen.get_rect())

        old_enemy_x, old_enemy_y = enemy.x, enemy.y
        if enemy.x < player.x:
            enemy.x += enemy_speed
        elif enemy.x > player.x:
            enemy.x -= enemy_speed
        if enemy.y < player.y:
            enemy.y += enemy_speed
        elif enemy.y > player.y:
            enemy.y -= enemy_speed
        for wall in walls:
            if enemy.colliderect(wall):
                enemy.x, enemy.y = old_enemy_x, old_enemy_y

        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, BLUE, player)
        pygame.draw.rect(screen, ORANGE, enemy)
        for wall in walls:
            pygame.draw.rect(screen, BLACK, wall)

        score_text = font.render(f"Skor: {score}", True, WHITE)
        level_text = font.render(f"Level: {level}", True, WHITE)
        lives_text = font.render(f"Nyawa: {lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 40))
        screen.blit(lives_text, (10, 70))

        if player.colliderect(enemy):
            lives -= 1
            if lives <= 0:
                draw_text("Game Over!", 60, (200, 0, 0), screen)
                pygame.display.update()
                pygame.time.wait(2000)
                running = False
            else:
                player = create_rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                enemy = create_rect()

        current_time = pygame.time.get_ticks() // 1000
        if current_time > score and score < 999:
            score += 1
            if score % 10 == 0:
                level += 1
                enemy_speed += 0.5

        pygame.display.update()
        clock.tick(FPS)

    main_menu()

# Jalankan
main_menu()

