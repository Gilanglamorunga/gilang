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

# Musik & Suara (uncomment jika file ada)
# pygame.mixer.music.load("background.mp3")
# pygame.mixer.music.play(-1)
# hit_sound = pygame.mixer.Sound("hit.wav")

# Set up layar
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Polisi vs Penjahat")
font = pygame.font.SysFont("Arial", 30)
clock = pygame.time.Clock()

# Fungsi menampilkan teks di tengah layar dengan offset vertikal
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

# Fungsi untuk membuat objek kotak (player/enemy) dengan ukuran dan posisi acak/default
def create_rect(x=None, y=None, size=PLAYER_SIZE):
    if x is None:
        x = random.randint(0, SCREEN_WIDTH - size)
    if y is None:
        y = random.randint(0, SCREEN_HEIGHT - size)
    return pygame.Rect(x, y, size, size)

# Fungsi utama game
def game_loop():
    player = create_rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    enemy = create_rect()
    # Daftar dinding (wall)
    walls = [pygame.Rect(300, 200, 200, 20), pygame.Rect(100, 400, 600, 20)]

    score = 0
    lives = 3
    level = 1
    enemy_speed = 2

    running = True
    while running:
        screen.fill(WHITE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Input pemain
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.x -= 5
        if keys[pygame.K_RIGHT]:
            player.x += 5
        if keys[pygame.K_UP]:
            player.y -= 5
        if keys[pygame.K_DOWN]:
            player.y += 5

        # Batasi pemain agar tidak keluar layar
        player.clamp_ip(screen.get_rect())

        # Deteksi tabrakan dengan dinding, batasi gerakan pemain
        for wall in walls:
            if player.colliderect(wall):
                if keys[pygame.K_LEFT]:
                    player.x += 5
                if keys[pygame.K_RIGHT]:
                    player.x -= 5
                if keys[pygame.K_UP]:
                    player.y += 5
                if keys[pygame.K_DOWN]:
                    player.y -= 5

        # Musuh mengejar pemain
        if enemy.x < player.x:
            enemy.x += enemy_speed
        if enemy.x > player.x:
            enemy.x -= enemy_speed
        if enemy.y < player.y:
            enemy.y += enemy_speed
        if enemy.y > player.y:
            enemy.y -= enemy_speed

        # Gambar objek
        pygame.draw.rect(screen, BLUE, player)
        pygame.draw.rect(screen, ORANGE, enemy)
        for wall in walls:
            pygame.draw.rect(screen, BLACK, wall)

        # Tampilkan skor, level, dan nyawa
        score_text = font.render(f"Skor: {score}", True, BLACK)
        level_text = font.render(f"Level: {level}", True, BLACK)
        lives_text = font.render(f"Nyawa: {lives}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 40))
        screen.blit(lives_text, (10, 70))

        # Cek tabrakan player dan enemy
        if player.colliderect(enemy):
            try:
                hit_sound.play()
            except:
                pass  # Jika sound tidak ada, skip

            lives -= 1
            if lives <= 0:
                draw_text("Game Over!", 60, (200, 0, 0), screen)
                pygame.display.update()
                pygame.time.wait(2000)
                running = False
            else:
                # Reset posisi jika belum game over
                player = create_rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                enemy = create_rect()

        # Update skor dan level berdasarkan waktu
        current_time = pygame.time.get_ticks() // 1000
        if current_time > score and score < 999:
            score += 1
            if score % 10 == 0:
                level += 1
                enemy_speed += 0.5

        pygame.display.update()
        clock.tick(FPS)

    # Kembali ke menu setelah game over
    main_menu()

# Mulai program dari menu utama
main_menu()
