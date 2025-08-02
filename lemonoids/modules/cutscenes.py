# modules/cutscenes.py
import pygame

# 컷신 종료 후 발생시키는 커스텀 이벤트
BOSS_INTRO_END = pygame.USEREVENT + 3

class BossIntroCutscene:
    def __init__(self, screen, boss_image, player_image, font=None):
        self.screen = screen
        w, h = screen.get_size()

        # 보스 스프라이트 & 레이블
        self.boss_img = pygame.transform.scale(boss_image, (200, 200))
        self.boss_rect = self.boss_img.get_rect()
        # 시작 좌표: 화면 왼쪽 완전히 바깥
        self.boss_rect.topleft = (-self.boss_rect.width, 20)
        self.boss_label = (font or pygame.font.Font(None, 36)).render(
            "KING LEMON", True, (255, 215, 0))
        self.boss_label_rect = self.boss_label.get_rect(
            topright=(self.boss_rect.right + 10, self.boss_rect.bottom + 10)
        )

        # 플레이어 스프라이트 & 레이블
        self.pl_img = pygame.transform.scale(player_image, (150, 150))
        self.pl_rect = self.pl_img.get_rect()
        # 시작 좌표: 화면 오른쪽 완전히 바깥
        self.pl_rect.bottomright = (w + self.pl_rect.width, h - 20)
        self.pl_label = (font or pygame.font.Font(None, 36)).render(
            "PLAYER", True, (135, 206, 250))
        self.pl_label_rect = self.pl_label.get_rect(
            bottomleft=(self.pl_rect.left - 10, self.pl_rect.top - 10)
        )

        # VS 텍스트
        self.vs_text = (font or pygame.font.Font(None, 72)).render("VS", True, (255, 255, 255))
        self.vs_rect = self.vs_text.get_rect(center=(w//2, h//2))

        # 애니메이션 타임라인
        self.start_time = pygame.time.get_ticks()
        self.phase = 0
        # phase 0: in (0.8s), phase 1: hold (1.0s), phase 2: out (0.8s), phase 3: done
        self.durations = [800, 1000, 800]

    def update(self):
        now = pygame.time.get_ticks() - self.start_time

        # phase 0: slide in
        if now < self.durations[0]:
            t = now / self.durations[0]
            # boss: x from -width → 20
            self.boss_rect.x = int((-self.boss_rect.width) * (1-t) + 5 * t)
            self.boss_label_rect.topleft = (
                self.boss_rect.right + 10,
                self.boss_rect.bottom + 10,
            )
            # player: x from screen+width → screen_width - 170
            sw = self.screen.get_width()
            target_x = sw - self.pl_rect.width - 20
            self.pl_rect.x = int((sw + self.pl_rect.width) * (1-t) + target_x * t)
            self.pl_label_rect.bottomleft = (
                self.pl_rect.left - 10,
                self.pl_rect.top - 10,
            )

        # phase 1: hold
        elif now < sum(self.durations[:2]):
            # 위치 고정
            pass

        # phase 2: slide out
        elif now < sum(self.durations):
            t = (now - sum(self.durations[:2])) / self.durations[2]
            # boss: x from 20 → -width
            self.boss_rect.x = int(20 * (1-t) + (-self.boss_rect.width) * t)
            self.boss_label_rect.topleft = (
                self.boss_rect.right + 10,
                self.boss_rect.bottom + 10,
            )
            # player: x from target → screen + width
            sw = self.screen.get_width()
            target_x = sw - self.pl_rect.width - 20
            self.pl_rect.x = int(target_x * (1-t) + (sw + self.pl_rect.width) * t)
            self.pl_label_rect.bottomleft = (
                self.pl_rect.left - 10,
                self.pl_rect.top - 10,
            )

        else:
            # 완료
            pygame.event.post(pygame.event.Event(BOSS_INTRO_END))
            self.phase = 3

    def draw(self):
        # 반투명 오버레이
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0,0,0,180))
        self.screen.blit(overlay, (0,0))

        # 렌더 순서: boss → label → VS → player → label
        self.screen.blit(self.boss_img, self.boss_rect)
        self.screen.blit(self.boss_label, self.boss_label_rect)
        self.screen.blit(self.vs_text, self.vs_rect)
        self.screen.blit(self.pl_img, self.pl_rect)
        self.screen.blit(self.pl_label, self.pl_label_rect)
