import pygame, random, modulefinder
from modules.player import Player
from modules.levelselect import LevelSelect
from modules.special_lemon import BOSS_CLEARED
from modules.cutscenes import BossIntroCutscene, BOSS_INTRO_END
from modules.gamestate import GameState
import modules.audio as sfx
import modules.ui as ui
pygame.mixer.pre_init(frequency= 44100, size= 16, channels = 2 , buffer= 1024)
pygame.init()
screen = pygame.display.set_mode((800, 600),pygame.SCALED|pygame.RESIZABLE)
clock = pygame.time.Clock()
data = {}
#wave_manager = WaveManager()

# Sprite groups
meteors = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player((400, 500),bullets)
running = True
level_select = LevelSelect(screen)
selected_level = None
game_state = "TITLE"
game = None
alr_redeemed = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == BOSS_CLEARED:
            sfx.play_sfx('TADA', channel_id= 7)
            game_state = 'TITLE'

        elif game_state == 'LEVEL_SELECT':
            player.health = player.max_health
            meteors.empty()
            bullets.empty()

            lvl = level_select.handle_event(event)
            if lvl and lvl != 3: #todo boss event
                selected_level = lvl
                game = GameState(screen, selected_level)
                game.wave_manager.current_wave = 1
                game.wave_manager.start_time = pygame.time.get_ticks()
                sfx.stop_bgm()
                sfx.play_bgm("STAGE")

                game_state = 'PLAY'
            elif lvl == 3:
                    selected_level = lvl
                    game = GameState(screen, selected_level, meteors, player)
                    game.wave_manager.current_wave = 1
            elif game and game.cutscene_active and event.type == BOSS_INTRO_END and not event.type == BOSS_CLEARED:
                game.wave_manager.start_time = pygame.time.get_ticks()
                bgm = random.randint(1, 7)
                if bgm == 1 or bgm == 5 or bgm == 6 or bgm == 7:
                    sfx.play_bgm('COLOR')
                    print('"i havent found the color of lemons yet"')
                elif bgm == 2:
                    sfx.play_bgm("SPAMTON")
                    print('"NOWS UR CHANCE TO BE A BIG SHOT')
                elif bgm == 3:
                    sfx.play_bgm("HOPES AND DREAMS")
                    print("weehee heee")
                elif bgm == 4:
                    sfx.play_bgm("BLUUDUDE")
                    print("TEAM BLUUDUDE GET IN NOW")
                game_state = 'PLAY'

        elif game_state == 'TITLE':

            if alr_redeemed == 0:
                sfx.stop_bgm()
                alr_redeemed = 1     
        elif game_state == 'PLAY':
            game.wave_manager.handle_event(event, meteors)
            
            if game.check_level_complete():
                game_state = 'LEVEL_COMPLETE'
    # 화면 그리기
    keys = pygame.key.get_pressed()
    if game_state == 'TITLE':

        screen.fill((0,0,0))
        title_img = pygame.image.load('lemonoids/assets/images/lemonoids_title.png').convert_alpha()
        title_rect = title_img.get_rect(center = (400,200))
        screen.blit(title_img,title_rect)

        play_img = pygame.image.load('lemonoids/assets/images/play_button.png').convert_alpha()
        play_img = pygame.transform.scale(
        pygame.image.load("lemonoids/assets/images/play_button.png"),
        (450, 200)
    )
        play_rect = play_img.get_rect(center = (400,400))
        screen.blit(play_img,play_rect)

        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            if play_rect.collidepoint(mouse_pos):
                game_state = 'LEVEL_SELECT'

    elif game and game.cutscene_active and game_state == "LEVEL_SELECT":
        game.boss_intro.update()

        game.boss_intro.draw()

    elif game_state == 'LEVEL_SELECT':
        level_select.draw()
    
    elif game_state == 'PLAY':

        dx = keys[pygame.K_d] - keys[pygame.K_a]
        dy = keys[pygame.K_s] - keys[pygame.K_w]
        player.move(dx, dy)
        player.update()
        
        hits = pygame.sprite.groupcollide(meteors, bullets,False,True)
        for meteor, bs in hits.items():
            meteor.health -= len(bs) * 8 # player damage
            
            if meteor.health <= 0:
                for frag in meteor.split():
                    meteors.add(frag)
                # 적 처치 시 점수 업데이트
                if meteor.size >= 3:
                    sfx.play_sfx("B_BANG", channel_id= 4)
                elif meteor.size < 3:
                    sfx.play_sfx("S_BANG", channel_id= 3)
                game.update_score(meteor.__class__.__name__)
                meteor.kill()
            else:
                sfx.play_sfx("Lemon_hit", channel_id= 2)
   
        if selected_level == 3:
            
            for bullet in bullets:
                offset = (bullet.rect.x - game.boss.rect.x, bullet.rect.y - game.boss.rect.y)
                if game.boss.state == "vulnerable" and game.boss.mask.overlap(bullet.mask, offset):
                    bullet.kill()
                    game.boss.take_damage(5)
                    
            # hits = pygame.sprite.spritecollide(game.boss, bullets, True, collided= None)
            # for _ in hits:
            #     if game.boss.state == "vulnerable":
            #         game.boss.take_damage(4)
            game.boss.update()
        else:
            game.wave_manager.update()
        bullets.update()
        meteors.update()
            

        if not player.invincible:
            for meteor in meteors:
                offset = (meteor.rect.x - player.rect.x, meteor.rect.y - player.rect.y)
                if player.mask.overlap(meteor.mask, offset):
                    player.health -= 1
                    player.invincible = True
                    player.invincible_timer = 120 # 몇 프레임 (1초 60FPS)
                    break
            
            if selected_level == 3:
                offset = (game.boss.rect.x - player.rect.x, game.boss.rect.y - player.rect.y)
                if player.mask.overlap(game.boss.mask, offset):
                    player.health -= 1
                    player.invincible = True
                    player.invincible_timer = 120 # 몇 프레임 (1초 60FPS)
                
        if player.health <= 0:
            game_state = 'GAMEOVER'

        screen.fill((0, 0, 0))
       
        ui.drawWaveUI(screen,game.wave_manager)
        player.draw(screen)
        bullets.draw(screen)
        meteors.draw(screen)

        if selected_level == 3:
            game.boss.draw(screen)
        else:
            game.draw_score()

        # for debug / collide
        for meteor in meteors.sprites():
            #pygame.draw.rect(screen,(255,0,0),meteor.rect,width=1) # 히트박스 표시시
            ui.drawHealthBar(screen,meteor.rect.x+meteor.rect.width//2, meteor.rect.y - 10, meteor.health, meteor.max_health,meteor.size)
        # pygame.draw.rect(screen,(0,255,0),player.rect,width=1)
        # player.draw(screen)

    elif game_state == 'LEVEL_COMPLETE':
        game.handle_level_complete()
        game_state = 'LEVEL_SELECT'

    elif game_state == 'GAMEOVER':
        sfx.stop_bgm()
        sfx.play_bgm('GAMEOVER')
        screen.fill((50,0,0))
        font = pygame.font.Font(None, 74)
        over = font.render("GAME OVER", True,(255,0,0))
        retry = font.render("Press R to Retry", True, (255,255,255))
        screen.blit(over,(250,200))
        screen.blit(retry,(220,300))
        if keys[pygame.K_r]:
            alr_redeemed = 1
            sfx.stop_bgm()
            game_state = 'TITLE'
            
    pygame.display.flip()
    clock.tick(60)
pygame.quit()