import pygame
import sys

# Inicialização do Pygame
pygame.init()

# Configurações da tela
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Configurações de cores
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Carregando imagens
player_img = pygame.image.load('player1.png')
player_img = pygame.transform.scale(player_img, (90,70)).convert_alpha()
zombie_img = pygame.image.load('zumby.png').convert_alpha()
zombie_img = pygame.transform.scale(zombie_img, (70, 70))

# Variáveis de jogo
score = 0
num_zombies = 5

# Classe para o projétil
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Bullet, self).__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.x += 5
        if self.rect.x > screen_width:
            self.kill()

# Classe para o jogador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = screen_height // 2

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 3
        if keys[pygame.K_RIGHT]:
            self.rect.x += 3
        if keys[pygame.K_SPACE]:
            bullet = Bullet(self.rect.centerx, self.rect.centery)
            all_sprites.add(bullet)
            bullets.add(bullet)

# Classe para os zumbis
class Zombie(pygame.sprite.Sprite):
    def __init__(self, index, start_x):
        super(Zombie, self).__init__()
        self.image = zombie_img
        self.rect = self.image.get_rect()
        self.rect.x = start_x + index * (self.rect.width + 50)
        self.rect.y = screen_height // 2

    def update(self):
        if self.rect.x < player.rect.x:
            self.rect.x += 1
        elif self.rect.x > player.rect.x:
            self.rect.x -= 1
        if self.rect.y < player.rect.y:
            self.rect.y += 1
        elif self.rect.y > player.rect.y:
            self.rect.y -= 1

# Criando grupos de sprites
player = Player()
zombies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group([player])

def spawn_zombies(amount):
    start_x = screen_width  # Inicia zumbis à direita da tela
    for i in range(amount):
        zombie = Zombie(i, start_x)
        zombies.add(zombie)
        all_sprites.add(zombie)

spawn_zombies(num_zombies)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Loop principal do jogo
running = True
while running:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Verifica colisões
    hits = pygame.sprite.groupcollide(zombies, bullets, True, True)
    score += len(hits)

    if pygame.sprite.spritecollideany(player, zombies):
        running = False
        screen.fill(black)
        text = font.render("Game Over", True, red)
        screen.blit(text, (screen_width // 2 - 100, screen_height // 2 - 20))
        pygame.display.flip()
        pygame.time.wait(3000)
        break

    if not zombies:
        num_zombies *= 2
        spawn_zombies(num_zombies)

    screen.fill(black)
    all_sprites.update()
    all_sprites.draw(screen)

    score_text = font.render(f"Score: {score}", True, white)
    screen.blit(score_text, (10, 10))
    pygame.display.flip()

pygame.quit()
sys.exit()
