import pygame
import random
import math
import modules.audio as sfx
from modules.enemy import (
    Lemon, StrongLemon, BigLemon,
    SpeedyLemon, SpeedierLemon
)


BOSS_CLEARED = pygame.USEREVENT + 1

class SpecialLemon(pygame.sprite.Sprite):
    """
    일반적인 SpecialLemon(미니언) 클래스. random하게 움직이며, 보스 소환물로도 사용됩니다.
    """
    def __init__(self, pos, size=3, img="lemonoid.png"):
        super().__init__()
        self.size = size
        self.image = pygame.transform.scale(
            pygame.image.load("assets/images/" + img),
            (size * 60, size * 40)
        )
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.max_health = size * 20
        self.health = self.max_health
        self.speed = 1
        self._set_random_velocity(min_speed=1)

    def _set_random_velocity(self, min_speed):
        """
        미니언(레몬) 움직임을 랜덤으로 지정합니다.
        """
        while True:
            self.vx = random.uniform(-2, 2)
            self.vy = random.uniform(-2, 2)
            if abs(self.vx) + abs(self.vy) > min_speed:
                break

    def update(self):
        self.rect.x += self.vx * self.speed
        self.rect.y += self.vy * self.speed

        screen_w, screen_h = pygame.display.get_surface().get_size()
        if self.rect.right < 0:
            self.rect.left = screen_w
        if self.rect.left > screen_w:
            self.rect.right = 0
        if self.rect.bottom < 0:
            self.rect.top = screen_h
        if self.rect.top > screen_h:
            self.rect.bottom = 0

    def split(self):
        """
        큰 레몬을 부술 때 작은 조각들로 분리.
        """
        fragments = []
        nums_frag = 0
        if self.size > 2:
            nums_frag = 2
        elif self.size == 2:
            nums_frag = 3

        for _ in range(nums_frag):
            frag = type(self)(self.rect.center, self.size - 1)
            fragments.append(frag)
        return fragments


class KingLemon(pygame.sprite.Sprite):
    """
    보스 “King Lemon” 클래스. 떠다니기, 패턴 안내, 랜덤 패턴 반복, 취약 상태 연출 포함.
    """
    def __init__(self, pos, meteors_group, player):
        super().__init__()
        # 이미지 & 폰트
        self.base_image = pygame.transform.scale(
            pygame.image.load("assets/images/king_Lemon.png").convert_alpha(),
            (273, 234)
        )
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.font = pygame.font.Font(None, 48)

        # 참조
        self.player = player
        self.meteors_group = meteors_group

        # 위치 & 떠다니기
        self.original_pos = pygame.Vector2(pos)
        self.float_timer = pygame.time.get_ticks()

        # 체력 & 페이즈
        self.max_health = 100
        self.health = self.max_health
        self.phase = 1

        # 상태 머신
        self.state = "idle"          # idle → announce → start_* → update_* → vulnerable → idle
        self.next_state = None
        self.announce_start = 0
        self.announce_text = ""

        # 소환 관련
        self.current_summon_id = 0
        self.minions = pygame.sprite.Group()

        # 돌진 관련
        self.charge_count = 0
        self.charge_substate = None
        self.charge_speed = 8
        self.charge_target = None
        self.charging_wait_start = 0

        # 발사 관련
        self.fire_count = 0
        self.fire_cooldown = 200
        self.last_fire_time = 0

        # 취약 상태
        self.vulnerable_start = 0
        self.vulnerable_duration = 4500

        # 초기 무적
        self.invincible = True

    def update(self):
        now = pygame.time.get_ticks()
        # phase 체크
        if self.health <= self.max_health * 0.5:
            self.phase = 2
        elif self.health <= self.max_health * 0:
            self.phase = 3

        # 떠다니기 모션
        if self.state not in ["charging", "charging_wait","charging_ready"]:
            dt = (now - self.float_timer) / 1000.0
            offset = math.sin(dt * math.pi * 2) * 10
            self.rect.centery = self.original_pos.y + offset

        # 상태 머신
        if self.state == "idle":
            self.invincible = True
            self._choose_and_announce()

        elif self.state == "announce":
            if now - self.announce_start >= 1000:
                # 안내 끝, 패턴 시작
                self.state = self.next_state
                getattr(self, f"_start_{self.next_state}")()

        elif self.state.startswith("summon"):
            self._update_summon()

        elif self.state.startswith("charging"):
            if self.state == "charging_ready":
                self._start_charging_ready()
            elif self.state == "charging":
                self._update_charging()
                
            elif self.state == "charging_wait":
                if now - self.charging_wait_start >= 2000:
                    self._enter_vulnerable()

        elif self.state == "firing":
            self._update_firing()

        elif self.state == "vulnerable":
            if now - self.vulnerable_start >= self.vulnerable_duration:
                self.state = "idle"

        # 미니언 업데이트
        self.minions.update()

    def draw(self, surf):
        # 취약 상태 연출
        if self.state == "vulnerable":
            pygame.draw.circle(
                surf, (255, 255, 0),
                self.rect.center,
                max(self.rect.width, self.rect.height)//2 + 10,
                5
            )
        # 보스
        surf.blit(self.image, self.rect)
        # 안내 문구
        # if self.state == "announce":
        txt = self.font.render(self.announce_text, True, (255,255,255))
        r = txt.get_rect(center=(105, 110))
        surf.blit(txt, r)
        # 미니언
        for m in self.minions:
            surf.blit(m.image, m.rect)
        # 체력바
        self._draw_health_bar(surf)

    def _draw_health_bar(self, surf):
        w, h = pygame.display.get_surface().get_size()
        BAR_W, BAR_H = 400, 20
        x = (w - BAR_W)//2; y = 8
        pct = max(0, min(self.health/self.max_health, 1.0))
        pygame.draw.rect(surf, (50,50,50), (x,y,BAR_W,BAR_H))
        pygame.draw.rect(surf, (200,0,0), (x,y,BAR_W*pct,BAR_H))
        pygame.draw.rect(surf, (255,255,255), (x,y,BAR_W,BAR_H), 2)

    def _choose_and_announce(self):
        opts = ["summon", "firing"] if self.phase==1 else ["summon", "charging_ready","firing"]
        pat = random.choice(opts)
        self.next_state = pat
        self.state = "announce"
        texts = {"summon":"Summon!", "charging_ready" :"Charge!", "firing":"Fire!"}
        self.announce_text = texts[pat]
        self.announce_start = pygame.time.get_ticks()

    # --- Summon ---
    def _start_summon(self):
        self.current_summon_id += 1
        cnt = 5 if self.phase==1 else 7
        weights = ([(Lemon,0.7),(StrongLemon,0.3)] if self.phase==1
                   else [(SpeedyLemon, 0.7),(StrongLemon,0.3)])
        types, probs = zip(*weights)
        for _ in range(cnt):
            Cls = random.choices(types, weights=probs, k=1)[0]
            pos = self._random_edge_pos()
            m = Cls(pos)
            # summon_id 지정
            m.summon_id = self.current_summon_id
            # split 패치
            if hasattr(m, "split"):
                orig = m.split
                def patched_split(orig=orig, parent=m):
                    frags = orig()
                    for f in frags:
                        f.summon_id = parent.summon_id
                    return frags
                m.split = patched_split
            self.minions.add(m)
            self.meteors_group.add(m)
        self.invincible = True
        self.state = f"summon_{self.current_summon_id}"

    def _update_summon(self):
        alive = [spr for spr in self.meteors_group
                 if getattr(spr, "summon_id", None)==self.current_summon_id]
        if not alive:
            self._enter_vulnerable()

    # --- Charging ---
    def _start_charging_ready(self):
        self.charge_count = 0
        self.charge_substate = "go"
        self.charge_target = self.player.rect.center
        self.invincible = True
        self.state = "charging"

    def _update_charging(self):
        if self.charge_substate == "go":
            self._move_towards(self.charge_target, self.charge_speed)
            if self._near_point(self.rect.center, self.charge_target, 10):
                self.charge_substate = "return"
                self.charge_target = self.original_pos
        else:  # return
            self._move_towards(self.charge_target, self.charge_speed)
            if self._near_point(self.rect.center, self.charge_target, 10):
                self.charge_count += 1
                if self.charge_count < 5:
                    self.charge_substate = "go"
                    self.charge_target = self.player.rect.center
                else:
                    self.charging_wait_start = pygame.time.get_ticks()
                    self.state = "charging_wait"

    # --- Firing ---
    def _start_firing(self):
        self.fire_count = 0
        self.last_fire_time = pygame.time.get_ticks()
        self.invincible = True

    def _update_firing(self):
        now = pygame.time.get_ticks()
        req = 3 if self.phase==1 else 5
        if self.fire_count < req and now - self.last_fire_time >= self.fire_cooldown:
            if self.phase == 1:
                cls = SpeedyLemon
            else:
                cls = random.choices(
                    [SpeedyLemon, SpeedierLemon], weights=[0.8,0.2], k=1
                )[0]
            lemon = cls(self.rect.center)
            dx = self.player.rect.centerx - self.rect.centerx
            dy = self.player.rect.centery - self.rect.centery
            dist = math.hypot(dx, dy)
            if dist>0:
                lemon.vx = dx/dist * lemon.speed * 1
                lemon.vy = dy/dist * lemon.speed * 1
            self.meteors_group.add(lemon)
            self.fire_count += 1
            self.last_fire_time = now
        elif self.fire_count >= req:
            self._enter_vulnerable()

    def _enter_vulnerable(self):
        self.state = "vulnerable"
        self.invincible = False
        self.vulnerable_start = pygame.time.get_ticks()
        # 취약 시작 이펙트
        sfx.play_sfx("BOSS_VULN", channel_id=5)

    # 유틸리티
    def _random_edge_pos(self):
        w,h = pygame.display.get_surface().get_size()
        side = random.choice(["top","bottom","left","right"])
        if side=="top":    return (random.randint(0,w), -50)
        if side=="bottom": return (random.randint(0,w), h+50)
        if side=="left":   return (-50, random.randint(0,h))
        return (w+50, random.randint(0,h))

    def _move_towards(self, tgt, spd):
        cx,cy = self.rect.center; tx,ty = tgt
        dx,dy = tx-cx, ty-cy
        dist = math.hypot(dx,dy)
        if dist>0:
            self.rect.x += int(dx/dist * spd)
            self.rect.y += int(dy/dist * spd)

    def _near_point(self, p1, p2, th):
        return math.hypot(p1[0]-p2[0], p1[1]-p2[1]) <= th

    def take_damage(self, amount):
        if self.invincible:
            return
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            for _ in range(5):
                sfx.play_sfx("B_BANG", channel_id=4)
            self.kill()
    
    def kill(self):
        super().kill()
        evt = pygame.event.Event(BOSS_CLEARED, {"Sprite" : self})
        pygame.event.post(evt)