from os import listdir
import pkg_resources
import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT, K_SPACE, K_s, K_w, K_a, K_d, K_ESCAPE
import random
import os

def play():

    pygame.init()

    WHITE = 255, 255, 255
    BLACK = 0, 0, 0
    RED = 255, 0, 0
    GREEN = 0, 255, 0
    BLUE = 0, 0, 255

    COLOR = WHITE, RED, GREEN, BLUE

    font = pygame.font.SysFont('Verdana', 20)

    FPS = pygame.time.Clock()

    screen = width, height = 1280, 720

    main_surface = pygame.display.set_mode(screen)

    IMGS_PATH_GOOSE =  pkg_resources.resource_filename('src', 'game/goose/')
    IMGS_PATH_GAME = pkg_resources.resource_filename('src', 'game/')

    # player = pygame.Surface((20, 20))
    # player.fill((WHITE))
    player_imgs = [pygame.image.load(IMGS_PATH_GOOSE + file).convert_alpha() for file in listdir(IMGS_PATH_GOOSE)]
    player = player_imgs[0]
    player_rect = player.get_rect()
    player_speed = 10

    def create_enemy():
        # enemy = pygame.Surface((20, 20))
        # enemy.fill((RED))
        enemy = pygame.image.load(IMGS_PATH_GAME + 'enemy2.png').convert_alpha()
        enemy_rect = pygame.Rect(width + enemy.get_width(), random.randint(0, height - enemy.get_height()), *enemy.get_size())
        enemy_speed = random.randint(6,10)
        return [enemy, enemy_rect, enemy_speed]

    def create_bonus():
        # bonus = pygame.Surface((20, 20))
        # bonus.fill((GREEN))
        bonus = pygame.image.load(IMGS_PATH_GAME + 'bonus2.png').convert_alpha()
        bonus_rect = pygame.Rect(random.randint(0, width - bonus.get_width()), -bonus.get_height(), *bonus.get_size())
        bonus_speed = random.randint(4,7)
        return [bonus, bonus_rect, bonus_speed]

    def create_bomb():
        bomb = pygame.image.load(IMGS_PATH_GAME+'bomb.png').convert_alpha()
        bomb_rect = player_rect
        bomb_speed = random.randint(5,8)
        return [bomb, bomb_rect, bomb_speed]

    def handle_events():
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and bombs != 0:
                    bombss.append(create_bomb())
                    bombs -= 1

    bg = pygame.transform.scale(pygame.image.load(IMGS_PATH_GAME + 'background2.png').convert(), screen)
    bgX = 0
    bgX2 = bg.get_width()
    bg_speed = 5

    CREATE_ENEMY = pygame.USEREVENT + 1 
    pygame.time.set_timer(CREATE_ENEMY, 1000)

    CREATE_BONUS = pygame.USEREVENT + 2
    pygame.time.set_timer(CREATE_BONUS, 2000)

    CHANGE_IMG = pygame.USEREVENT + 3
    pygame.time.set_timer(CHANGE_IMG, 125)

    DEATH_EVENT = pygame.USEREVENT + 4

    lives = 3
    scores = 0
    bombs = 0
    img_index = 0

    enemies = []
    bonuses = []
    bombss = []

    start_screen = True
    is_working = False
    can_create_bomb = True
    game_over = False

    def show_game_over_screen():
        game_over = True
        while game_over:           
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_over = False

            # keyboard.wait('esc')

            custom_image = pygame.image.load(IMGS_PATH_GAME + 'goose_doose.jpg').convert_alpha()
            custom_image_rect = custom_image.get_rect(center=(width // 2, height // 2))
            main_surface.blit(custom_image, custom_image_rect)
                    
            game_over_text = font.render("Гра закінчена!", True, WHITE)
            game_over_rect = game_over_text.get_rect(center=(width // 2 + 150, height // 2 - 100))
            main_surface.blit(game_over_text, game_over_rect)
                    
            extra_text = font.render("Гусак пішов на лікарняний", True, WHITE)
            extra_rect = extra_text.get_rect(center=(width // 2 + 150, height // 2 - 50))
            main_surface.blit(extra_text, extra_rect)

            score_text = font.render("Ваш рахунок: " + str(scores), True, WHITE)
            score_rect = score_text.get_rect(center=(width // 2 + 150, height // 2 ))
            main_surface.blit(score_text, score_rect)
                    
            pygame.display.flip()
        print('The End. Thank for attention.')
        pygame.quit()

        
    while start_screen:
        
        # Код для відображення початкового екрану
        main_surface.blit(bg, (0, 0))
        
        # Власна картинка та напис
        custom_image = pygame.image.load(IMGS_PATH_GAME + 'background.png').convert_alpha()
        custom_image_rect = custom_image.get_rect(center=(width // 2, height // 2))
        main_surface.blit(custom_image, custom_image_rect)

        text = font.render("Натисніть будь-яку клавішу, щоб грати", True, BLACK)
        text_rect = text.get_rect(center=(width // 2, height // 2 + 100))
        main_surface.blit(text, text_rect)

        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                is_working = False
            if event.type == pygame.KEYDOWN:
                start_screen = False
                is_working = True

    while is_working: 
        
        FPS.tick(60)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                if pressed_keys[K_ESCAPE]:
                    show_game_over_screen()
                    is_working == False
                
            if event.type == CREATE_ENEMY:
                enemies.append(create_enemy())
                if len(enemies) <= 2:
                    enemies.append(create_enemy())
                if scores !=0 and scores % 10 == 0:
                    enemies.append(create_enemy())
                    enemies.append(create_enemy())
                
            if event.type == CREATE_BONUS:
                bonuses.append(create_bonus())
                
            if event.type == CHANGE_IMG:
                img_index += 1
                if img_index == len(player_imgs):
                    img_index = 0
                player = player_imgs[img_index]
            
            if event.type == DEATH_EVENT:
                is_working = False
                game_over = True   
        
        bgX -= bg_speed
        bgX2 -= bg_speed
        
        if bgX < -bg.get_width():
            bgX = bg.get_width()
        
        if bgX2 < -bg.get_width():
            bgX2 = bg.get_width()
        
        main_surface.blit(bg, (bgX, 0))
        main_surface.blit(bg, (bgX2, 0))
        main_surface.blit(player, player_rect)
        main_surface.blit(font.render(str(scores) + " score", True, BLACK), (width - 110, 0))
        main_surface.blit(font.render(str(bombs) + " bombs", True, BLACK), (width - 110, 20))
        main_surface.blit(font.render(str(lives) + " lives", True, BLACK), (width - 110, 40))
        
        pressed_keys = pygame.key.get_pressed()
        
        #контроль ворогів
        for enemy in enemies:
            enemy[1] = enemy[1].move(-enemy[2], 0)
            main_surface.blit(enemy[0], enemy[1])
        # # Зміна координат ворога залежно від його напрямку руху
        #     if enemy[1].top < 0:
        #         enemy[1] = enemy[1].move(-enemy[2], -enemy[2])  # Рух вверх
        #     elif enemy[1].bottom > height:
        #         enemy[1] = enemy[1].move(-enemy[2], enemy[2])  # Рух вниз   
            # elif enemy[1].top < 0:
            #     # Зміна напрямку руху ворога на протилежний
            #     # enemy[1].bottom -= enemy[2]
            #     # # Переміщення ворога вліво
            #     # enemy[1].left -= enemy[2]
            #     #  # Переміщення ворога внизw
            #     enemy[1].top = 0
            
            
            if enemy[1].left < - 200:
                enemies.pop(enemies.index(enemy))
                
            if player_rect.colliderect(enemy[1]):
                enemies.pop(enemies.index(enemy))
                lives -= 1
                if lives == 0:
                    pygame.time.set_timer(DEATH_EVENT, 10)  # Показати екран програшу через 0 секунд
                    
                
        
        #контроль бонусівa
        for bonus in bonuses:
            bonus[1] = bonus[1].move(0, bonus[2])
            main_surface.blit(bonus[0], bonus[1])
            
            if bonus[1].bottom > height + 300:
                bonuses.pop(bonuses.index(bonus))
                
            if player_rect.colliderect(bonus[1]):
                bonuses.pop(bonuses.index(bonus))
                scores += 1
                if  scores % 3 == 0:
                    bombs += 1
        
        for bomb in bombss:
            bomb[1] = bomb[1].move(bomb[2], 2)
            main_surface.blit(bomb[0], bomb[1])
            
            if bomb[1].right > width + 100:
                bombss.pop(bombss.index(bomb))
                
            if bomb[1].colliderect(enemy[1]):
                enemies.pop(enemies.index(enemy))
                bombss.pop(bombss.index(bomb))
            
                
        # Керування
        if (pressed_keys[K_DOWN] or pressed_keys[K_s]) and not player_rect.bottom >= height:
            player_rect = player_rect.move(0, player_speed)
        
        if (pressed_keys[K_UP] or pressed_keys[K_w]) and not player_rect.top <= 0:
            player_rect = player_rect.move(0, -player_speed)
        
        if (pressed_keys[K_RIGHT] or pressed_keys[K_d]) and not player_rect.right >= width:
            player_rect = player_rect.move(player_speed, 0)
        
        if (pressed_keys[K_LEFT] or pressed_keys[K_a]) and not player_rect.left <= 0:
            player_rect = player_rect.move(-player_speed, 0)
        
            
        if pressed_keys[K_SPACE] and bombs != 0 and can_create_bomb:
            bombss.append(create_bomb())
            bombs -= 1
            can_create_bomb = False

        if not pressed_keys[K_SPACE]:
            can_create_bomb = True
        
        if pressed_keys[K_ESCAPE]:
            is_working = False
        
        pygame.display.flip()  

    if game_over:
        show_game_over_screen()
if __name__ == '__main__':
    play()