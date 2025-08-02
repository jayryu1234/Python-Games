import pygame

#pygame.mixer.music.load("assets/SFX/BGM_SpamtonCD_perfectloop.wav")
#pygame.mixer.music.play(-1)'

pygame.mixer.init()
VOLUME = 1
SOUND = 0
bgm = {     "COLOR" : ("lemonoids/assets/FF9CAE.wav"),
            'STAGE' : ("lemonoids/assets/SFX/MAIN_THEME.wav"),
            'SPAMTON' : ("lemonoids/assets/SFX/BGM_SpamtonCD_perfectloop.wav"),
            'BLUUDUDE' : ("lemonoids/assets/SFX/BGMFB_BLUUDUDE_CHASE_THEME.wav"),
            'GAMEOVER' : ("lemonoids/assets/SFX/DETERMINATION.wav"),
            #'TITLE' : ("lemonoids/assets/SFX/wat.wav"), # todo get new title main menu and use this for other stages 
            'CHECKER' : ("lemonoids/assets/SFX/CHECKER_DANCE.wav"),
            'HOPES AND DREAMS' : ("lemonoids/assets/SFX/FIELDS_OF_HOPES_AND_DREAMS_LES_GOOO.wav")
        }
sfx = {
            'shoot' : (pygame.mixer.Sound("lemonoids/assets/SFX/laser.wav"),1),
            'S_BANG' : (pygame.mixer.Sound("lemonoids/assets/SFX/S_BANG.wav"), 1),
            'B_BANG' : (pygame.mixer.Sound("lemonoids/assets/SFX/Big_Explosion.wav"), 1),
            "Lemon_hit" : (pygame.mixer.Sound("lemonoids/assets/SFX/lemon_hit.wav"),1.5),
            "TADA" : (pygame.mixer.Sound('lemonoids/assets/SFX/Tada.wav'), 1.3)
        }

def play_bgm(key):
    pygame.mixer.music.load(bgm[key])
    pygame.mixer.music.play(-1)
    
def stop_bgm():
    pygame.mixer.music.stop()
def play_sfx(sound, channel_id):
    channel = pygame.mixer.Channel(channel_id)
    channel.set_volume(0.7)
    if sound in sfx:
        sfx[sound][SOUND].set_volume(sfx[sound][VOLUME])
        channel.play(sfx[sound][SOUND])