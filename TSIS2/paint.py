from datetime import datetime
import pygame
from tools import draw_shape, flood_fill


WIDTH = 1060
HEIGHT = 720
TOOLBAR_HEIGHT = 90
CANVAS_HEIGHT = HEIGHT - TOOLBAR_HEIGHT

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY_BG = (232, 234, 238)
GRAY_BORDER = (180, 185, 195)
BTN_NORMAL = (248, 249, 251)
BTN_ACTIVE = (185, 215, 250)

TOOLS = [
    ("pencil", "Pencil"),
    ("line", "Line"),
    ("rect", "Rect"),
    ("square", "Square"),
    ("circle", "Circle"),
    ("fill", "Fill"),
    ("text", "Text"),
    ("picker", "Picker"),
    ("eraser", "Eraser"),
]

BRUSH_SIZES = [
    (2, "2px [1]"),
    (5, "5px [2]"),
    (10, "10px [3]"),
]

PALETTE = [
    (0, 0, 0),
    (255, 255, 255),
    (220, 38, 38),
    (22, 163, 74),
    (37, 99, 235),
    (234, 179, 8),
    (6, 182, 212),
    (219, 39, 119),
    (249, 115, 22),
    (124, 58, 237),
    (120, 53, 15),
    (107, 114, 128),
]


def save_canvas(canvas):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"paint_{timestamp}.png"
    pygame.image.save(canvas, filename)
    return filename


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Paint - TSIS 2")
    clock = pygame.time.Clock()

    ui_font = pygame.font.SysFont("arial", 15)
    canvas_font = pygame.font.SysFont("arial", 28)

    canvas = pygame.Surface((WIDTH, CANVAS_HEIGHT))
    canvas.fill(WHITE)

    current_tool = "pencil"
    current_color = BLACK
    brush_size = 5

    drawing = False
    start_pos = None
    last_pos = None

    text_active = False
    text_pos = (0, 0)
    text_value = ""

    status_text = ""
    status_timer = 0

    tool_buttons = []
    x_offset = 10
    for tool_id, label in TOOLS:
        rect = pygame.Rect(x_offset, 8, 108, 34)
        tool_buttons.append((tool_id, label, rect))
        x_offset += 115

    size_buttons = []
    x_offset = 10
    for size_val, label in BRUSH_SIZES:
        rect = pygame.Rect(x_offset, 48, 72, 34)
        size_buttons.append((size_val, label, rect))
        x_offset += 78

    color_buttons = []
    x_offset = 260
    for color in PALETTE:
        rect = pygame.Rect(x_offset, 50, 28, 28)
        color_buttons.append((color, rect))
        x_offset += 34

    save_button = pygame.Rect(WIDTH - 135, 48, 125, 34)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if (event.mod & pygame.KMOD_CTRL) and event.key == pygame.K_s:
                    saved_name = save_canvas(canvas)
                    status_text = f"Saved: {saved_name}"
                    status_timer = 180
                    continue

                if text_active:
                    if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        if text_value:
                            rendered = canvas_font.render(text_value, True, current_color)
                            canvas.blit(rendered, text_pos)
                        text_active = False
                        text_value = ""
                    elif event.key == pygame.K_ESCAPE:
                        text_active = False
                        text_value = ""
                    elif event.key == pygame.K_BACKSPACE:
                        text_value = text_value[:-1]
                    else:
                        if event.unicode and event.unicode.isprintable():
                            text_value += event.unicode
                else:
                    if event.key == pygame.K_1:
                        brush_size = 2
                    elif event.key == pygame.K_2:
                        brush_size = 5
                    elif event.key == pygame.K_3:
                        brush_size = 10

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if my < TOOLBAR_HEIGHT:
                    for tool_id, _, rect in tool_buttons:
                        if rect.collidepoint(mx, my):
                            current_tool = tool_id
                            text_active = False
                            text_value = ""
                            break

                    for size_val, _, rect in size_buttons:
                        if rect.collidepoint(mx, my):
                            brush_size = size_val
                            break

                    for color, rect in color_buttons:
                        if rect.collidepoint(mx, my):
                            current_color = color
                            break

                    if save_button.collidepoint(mx, my):
                        saved_name = save_canvas(canvas)
                        status_text = f"Saved: {saved_name}"
                        status_timer = 180
                else:
                    cpos = (mx, my - TOOLBAR_HEIGHT)
                    if current_tool == "fill":
                        flood_fill(canvas, cpos, current_color)
                    elif current_tool == "picker":
                        current_color = tuple(canvas.get_at(cpos)[:3])
                    elif current_tool == "text":
                        if text_active and text_value:
                            rendered = canvas_font.render(text_value, True, current_color)
                            canvas.blit(rendered, text_pos)
                        text_active = True
                        text_pos = cpos
                        text_value = ""
                    elif current_tool == "pencil":
                        drawing = True
                        last_pos = cpos
                        pygame.draw.circle(canvas, current_color, cpos, max(1, brush_size // 2))
                    elif current_tool == "eraser":
                        drawing = True
                        last_pos = cpos
                        pygame.draw.circle(canvas, WHITE, cpos, brush_size)
                    else:
                        drawing = True
                        start_pos = cpos
                        last_pos = cpos

            elif event.type == pygame.MOUSEMOTION and drawing:
                mx, my = event.pos
                cpos = (mx, max(0, my - TOOLBAR_HEIGHT))
                if current_tool in ("pencil", "eraser"):
                    draw_shape(canvas, current_tool, current_color, last_pos, cpos, brush_size)
                    last_pos = cpos
                else:
                    last_pos = cpos

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and drawing:
                mx, my = event.pos
                cpos = (mx, max(0, my - TOOLBAR_HEIGHT))
                if current_tool not in ("pencil", "eraser") and start_pos is not None:
                    draw_shape(canvas, current_tool, current_color, start_pos, cpos, brush_size)
                drawing = False
                start_pos = None
                last_pos = None

        screen.fill(WHITE)
        screen.blit(canvas, (0, TOOLBAR_HEIGHT))

        if drawing and current_tool not in ("pencil", "eraser") and start_pos and last_pos:
            preview = canvas.copy()
            draw_shape(preview, current_tool, current_color, start_pos, last_pos, brush_size)
            screen.blit(preview, (0, TOOLBAR_HEIGHT))

        if text_active:
            rendered = canvas_font.render(text_value, True, current_color)
            draw_x = text_pos[0]
            draw_y = text_pos[1] + TOOLBAR_HEIGHT
            screen.blit(rendered, (draw_x, draw_y))
            if (pygame.time.get_ticks() // 500) % 2 == 0:
                cursor_x = draw_x + rendered.get_width() + 2
                pygame.draw.line(
                    screen,
                    current_color,
                    (cursor_x, draw_y),
                    (cursor_x, draw_y + canvas_font.get_height()),
                    2,
                )

        pygame.draw.rect(screen, GRAY_BG, (0, 0, WIDTH, TOOLBAR_HEIGHT))
        pygame.draw.line(screen, GRAY_BORDER, (0, TOOLBAR_HEIGHT - 1), (WIDTH, TOOLBAR_HEIGHT - 1), 2)

        for tool_id, label, rect in tool_buttons:
            bg = BTN_ACTIVE if current_tool == tool_id else BTN_NORMAL
            pygame.draw.rect(screen, bg, rect, border_radius=5)
            pygame.draw.rect(screen, GRAY_BORDER, rect, 1, border_radius=5)
            txt = ui_font.render(label, True, BLACK)
            screen.blit(txt, txt.get_rect(center=rect.center))

        for size_val, label, rect in size_buttons:
            bg = BTN_ACTIVE if brush_size == size_val else BTN_NORMAL
            pygame.draw.rect(screen, bg, rect, border_radius=5)
            pygame.draw.rect(screen, GRAY_BORDER, rect, 1, border_radius=5)
            txt = ui_font.render(label, True, BLACK)
            screen.blit(txt, txt.get_rect(center=rect.center))

        for color, rect in color_buttons:
            pygame.draw.rect(screen, color, rect, border_radius=4)
            border_w = 3 if current_color == color else 1
            border_c = (30, 100, 220) if current_color == color else BLACK
            pygame.draw.rect(screen, border_c, rect, border_w, border_radius=4)

        pygame.draw.rect(screen, current_color, (680, 50, 34, 28), border_radius=4)
        pygame.draw.rect(screen, BLACK, (680, 50, 34, 28), 1, border_radius=4)

        pygame.draw.rect(screen, BTN_NORMAL, save_button, border_radius=5)
        pygame.draw.rect(screen, GRAY_BORDER, save_button, 1, border_radius=5)
        save_txt = ui_font.render("Save [Ctrl+S]", True, BLACK)
        screen.blit(save_txt, save_txt.get_rect(center=save_button.center))

        if status_timer > 0:
            status_surf = ui_font.render(status_text, True, (22, 120, 50))
            screen.blit(status_surf, (725, 56))
            status_timer -= 1

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()