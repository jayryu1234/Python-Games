import pygame
from pathlib import Path
dd = Path(__file__).parent
#pygame.mixer.music.load("assets/SFX/BGM_SpamtonCD_perfectloop.wav")
#pygame.mixer.music.play(-1)'

pygame.mixer.init()
VOLUME = 1
SOUND = 0
bgm = {
            'COLOR' : None,
            'STAGE' : ("assets/SFX/MAIN_THEME.wav"),
            'SPAMTON' : ("assets/SFX/BGM_SpamtonCD_perfectloop.wav"),
            'BLUUDUDE' : ("assets/SFX/BGMFB_BLUUDUDE_CHASE_THEME.wav"),
            'GAMEOVER' : ("assets/SFX/DETERMINATION.wav"),
            'CHECKER' : ("assets/SFX/CHECKER_DANCE.wav"),
            'HOPES AND DREAMS' : ("assets/SFX/FIELDS_OF_HOPES_AND_DREAMS_LES_GOOO.wav")
        }
sfx = {
            'shoot' : (pygame.mixer.Sound(dd._str + "/assets/SFX/laser.wav"),1),
            'S_BANG' : (pygame.mixer.Sound("assets/SFX/S_BANG.wav"), 1),
            'B_BANG' : (pygame.mixer.Sound("assets/SFX/Big_Explosion.wav"), 1),
            "Lemon_hit" : (pygame.mixer.Sound("assets/SFX/lemon_hit.wav"),1.5),
            "TADA" : (pygame.mixer.Sound('assets/SFX/Tada.wav'), 1.3)
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