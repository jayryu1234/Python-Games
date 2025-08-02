import pygame, json

class LevelSelect:
    def __init__(self, screen):
        self.screen = screen
        # 레벨 데이터 로드
        with open('lemonoids/assets/levels.json', 'r') as f:
            self.data = json.load(f)
        # 버튼 영역 정의
        self.buttons = {}
        for i in [1,2,3,4, 5]:
            rect = pygame.Rect(200, 20 + (i-1)*120, 400, 100)
            self.buttons[i] = rect

    def draw(self):
        font = pygame.font.Font(None, 48)
        small = pygame.font.Font(None, 32)
        self.screen.fill((20,20,50))
        for level, rect in self.buttons.items():
            # 버튼 배경
            pygame.draw.rect(self.screen, (50,50,100), rect)
            # 레벨 텍스트
            text = font.render(f"LEVEL {level}", True, (255,255,255))
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)
            # 클리어 여부 표시
            if self.data[str(level)]['cleared']:
                chk = small.render("CLEARED", True, (0,255,0))
                self.screen.blit(chk, (rect.right - 120, rect.top + 10))
            # 최고 점수 표시
            hs = self.data[str(level)]['high_score']
            score_txt = small.render(f"Best: {hs}", True, (200,200,200))
            self.screen.blit(score_txt, (rect.left + 10, rect.bottom - 30))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pygame.time.delay(10)
            pos = pygame.mouse.get_pos()
            for level, rect in self.buttons.items():
                if rect.collidepoint(pos):
                    return level  # 선택된 레벨 반환
        return None