import pygame
def drawHealthBar(surf, x, y, current, maximum, size):
    BAR_WIDTH = 40 * size
    BAR_HEIGHT = 5 *size
    
    pygame.draw.rect(surf, (100, 100, 100), (x-BAR_WIDTH//2, y, BAR_WIDTH, BAR_HEIGHT))
    
    ratio = max(0, min(current / maximum, 1.0))
    
    pygame.draw.rect(surf, (0, 255, 0), (x - BAR_WIDTH//2, y, BAR_WIDTH*ratio, BAR_HEIGHT))

def drawWaveUI(surf, wave_manager):
    font = pygame.font.Font(None, 36)
    
    

    elapsed = pygame.time.get_ticks() - wave_manager.start_time
    if wave_manager.level == 3:
        _font = pygame.font.Font(None, 45)
        __font = pygame.font.Font(None, 20)
        state_font = pygame.font.Font(None, 40)
        higer_text = __font.render(f"BEST THEMES EVER", True, (255, 255, 255))
        other_text = _font.render(f"KING LEMON", True, (255, 255, 255))
        surf.blit(other_text, (300, 70))
        surf.blit(higer_text, (336, 50))
        state = state_font.render(f"Boss state:", True, (0, 177, 0))
        surf.blit(state, (30, 50))
    elif wave_manager.level != 3:
        duration = wave_manager.wave_duration[wave_manager.level].get(wave_manager.current_wave, 1)
        ratio = min(elapsed / duration, 1.0)
        text = font.render(f"Wave {wave_manager.current_wave}", True, (255, 255, 255))
        surf.blit(text, (10, 10))

        pygame.draw.rect(surf, (100, 100, 100), (10, 50, 200, 10))
        pygame.draw.rect(surf, (0, 200, 0), (10, 50, 200*ratio, 10))

