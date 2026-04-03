import pygame
import sys
import random
import os

# 1. ІНІЦІАЛІЗАЦІЯ
pygame.init()
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# КОЛЬОРИ
BG_COLOR = (10, 10, 30)
GRID_COLOR = (40, 40, 80)
WHITE = (250, 250, 250)
COLORS = {
    'blue': (40, 90, 255), 'light_blue': (0, 210, 255),
    'purple': (160, 40, 255), 'yellow': (255, 210, 40),
    'red': (255, 40, 40), 'green': (40, 255, 90)
}

# НАЛАШТУВАННЯ
GRID_SIZE = 10
CELL_SIZE = min(SCREEN_WIDTH, SCREEN_HEIGHT) // (GRID_SIZE + 2)
OFFSET_X = (SCREEN_WIDTH - (GRID_SIZE * CELL_SIZE)) // 2
OFFSET_Y = 220 # Сітка трохи вище
HIGH_SCORE_FILE = "high_score.txt"

# ПІДСИЛЕНІ БАЛИ
SHAPES_LIB = [
    ([(0,0)], 25), ([(0,0),(1,0)], 50), ([(0,0),(0,1)], 50),
    ([(0,0),(1,0),(0,1),(1,1)], 100), ([(0,0),(1,0),(2,0)], 75),
    ([(0,0),(0,1),(0,2)], 75), ([(0,0),(1,0),(2,0),(1,1)], 150),
    ([(0,0),(0,1),(0,2),(1,2),(2,2)], 200), ([(0,0),(1,0),(2,0),(3,0),(4,0)], 250)
]

def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        try:
            with open(HIGH_SCORE_FILE, "r") as f: return int(f.read())
        except: return 0
    return 0

def save_high_score(s):
    with open(HIGH_SCORE_FILE, "w") as f: f.write(str(s))

# ЕФЕКТИ
particles = []
class Particle:
    def __init__(self, x, y, color):
        self.x, self.y = x, y
        self.vx, self.vy = random.uniform(-7, 7), random.uniform(-7, 7)
        self.life = 255
        self.color = color
    def update(self):
        self.x += self.vx; self.y += self.vy; self.life -= 15
        return self.life > 0
    def draw(self, surf):
        s = pygame.Surface((8, 8), pygame.SRCALPHA)
        s.fill((*self.color, self.life))
        surf.blit(s, (self.x, self.y))

# КЛАС ФІГУР
class InventoryPiece:
    def __init__(self, index):
        self.index = index
        self.reset()
    def reset(self):
        shape_data = random.choice(SHAPES_LIB)
        self.shape, self.points = shape_data
        self.color_name = random.choice(list(COLORS.keys()))
        self.active = True
        spacing = SCREEN_WIDTH // 4
        self.start_x = spacing * (self.index + 1) - (CELL_SIZE // 2)
        self.start_y = SCREEN_HEIGHT - 450 # ПІДНЯТО ВИЩЕ
        self.pos = [self.start_x, self.start_y]

    def draw(self, surf, is_dragging=False):
        if not self.active: return
        scale = 1.0 if is_dragging else 0.65
        for rx, ry in self.shape:
            draw_pretty_block(surf, self.pos[0] + rx*CELL_SIZE*scale, 
                              self.pos[1] + ry*CELL_SIZE*scale, 
                              int(CELL_SIZE*scale), self.color_name)

def draw_pretty_block(surf, x, y, size, color_name, alpha=255):
    base = COLORS[color_name]
    temp = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.rect(temp, (*base, alpha), (0, 0, size, size), border_radius=6)
    l_c = tuple(min(255, c + 90) for c in base)
    d_c = tuple(max(0, c - 90) for c in base)
    pygame.draw.line(temp, (*l_c, alpha), (3, 3), (size-3, 3), 4)
    pygame.draw.line(temp, (*l_c, alpha), (3, 3), (3, size-3), 4)
    pygame.draw.line(temp, (*d_c, alpha), (size-3, 3), (size-3, size-3), 4)
    pygame.draw.line(temp, (*d_c, alpha), (3, size-3), (size-3, size-3), 4)
    surf.blit(temp, (x, y))

# ГРА
grid_data = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
score = 0
high_score = load_high_score()
inventory = [InventoryPiece(i) for i in range(3)]
dragged_piece = None
font_big = pygame.font.SysFont('Arial', 50, bold=True)
font_small = pygame.font.SysFont('Arial', 30, bold=True)
restart_btn = pygame.Rect(SCREEN_WIDTH - 180, 40, 150, 60)

def check_lines():
    global score, high_score
    rows, cols = [], []
    for r in range(GRID_SIZE):
        if all(grid_data[r][col] for col in range(GRID_SIZE)): rows.append(r)
    for c in range(GRID_SIZE):
        if all(grid_data[row][c] for row in range(GRID_SIZE)): cols.append(c)
    
    num_lines = len(rows) + len(cols)
    if num_lines > 0:
        # ЩЕДРА СИСТЕМА ОЧОК: 500 за одну лінію, 1200 за дві, 2000 за три!
        bonus = {1: 500, 2: 1200, 3: 2000, 4: 3500}.get(num_lines, num_lines * 1000)
        score += bonus
        
        for r in rows:
            for c in range(GRID_SIZE):
                c_v = COLORS[grid_data[r][c]]
                for _ in range(6): particles.append(Particle(OFFSET_X+c*CELL_SIZE, OFFSET_Y+r*CELL_SIZE, c_v))
                grid_data[r][c] = None
        for c in cols:
            for r in range(GRID_SIZE):
                if grid_data[r][c]:
                    c_v = COLORS[grid_data[r][c]]
                    for _ in range(6): particles.append(Particle(OFFSET_X+c*CELL_SIZE, OFFSET_Y+r*CELL_SIZE, c_v))
                    grid_data[r][c] = None
        
        if score > high_score:
            high_score = score
            save_high_score(high_score)

# ЦИКЛ
clock = pygame.time.Clock()
while True:
    screen.fill(BG_COLOR)
    
    # UI
    pygame.draw.rect(screen, (70, 70, 130), restart_btn, border_radius=15)
    screen.blit(font_small.render("RESET", True, WHITE), (restart_btn.x+35, restart_btn.y+15))
    screen.blit(font_big.render(f"SCORE: {score}", True, WHITE), (30, 40))
    screen.blit(font_small.render(f"MAX: {high_score}", True, (200, 200, 200)), (35, 100))

    # Grid
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            x, y = OFFSET_X + c * CELL_SIZE, OFFSET_Y + r * CELL_SIZE
            if grid_data[r][c]: draw_pretty_block(screen, x, y, CELL_SIZE, grid_data[r][c])
            else: pygame.draw.rect(screen, GRID_COLOR, (x, y, CELL_SIZE, CELL_SIZE), 1)

    # Ghost
    if dragged_piece:
        gc = int((dragged_piece.pos[0] + CELL_SIZE//2 - OFFSET_X) // CELL_SIZE)
        gr = int((dragged_piece.pos[1] + CELL_SIZE//2 - OFFSET_Y) // CELL_SIZE)
        can = True
        for rx, ry in dragged_piece.shape:
            if not (0 <= gc+rx < GRID_SIZE and 0 <= gr+ry < GRID_SIZE and grid_data[gr+ry][gc+rx] is None):
                can = False; break
        if can:
            for rx, ry in dragged_piece.shape:
                draw_pretty_block(screen, OFFSET_X+(gc+rx)*CELL_SIZE, OFFSET_Y+(gr+ry)*CELL_SIZE, CELL_SIZE, dragged_piece.color_name, 80)

    # Inventory & Particles
    for p in inventory: p.draw(screen, p == dragged_piece)
    for p in particles[:]:
        if not p.update(): particles.remove(p)
        else: p.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if restart_btn.collidepoint(event.pos):
                grid_data = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
                score = 0
                for p in inventory: p.reset()
            else:
                for p in inventory:
                    if p.active:
                        # Збільшена зона торкання для зручності
                        rect = pygame.Rect(p.pos[0]-20, p.pos[1]-20, CELL_SIZE*3, CELL_SIZE*3)
                        if rect.collidepoint(event.pos):
                            dragged_piece = p; break
        
        if event.type == pygame.MOUSEBUTTONUP and dragged_piece:
            gc = int((dragged_piece.pos[0] + CELL_SIZE//2 - OFFSET_X) // CELL_SIZE)
            gr = int((dragged_piece.pos[1] + CELL_SIZE//2 - OFFSET_Y) // CELL_SIZE)
            can = True
            for rx, ry in dragged_piece.shape:
                if not (0 <= gc+rx < GRID_SIZE and 0 <= gr+ry < GRID_SIZE and grid_data[gr+ry][gc+rx] is None):
                    can = False; break
            if can:
                for rx, ry in dragged_piece.shape: grid_data[gr+ry][gc+rx] = dragged_piece.color_name
                score += dragged_piece.points
                dragged_piece.active = False
                check_lines()
                if all(not p.active for p in inventory):
                    for p in inventory: p.reset()
            dragged_piece.pos = [dragged_piece.start_x, dragged_piece.start_y]
            dragged_piece = None

        if event.type == pygame.MOUSEMOTION and dragged_piece:
            dragged_piece.pos = [event.pos[0]-CELL_SIZE//2, event.pos[1]-CELL_SIZE//2]

    pygame.display.flip()
    clock.tick(60)
