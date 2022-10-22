import pygame, sys
from mazeGen import main
from sprites import GameObj, Player, Gold
import time
from random import randint

"""
You are trying to find the exit of this maze while gaining as much gold as possible, you hold three torches, each lasts 3 seconds, they will allow you to see further. 

"""
# from sprites import GameObject
pygame.init()

clock = pygame.time.Clock()
FRAME_RATE = 30
pygame.key.set_repeat(250, 250)
height = 15
width = 20
block_s = 25
screen = pygame.display.set_mode((width * block_s, height * block_s))

pygame.display.set_caption('Maze Game')
maze = main(height, width)
walls = pygame.sprite.Group()

for i in range(0, height):
    for j in range(0, width):
        if (maze[i][j] == 'u'):
            pass
        elif (maze[i][j] == 'c'):
            pos = i, j
        elif maze[i][j] == 'w':
            # pass
            walls.add(GameObj((j * block_s, i * block_s), (block_s, block_s), 'black'))

player = Player([block_s + 1, 1], [block_s - 2, block_s - 2], 'green', walls)
player_g = pygame.sprite.GroupSingle(player)

NUM_GOLD = 10
golds = pygame.sprite.Group()


def checkGold():
    gold = Gold((randint(0, width) * block_s + 1, randint(0, height) * block_s + 1), [block_s - 2, block_s - 2])
    l = 0
    while gold.collision(walls) or gold.pos[0] < 0 or gold.pos[0] > screen.get_width() or gold.pos[1] < 0 or gold.pos[
        1] > screen.get_height():   gold.set_pos((randint(0, width) * block_s + 1, randint(0, height) * block_s + 1))
    golds.add(gold)


for _ in range(NUM_GOLD):
    checkGold()

torchDuration = 0


def main():
    torch_num = 3
    last_time = 0
    gold_collected = 0

    while True:
        if time.time() - last_time >= 3:
            viewSize = 3
        else:
            viewSize = 5
        darkness = [
            [0, 0, player.pos[0] - int(viewSize / 2) * block_s, player.pos[1] + (int(viewSize / 2) + 1) * block_s],
            # top left down
            [player.pos[0] - int(viewSize / 2) * block_s, 0, screen.get_width() * 2,
             player.pos[1] - int(viewSize / 2) * block_s],
            [player.pos[0] + (int(viewSize / 2) + 1) * block_s, player.pos[1] - int(viewSize / 2) * block_s,
             screen.get_width() * 2, screen.get_height() * 2],
            [0, player.pos[1] + (int(viewSize / 2) + 1) * block_s, player.pos[0] + (int(viewSize / 2) + 1) * block_s,
             screen.get_height() * 2]
        ]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move([-1, 0], block_s)
                elif event.key == pygame.K_RIGHT:
                    player.move([1, 0], block_s)
                elif event.key == pygame.K_UP:
                    player.move([0, -1], block_s)
                elif event.key == pygame.K_DOWN:
                    player.move([0, 1], block_s)
                elif event.key == pygame.K_t:
                    if torch_num > 0:
                        viewSize = 5
                        torch_num -= 1
                        last_time = time.time()
                if pygame.sprite.spritecollide(player, golds, True):
                    gold_collected += 1
        screen.fill('light gray')
        walls.draw(screen)
        player_g.draw(screen)
        golds.draw(screen)
        for rect in darkness:
            pygame.draw.rect(screen, 'gray', rect)
        make_text('Torches:' + str(torch_num), 20, 'white', [screen.get_width() - 5 * block_s, block_s])
        make_text('Amount of Gold Collected:' + str(gold_collected), 20, 'white',
                  [screen.get_width() - 11 * block_s, 2 * block_s])
        pygame.display.update()
        clock.tick(FRAME_RATE)
        if player.pos[1] >= screen.get_height():
            print("you won")
            sys.exit()


def make_text(text, text_s, text_c, pos):
    my_font = pygame.font.SysFont('Comic Sans MS', text_s)
    text_surface = my_font.render(str(text), False, text_c)
    screen.blit(text_surface, pos)


if __name__ == '__main__':
    main()