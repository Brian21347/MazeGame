import pygame
import sys
from mazeGen import maze_gen
from sprites import GameObj, Player, Gold, Ghost
import time
from random import randint

"""
You are trying to find the exit of this maze while gaining as much gold as possible, you hold three torches, each lasts 3 seconds, they will allow you to see further. 

"""
pygame.init()

clock = pygame.time.Clock()
FRAME_RATE = 30
NORMAL_VIEW = 2.5
TORCHED_VIEW = 4.5
TORCH_DURATION = 3
pygame.key.set_repeat(150, 150)
height = 15
width = 20
block_size = 25
screen = pygame.display.set_mode((width * block_size, height * block_size))

pygame.display.set_caption('Maze Game')
maze = maze_gen(height, width)
walls = pygame.sprite.Group()

for i in range(0, height):
    for j in range(0, width):
        if (maze[i][j] == 'u'):
            pass
        elif (maze[i][j] == 'c'):
            pos = i, j
        elif maze[i][j] == 'w':
            walls.add(GameObj((j * block_size, i * block_size),
                      (block_size, block_size), 'black'))

player = Player([block_size + 1, 1], [block_size -
                2, block_size - 2], 'green', walls)
player_g = pygame.sprite.GroupSingle(player)

GHOST_SPEED = 1
ghost = Ghost([screen.get_width() / 2, screen.get_height() / 2],
              [block_size, block_size], "white", player, GHOST_SPEED)
ghost_g = pygame.sprite.GroupSingle(ghost)

NUM_GOLD = 10
golds = pygame.sprite.Group()


def checkGold():
    gold = Gold((randint(0, width) * block_size + 1, randint(0, height)
                * block_size + 1), [block_size - 2, block_size - 2])
    l = 0
    while gold.collision(walls) or gold.pos[0] < 0 or gold.pos[0] > screen.get_width() or gold.pos[1] < 0 or gold.pos[
            1] > screen.get_height():
        gold.set_pos((randint(0, width) * block_size + 1,
                     randint(0, height) * block_size + 1))
    golds.add(gold)


for _ in range(NUM_GOLD):
    checkGold()

torchDuration = 0


def maze_gen():
    torch_num = 3
    last_time = 0
    gold_collected = 0

    while True:
        if time.time() - last_time >= TORCH_DURATION:
            viewSize = NORMAL_VIEW
            ghost.set_speed(GHOST_SPEED)
        else:
            viewSize = TORCHED_VIEW
        darkness = [
            [0, 0, player.pos[0] - viewSize / 2 * block_size,
             player.pos[1] + (viewSize / 2 + 1) * block_size],
            # top left down
            [player.pos[0] - viewSize / 2 * block_size, 0, screen.get_width() * 2,
             player.pos[1] - viewSize / 2 * block_size],
            [player.pos[0] + (viewSize / 2 + 1) * block_size, player.pos[1] - viewSize / 2 * block_size,
             screen.get_width() * 2, screen.get_height() * 2],
            [0, player.pos[1] + (viewSize / 2 + 1) * block_size, player.pos[0] + (viewSize / 2 + 1) * block_size,
             screen.get_height() * 2]
        ]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move([-1, 0], block_size)
                elif event.key == pygame.K_RIGHT:
                    player.move([1, 0], block_size)
                elif event.key == pygame.K_UP:
                    player.move([0, -1], block_size)
                elif event.key == pygame.K_DOWN:
                    player.move([0, 1], block_size)
                elif event.key == pygame.K_t:
                    if torch_num > 0:
                        torch_num -= 1
                        last_time = time.time()
                        ghost.set_speed(GHOST_SPEED * -1)
                if pygame.sprite.spritecollide(player, golds, True):
                    gold_collected += 1
        ghost_g.update()
        screen.fill('light gray')
        walls.draw(screen)
        golds.draw(screen)
        player_g.draw(screen)
        ghost_g.draw(screen)
        if pygame.sprite.spritecollide(player, ghost_g, dokill=False):
            pygame.display.update()
            time.sleep(2)
            print("The ghost got you!")
            sys.exit()
        if player.pos[1] >= screen.get_height():
            pygame.display.update()
            time.sleep(2)
            print(f"You escaped the maze with {gold_collected} gold.")
            sys.exit()
        for rect in darkness:
            pygame.draw.rect(screen, 'gray', rect)
        make_text('Torches:' + str(torch_num), 20, 'white',
                  [screen.get_width() - 5 * block_size, block_size])
        make_text('Amount of Gold Collected:' + str(gold_collected), 20, 'white',
                  [screen.get_width() - 11 * block_size, 2 * block_size])
        pygame.display.update()
        clock.tick(FRAME_RATE)


def make_text(text, text_s, text_c, pos):
    my_font = pygame.font.SysFont('Comic Sans MS', text_s)
    text_surface = my_font.render(str(text), False, text_c)
    screen.blit(text_surface, pos)


if __name__ == '__main__':
    maze_gen()
