import pgzrun
import sys
import random
from pygame.rect import Rect

WIDTH = 800
HEIGHT = 600
TILE_SIZE = 50

game_state = "menu"
game_move = False
player_moving = False
music_on = True
music.play("game_music")
music.playing = True

stage = 0
lives = 3

stages = [
    {
        "name": "The Jungle",
        "background": (179, 104, 75),
        "walls": "trees",
        "map": [
            "################",
            "#P  #     #   E#",
            "#   #   ### ####",
            "#       #      #",
            "###     #  #####",
            "#              #",
            "#  #  #   ######",
            "#  ####   #   G#",
            "#  #  #   #  ###",
            "#  ## ##       #",
            "#E         ##  #",
            "################",
        ],
    },
    {
        "name": "The Ice",
        "background": (69, 170, 242),
        "walls": "ice_cubes",
        "map": [
            "################",
            "#P ##         E#",
            "#  #####  ######",
            "#              #",
            "#  ####  #######",
            "#  #           #",
            "#  # #####  ####",
            "#E #           #",
            "#  ###  #####  #",
            "#    #   ##    #",
            "#    # E  #G   #",
            "################",
        ],
    },
    {
        "name": "The Stone Castle",
        "background": (165, 177, 194),
        "walls": "stones",
        "map": [
            "################",
            "#P       E     #",
            "#  ###  ###   ##",
            "#    #  # #   E#",
            "###            #",
            "#    ###  ###  #",
            "#E             #",
            "#############  #",
            "#              #",
            "###  ########  #",
            "#G         E   #",
            "################",
        ],
    },
    {
        "name": "The Desert",
        "background": (246, 229, 141),
        "walls": "pyramids",
        "map": [
            "################",
            "#E  #         E#",
            "### #   ########",
            "#   #          #",
            "# ##  #  #  ####",
            "#     #        #",
            "#  #  #   ######",
            "#E #  #   #   E#",
            "#  # G#   # ####",
            "#  #####       #",
            "#E         ## P#",
            "################",
        ],
    },
    {
        "name": "The Flames",
        "background": (241, 165, 78),
        "walls": "fire",
        "map": [
            "################",
            "#P            E#",
            "# ###  #########",
            "# #    #      G#",
            "# #  ### # #####",
            "#E#   #E #    E#",
            "####  #####  ###",
            "#     #   #    #",
            "#  #     E#  # #",
            "#  ########  # #",
            "#             E#",
            "################",
        ],
    },
]

walls = []
enemies = []
player = Actor("player_idle", (0, 0))
player.direction = "right"
goal = Actor("goal", (0, 0))
heart_1 = Actor("heart", (20, 35))
heart_2 = Actor("heart", (55, 35))
heart_3 = Actor("heart", (90, 35))
music_off_icon = Actor("music_off", (775, 575))

def load_stage():
    global walls, enemies, player, goal, game_move, player_moving

    game_move = True
    player_moving = False

    walls = []
    enemies = []
    
    for row_idx, row in enumerate(stages[stage]["map"]):
        for col_idx, tile in enumerate(row):
            x, y = col_idx * TILE_SIZE, row_idx * TILE_SIZE
            if tile == "#":
                walls.append(Actor(stages[stage]["walls"], (x + TILE_SIZE//2, y + TILE_SIZE//2)))
            elif tile == "P":
                player.pos = (x + TILE_SIZE//2, y + TILE_SIZE//2)
            elif tile == "E":
                enemies.append(Actor("enemy_idle", (x + TILE_SIZE//2, y + TILE_SIZE//2)))
            elif tile == "G":
                goal.pos = (x + TILE_SIZE//2, y + TILE_SIZE//2)

def draw_menu():
    screen.clear()
    screen.fill((128, 0, 0))
    screen.draw.text("The Zombie Maze", center=(WIDTH//2, HEIGHT//3), fontsize=40, fontname="press_start_2p", color="white", shadow=(1,1))
    controls = """
        Controls:\n\n
        Start Game: SPACE\n
        Move Player: ARROWS\n
        Play/Mute Music/Sounds: M\n
        Exit: ESC
    """
    screen.draw.text(controls, left=5, bottom=(HEIGHT - 20), fontsize=25, color="white")

def draw_stage_init():
    screen.clear()
    screen.draw.text(f"STAGE {stage + 1}\n\n{stages[stage]['name']}", center=(WIDTH//2, HEIGHT//2), fontsize=30, fontname="press_start_2p", color="white")

def draw_game_over():
    screen.clear()
    screen.draw.text("GAME OVER", center=(WIDTH//2, HEIGHT//2), fontsize=50, fontname="press_start_2p", color="white")

def draw_game_finished():
    screen.clear()
    screen.draw.text("YOU DID IT!", center=(WIDTH//2, HEIGHT//4), fontsize=40, fontname="press_start_2p", color="white")
    finish_text = "You outrun all of those zombies and\n"
    finish_text += "find your way out of the maze!\n\n"
    finish_text += "Congratulations and thank you\n"
    finish_text += "for play The Zombie Maze!"
    screen.draw.text(finish_text, center=(WIDTH//2, HEIGHT//2), fontsize=20, fontname="press_start_2p", color="white")
    screen.draw.text("Develop with <3 by Wesley Oliveira", center=(WIDTH//2, HEIGHT//4 * 3), fontsize=20, fontname="press_start_2p", color="white")

def draw():
    screen.clear()
    if game_state == "menu":
        draw_menu()
        if not music_on:
            music_off_icon.draw()
    elif game_state == "start":
        draw_stage_init()
    elif game_state == "game_over":
        draw_game_over()
    elif game_state == "game_finished":
        draw_game_finished()
    elif game_state == "playing":
        screen.fill(stages[stage]["background"])

        for wall in walls:
            wall.draw()
        
        for enemy in enemies:
            enemy.draw()

        goal.draw()
        player.draw()

        screen.draw.text("STAGE "+str(stage + 1), center=(60, 15), fontsize=15, fontname="press_start_2p", color="black")

        heart_1.draw()
        if lives >= 2:
            heart_2.draw()
        if lives >= 3:
            heart_3.draw()

        if not music_on:
            music_off_icon.draw()

def update_player():
    global game_state, game_move, player_moving

    if player_moving or not game_move:
        return

    pos_x = player.x
    pos_y = player.y
    
    if keyboard.left and keyboard.up and not check_collision(player.x - TILE_SIZE, player.y - TILE_SIZE):
        pos_x = player.x - TILE_SIZE
        pos_y = player.y - TILE_SIZE
        player.direction = "left"
    elif keyboard.left and keyboard.up and not check_collision(player.x - TILE_SIZE, player.y + TILE_SIZE):
        pos_x = player.x - TILE_SIZE
        pos_y = player.y + TILE_SIZE
        player.direction = "left"
    elif keyboard.right and keyboard.up and not check_collision(player.x + TILE_SIZE, player.y - TILE_SIZE):
        pos_x = player.x + TILE_SIZE
        pos_y = player.y - TILE_SIZE
        player.direction = "right"
    elif keyboard.right and keyboard.down and not check_collision(player.x + TILE_SIZE, player.y + TILE_SIZE):
        pos_x = player.x + TILE_SIZE
        pos_y = player.y + TILE_SIZE
        player.direction = "right"
    elif keyboard.left and not check_collision(player.x - TILE_SIZE, player.y):
        pos_x = player.x - TILE_SIZE
        player.direction = "left"
    elif keyboard.right and not check_collision(player.x + TILE_SIZE, player.y):
        pos_x = player.x + TILE_SIZE
        player.direction = "right"
    elif keyboard.up and not check_collision(player.x, player.y - TILE_SIZE):
        pos_y = player.y - TILE_SIZE
    elif keyboard.down and not check_collision(player.x, player.y + TILE_SIZE):
        pos_y = player.y + TILE_SIZE

    if (pos_x != player.x or pos_y != player.y):
        player_moving = True 

        future_rect = Rect(pos_x - TILE_SIZE // 2, pos_y - TILE_SIZE // 2, TILE_SIZE, TILE_SIZE)
        if future_rect.collidepoint(goal.x, goal.y):
            set_finished_stage()
        else:
            animate(
                player,
                duration=.3, 
                pos=(pos_x, pos_y),
                on_finished=unlock_movement,
            )
            set_run()

def unlock_movement():
    global player_moving
    player_moving = False

def set_run():
    player.image = "player_run0" if player.direction == "right" else "player_run0_left"
    
    clock.schedule_unique(set_run_1, .1)
    clock.schedule_unique(set_run_2, .2)
    clock.schedule_unique(set_player_normal, .3)

def set_run_1():
    player.image = "player_run1" if player.direction == "right" else "player_run1_left"

def set_run_2():
    player.image = "player_run2" if player.direction == "right" else "player_run2_left"

def set_player_normal():
    player.image = "player_idle" if player.direction == "right" else "player_idle_left"

def set_finished_stage():
    global game_move

    if not game_move:
        return

    game_move = False
    player.image = "player_cheer"
    sounds.victory_moment.play()
    clock.schedule_unique(set_player_normal, 3)
    clock.schedule_unique(prepare_next_stage, 3)

def prepare_next_stage(first_stage=False):
    global stage, game_state

    game_state = "start"
    if stage == 4:
        set_game_finished()
    else:
        if not first_stage:
            stage += 1
        clock.schedule_unique(init_next_stage, 5)

def init_next_stage():
    global game_state

    game_state = "playing"
    load_stage()

def set_player_hit():
    global game_move, game_state, lives

    if not game_move:
        return

    game_move = False
    player.image = "player_hit"
    clock.schedule_unique(set_player_normal, 4)
    if music_on:
        sounds.player_hurt.play()
        sounds.zombie_attack.play()

    lives -= 1
    if lives < 1:
        clock.schedule_unique(set_game_over, 4)
    else:
        clock.schedule_unique(load_stage, 4)

def set_game_over():
    global game_move, game_state, stage, lives

    game_move = False
    game_state = "game_over"
    stage = 0
    lives = 3

    if music_on:
        music.stop()
        music.play("game_over")
        music.playing = True

    clock.schedule_unique(back_to_menu, 10)

def set_game_finished():
    global game_move, game_state, stage, lives, music_on

    game_move = False
    game_state = "game_finished"
    stage = 0
    lives = 3
    
    if music_on:
        music.stop()
        music.play("game_finished")
        music.playing = True

    clock.schedule_unique(back_to_menu, 20)

def back_to_menu():
    global game_state
    game_state = "menu"
    if music_on:
        music.stop()
        music.play("game_music")
        music.playing = True

def check_collision(x, y):
    future_rect = Rect(x - TILE_SIZE // 2, y - TILE_SIZE // 2, TILE_SIZE, TILE_SIZE)
    return any(future_rect.colliderect(wall._rect) for wall in walls)

def move_enemies():
    if not game_move:
        return

    for enemy in enemies:
        pos_x = enemy.x
        pos_y = enemy.y
        future_x = pos_x + TILE_SIZE if player.x > pos_x else pos_x - TILE_SIZE
        future_y = pos_y + TILE_SIZE if player.y > pos_y else pos_y - TILE_SIZE
        distance_x = player.x - pos_x if player.x > pos_x else pos_x - player.x
        distance_y = player.y - pos_y if player.y > pos_y else pos_y - player.y
        collision_x = check_collision(future_x, pos_y)
        collision_y = check_collision(pos_x, future_y)

        if not collision_x and not collision_y:
            if distance_x > distance_y:
                pos_x = future_x
            else:
                pos_y = future_y
        elif not collision_x:
            pos_x = future_x
        elif not collision_y:
            pos_y = future_y

        if pos_x == future_x or pos_y == future_y:
            animate(enemy, duration=.5, pos=(pos_x, pos_y))

            future_rect = Rect(pos_x - TILE_SIZE // 2, pos_y - TILE_SIZE // 2, TILE_SIZE, TILE_SIZE)
            if future_rect.colliderect(player._rect):
                enemy.image = "enemy_attack"

def animate_enemies():
    if not game_move:
        return

    for enemy in enemies:
        if enemy.image == "enemy_idle":
            enemy.image = "enemy_walk1"
        elif enemy.image == "enemy_walk1":
            enemy.image = "enemy_walk2"
        else:
            enemy.image = "enemy_idle"

clock.schedule_interval(move_enemies, 0.5)
clock.schedule_interval(animate_enemies, 0.2)

def toggle_music():
    global music_on
    music_on = not music_on
    if music_on:
        music.play("game_music")
        music.playing = True
    else:
        music.stop()

def on_key_down():
    if keyboard.m:
        toggle_music()
    elif keyboard.escape:
        sys.exit()

def update():
    global game_state, game_move
    
    if game_state == "menu" and keyboard.space:
        prepare_next_stage(True)
    elif not game_move:
        return
    elif any(player.colliderect(enemy) for enemy in enemies):
        set_player_hit()
    else:
        update_player()
        
pgzrun.go()