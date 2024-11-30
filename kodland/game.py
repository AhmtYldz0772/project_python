import random
import pgzero
from pgzero.actor import Actor
from pgzero.screen import Screen
from pgzero import music  # Ses Kütüphanesi

# Ses
is_sound_on = True  # Ses açık mı değil mi?
music.play("oyun_muzigi")

# Ekran -ve hücre
cell = Actor("zemin_3")
screen_width = 9  # Ekranın eni
screen_height = 10  # Ekranın boyu
WIDTH = cell.width * screen_width
HEIGHT = cell.height * screen_height
game_mode = "menu"
TITLE = "Zindanlar"  # ad

# Aktörler
ground1 = Actor("zemin")
ground2 = Actor("zemin")
ground3 = Actor("zemin_2")
background = Actor("background")
game_button = Actor("oyun", (200, 100))
game_button2 = Actor("oyun", (200, 100))
exit_button = Actor("cikis", (200, 200))
sound_on_button = Actor("ses_acik", (400, 50))
close_button = Actor("carpi", (400, 50))

# Harita
game_map = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 2, 2, 0],
    [0, 1, 3, 1, 1, 1, 3, 2, 0],
    [0, 1, 1, 2, 2, 2, 2, 1, 0],
    [0, 1, 1, 2, 3, 1, 2, 1, 0],
    [0, 1, 1, 2, 1, 1, 2, 1, 0],
    [0, 2, 3, 2, 2, 1, 3, 1, 0],
    [0, 2, 2, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
]

# Karakter sınıfı
class Character(Actor):
    def __init__(self, image, position):
        super().__init__(image, position)
        self.health = 100
        self.attack = 20
        self.direction = "right"

    def move(self, x_change, y_change):
        self.x += x_change
        self.y += y_change

    def update_sprite(self):
        if self.direction == "right":
            self.image = "karakter2"
        elif self.direction == "left":
            self.image = "sol"
        elif self.direction == "down":
            self.image = "karakter_down"
        elif self.direction == "up":
            self.image = "karakter_up"


player = Character('karakter2', (cell.width, cell.height))

# Oyun elemanı
hearts = []
swords = []
enemies = []

# Düşmanlar
for i in range(5):
    x = random.randint(60, 290)
    y = random.randint(60, 290)
    enemy = Actor("dusman2", topleft=(x, y))
    enemy.health = random.randint(10, 20)
    enemy.attack = random.randint(5, 10)
    enemy.bonus = random.randint(0, 2)
    enemies.append(enemy)


def draw_map():
    for i, row in enumerate(game_map):
        for j, cell_value in enumerate(row):
            x, y = cell.width * j, cell.height * i
            if cell_value == 0:
                cell.pos = (x, y)
                cell.draw()
            elif cell_value == 1:
                ground1.pos = (x, y)
                ground1.draw()
            elif cell_value == 2:
                ground2.pos = (x, y)
                ground2.draw()
            elif cell_value == 3:
                ground3.pos = (x, y)
                ground3.draw()

# çizimler
def draw():
    if game_mode == "game":
        screen.fill("#2f3542")
        draw_map()
        player.draw()
        close_button.draw()
        screen.draw.text(f"Health: {player.health}", (20, 450), color='white', fontsize=20)
        screen.draw.text(f"Attack: {player.attack}", (350, 450), color='white', fontsize=20)

        for enemy in enemies:
            enemy.draw()

        for heart in hearts:
            heart.draw()

        for sword in swords:
            sword.draw()

    elif game_mode == "menu":
        background.draw()
        game_button.draw()
        sound_on_button.draw()
        exit_button.draw()

    elif game_mode == "end":
        background.draw()
        game_button2.draw()
        screen.draw.text(
            "You Won!", center=(WIDTH // 2, HEIGHT // 2 - 50), fontsize=50, color="green"
        )
        screen.draw.text(
            "Click to return to main menu",
            center=(WIDTH // 2, HEIGHT // 2 + 50),
            fontsize=20,
            color="white",
        )

# hareketler
def on_key_down(key):
    global game_mode
    old_x, old_y = player.x, player.y

    if keyboard.right and player.right + cell.width <= WIDTH:
        player.move(cell.width, 0)
        player.direction = "right"
    elif keyboard.left and player.left - cell.width >= 0:
        player.move(-cell.width, 0)
        player.direction = "left"
    elif keyboard.down and player.bottom + cell.height <= HEIGHT:
        player.move(0, cell.height)
        
    elif keyboard.up and player.top - cell.height >= 0:
        player.move(0, -cell.height)
        

    player.update_sprite()

    enemy_index = player.collidelist(enemies)
    if enemy_index != -1:
        player.x, player.y = old_x, old_y
        enemy = enemies[enemy_index]
        enemy.health -= player.attack
        player.health -= enemy.attack
        if enemy.health <= 0:
            if enemy.bonus == 1:
                hearts.append(Actor("kalp", enemy.pos))
            elif enemy.bonus == 2:
                swords.append(Actor("kiliclar", enemy.pos))
            enemies.pop(enemy_index)

# güncellemeler
def update(dt):
    global is_sound_on, game_mode

    for i in range(len(hearts)):
        if player.colliderect(hearts[i]):
            player.health += 10
            hearts.pop(i)
            break

    for i in range(len(swords)):
        if player.colliderect(swords[i]):
            player.attack += 10
            swords.pop(i)
            break

    if not enemies and player.health > 0:
        game_mode = "end"
        music.stop()

# tıklamalar
def on_mouse_down(pos):
    global game_mode, is_sound_on

    if game_mode == "menu":
        if game_button.collidepoint(pos):
            game_mode = "game"
        elif exit_button.collidepoint(pos):
            exit()
        elif sound_on_button.collidepoint(pos):
            is_sound_on = not is_sound_on
            sound_on_button.image = "ses_kapali" if not is_sound_on else "ses_acik"
            if is_sound_on:
                music.unpause()
            else:
                music.pause()

    elif game_mode == "game":
        if close_button.collidepoint(pos):
            game_mode = "menu"

    elif game_mode == "end":
        if game_button2.collidepoint(pos):
            print("Clicked")
            game_mode = "menu" # son
