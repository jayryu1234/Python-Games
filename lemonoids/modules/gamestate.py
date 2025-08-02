import pygame, json
from modules.wavemanager import WaveManager
from modules.cutscenes import BossIntroCutscene, BOSS_INTRO_END
from modules.special_lemon import KingLemon
def load_level_data():
    with open('assets/levels.json', 'r') as f:
        return json.load(f)
def save_level_data(data):
    with open('assets/levels.json', 'w') as f:
        json.dump(data, f)

class GameState:
    boss_intro = None
    cutscene_active = False
    boss = None
    def __init__(self, screen, level):
        self.screen = screen
        self.level = level
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        # 레벨 전용 wave_config 로 WaveManager 생성
        self.wave_manager = WaveManager(level=level)
        self.level_data = load_level_data()
        

    def __init__(self, screen, level, meteors=None, _player=None): #init for boss stages!
        self.screen = screen
        self.level = level
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        # 레벨 전용 wave_config 로 WaveManager 생성
        self.wave_manager = WaveManager(level=level)
        self.level_data = load_level_data()

        self.player = _player
        self.meteors = meteors

        self.boss = KingLemon(
            pos= (screen.get_width() // 2, 199),
            meteors_group= meteors,
            player= self.player
        )
        
        #CUTSCENE
        if level == 3:
            self.boss_intro = BossIntroCutscene(screen, self.boss.base_image, _player.original)
            self.cutscene_active = True


    def update_score(self, lemon_type):
        # 적 타입별 점수 부여
        pts = { 'Lemon':10, 'StrongLemon':30, 'SpeedyLemon':20, 'StrongerLemon' : 50, "SpeedierLemon" : 40, "SpeedyPlus" : 60 }
        self.score += pts.get(lemon_type, 0)
        self.draw_score()

    def draw_score(self):
        text = self.font.render(f"Score: {self.score}", True, (255,255,0))
        self.screen.blit(text, (10, 70))

    def check_level_complete(self):
        # 모든 wave 클리어 조건 확인 (wave_manager.current_wave > max)
        try:
            if self.wave_manager.current_wave > max(self.wave_manager.wave_config[self.level].keys()):
                return True
        except TypeError:
            pass
        return False

    def handle_level_complete(self):
        # 레벨 클리어 시 데이터 업데이트 및 화면 렌더링
        if self.level == 3:
            clr_font = pygame.font.Font(None, 72)
            msg = clr_font.render(f"YOU WON. THE END.", True, (255,255,255))
            self.screen.blit(msg, (200,200))
            pygame.display.flip()
            pygame.time.delay(2000)
        else:

            data = self.level_data
            high = data[str(self.level)]['high_score']
            if self.score > high:
                data[str(self.level)]['high_score'] = self.score
            data[str(self.level)]['cleared'] = True
            save_level_data(data)
            # 'LEVEL n CLEAR' 표시
            clr_font = pygame.font.Font(None, 72)
            msg = clr_font.render(f"LEVEL {self.level} CLEAR", True, (255,255,255))
            sc = self.font.render(f"Your: {self.score}  Best: {data[str(self.level)]['high_score']}", True, (255,255,0))
            self.screen.blit(msg, (200,200))
            self.screen.blit(sc, (250,300))
            pygame.display.flip()
            pygame.time.delay(2000)  # 3초 대기