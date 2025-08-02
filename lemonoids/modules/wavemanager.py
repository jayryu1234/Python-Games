import pygame, random
from modules.enemy import Lemon, StrongLemon, SpeedyLemon, HealerLemon, StrongerLemon, SpeedierLemon, SpeedyPlus, BigLemon
BOSS = pygame.USEREVENT + 3
class WaveManager:
    def __init__(self, level):
        self.current_wave = 1
        self.start_time = pygame.time.get_ticks()
        self.wave_duration = {
            1: {
                1: 20_000,
                2: 25_000,
                3: 25_000,
                4: 20_000,
                5: 10_000,
                6: 30_000,
                7: 45_000,
                8: 30_000,
                9: 20_000,
                10: 40_000,
                "BOSS": 999_000
            },
            2: {
                1: 55_000,
                2: 30_000,
                3: 30_000,
                4: 30_000,
                5: 30_000
            },
            3: {1: 999_000

            },
        }
        self.level = level
        self.wave_config = {
            1:{1: {"types":[(Lemon, 1)], "rate": 2500},
                2: {"types":[(Lemon, 0.7), (SpeedyLemon, 0.3)], "rate": 2500},
                3: {"types":[(Lemon, 0.9), (StrongLemon, 0.1)], "rate": 2500},
                4: {"types":[(Lemon, 0.7), (StrongLemon, 0.1), (SpeedyLemon, 0.2)], "rate": 2500},
                5: {"types":[(SpeedyLemon, 1)], "rate": 1500},
                6: {"types": [(StrongLemon, 0.3), (SpeedyLemon, 0.3), (Lemon, 0.4)], "rate" : 3500},
                #da stronger one incoming
                7: {"types": [(StrongerLemon, 1)], "rate" : 15000},
                8: {"types": [(StrongerLemon, 0.1), (StrongLemon, 0.9)], "rate" : 5000},
                9: {"types": [(StrongerLemon, 0.2), (Lemon, 0.8)], "rate" : 4000},
                10: {"types": [(SpeedyLemon, 0.7), (SpeedierLemon, 0.3)], "rate" : 4000},

            },
            2:{
                1: {"types": [(BigLemon, 1)], "rate": 7500},
                2: {"types": [(StrongLemon, 0.5), (Lemon, 0.3), (SpeedyLemon, 0.2)], "rate": 3500},
                3: {"types": [(StrongerLemon, 1)], "rate" : 10000},
                4: {"types": [(SpeedierLemon, 1)], "rate": 3000},
                5: {"types": [(SpeedyPlus, 1)], "rate": 6000}
            },
            3:{"BOSS" : {"types": ["KING_LEMON", 1]}

            }
            
            
        }
        if level == 3: #todo boss event
            self.SPAWN_EVENT = pygame.USEREVENT+ 2
            pass
        else:
            self.SPAWN_EVENT = pygame.USEREVENT+ 2
            pygame.time.set_timer(self.SPAWN_EVENT, self.wave_config[self.level][1]["rate"])

    def update(self):
        elapsed = pygame.time.get_ticks() - self.start_time
        if elapsed >= self.wave_duration[self.level].get(self.current_wave, float('inf')):
            self.next_wave()
    
    def next_wave(self):
        print(f"Wave {self.current_wave} complete!!!")
        if self.current_wave <= max(self.wave_config[self.level].keys()):
            self.current_wave += 1
            self.start_time = pygame.time.get_ticks()
            new_rate = self.wave_config[self.level].get(self.current_wave,{}).get("rate")
            if new_rate:
                pygame.time.set_timer(self.SPAWN_EVENT, new_rate)
        
        #event thingy
    def handle_event(self, event, lemonoid_group):
        
        if event.type == self.SPAWN_EVENT:
            try:
                cfg = self.wave_config[self.level][self.current_wave]
                types, weights = zip(*cfg['types'])
                LemonClass = random.choices(types, weights = weights, k=1)[0]
                lemonoid_group.add(LemonClass(self.randomPos()))
            except KeyError:
                pass

    def randomPos(self):
        side = random.choice(['top','bottom','left','right'])
        w, h = pygame.display.get_surface().get_size()
        if side == 'top': pos = (random.randint(0,w),-20)
        elif side == 'bottom': pos = (random.randint(0,w),h+20)
        elif side == 'left': pos = (-20,random.randint(0,h))
        elif side == 'right': pos = (w+20,random.randint(0,h))
        return pos