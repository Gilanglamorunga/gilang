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

# # Musik & Suara
# pygame.mixer.music.load("background.mp3")
# pygame.mixer.music.play(-1)
# hit_sound = pygame.mixer.Sound("hit.wav")

# Set up layar
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Polisi vs Penjahat")
font = pygame.font.SysFont("Arial", 30)
clock = pygame.time.Clock()

# Fungsi untuk menampilkan teks di tengah
def draw_text(text, size, color, surface, y_offset=0):
    font_obj = pygame.font.SysFont("Arial", size)
    text_surface = font_obj.render(text, True, color)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + y_offset))
    surface.blit(text_surface, text_rect)

# Fungsi menu utama
def main_menu():
    while True:
        screen.fill(WHITE)
        draw_text("Polisi vs Penjahat", 50, BLACK, screen, -50)
        draw_text("Tekan ENTER untuk mulai", 30, BLACK, screen, 20)
        draw_text("Tekan ESC untuk keluar", 30, BLACK, screen, 60)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_loop()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# Fungsi membuat objek
def create_rect(x=None, y=None, size=PLAYER_SIZE):
    if x is None:
        x = random.randint(0, SCREEN_WIDTH - size)
    if y is None:
        y = random.randint(0, SCREEN_HEIGHT - size)
    return pygame.Rect(x, y, size, size)

# Fungsi utama game
def game_loop():
    # Objek awal
    player = create_rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    enemy = create_rect()
    walls = [pygame.Rect(300, 200, 200, 20), pygame.Rect(100, 400, 600, 20)]

    # Variabel status
    score = 0
    lives = 3
    level = 1
    enemy_speed = 2

    running = True
    while running:
        screen.fill(WHITE)

        # Input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: player.x -= 5
        if keys[pygame.K_RIGHT]: player.x += 5
        if keys[pygame.K_UP]: player.y -= 5
        if keys[pygame.K_DOWN]: player.y += 5

        # Batas layar
        player.clamp_ip(screen.get_rect())

        # Deteksi dinding
        for wall in walls:
            if player.colliderect(wall):
                if keys[pygame.K_LEFT]: player.x += 5
                if keys[pygame.K_RIGHT]: player.x -= 5
                if keys[pygame.K_UP]: player.y += 5
                if keys[pygame.K_DOWN]: player.y -= 5

        # Musuh mengejar
        if enemy.x < player.x: enemy.x += enemy_speed
        if enemy.x > player.x: enemy.x -= enemy_speed
        if enemy.y < player.y: enemy.y += enemy_speed
        if enemy.y > player.y: enemy.y -= enemy_speed

        # Gambar objek
        pygame.draw.rect(screen, BLUE, player)
        pygame.draw.rect(screen, ORANGE, enemy)
        for wall in walls:
            pygame.draw.rect(screen, BLACK, wall)

        # Teks skor/nyawa
        score_text = font.render(f"Skor: {score}", True, BLACK)
        level_text = font.render(f"Level: {level}", True, BLACK)
        lives_text = font.render(f"Nyawa: {lives}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 40))
        screen.blit(lives_text, (10, 70))

        # Tabrakan
        if player.colliderect(enemy):
            hit_sound.play()
            lives -= 1
            if lives <= 0:
                draw_text("Game Over!", 60, (200, 0, 0), screen)
                pygame.display.update()
                pygame.time.wait(2000)
                running = False
            else:
                player = create_rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                enemy = create_rect()

        # Naik level tiap 15 detik
        if pygame.time.get_ticks() // 1000 > score and score < 999:
            score += 1
            if score % 10 == 0:
                level += 1
                enemy_speed += 0.5

        # Event keluar
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(FPS)

# Mulai dari menu
main_menu()
