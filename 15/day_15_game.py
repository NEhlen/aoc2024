import numpy as np
import pygame
from pygame.locals import *
import pygame.freetype
import sys

pygame.init()
np.set_printoptions(linewidth=800)

file = "15/input.txt"

play = True
save_imgs = False

with open(file, "r") as f:
    plan, moves = f.read().strip().split("\n\n")


def score_boxes(boxes: set[complex]) -> int:
    return sum([int(box.imag) * 100 + int(box.real) for box in boxes])


# process moves
moves = moves.replace("\n", "")
dir_map = {"v": 0 + 1j, "<": -1 + 0j, ">": 1 + 0j, "^": 0 - 1j}
dir_map_reverse = dict(zip(dir_map.values(), dir_map.keys()))
# moves = [dir_map[char_] for char_ in moves]


# modify map
plan = plan.replace("#", "##")
plan = plan.replace("O", "[]")
plan = plan.replace(".", "..")
plan = plan.replace("@", "@.")

plan = np.array([[char_ for char_ in line] for line in plan.split("\n")])
ry, rx = np.where(plan == "@")
starting_pos_robot = rx[0] + 1j * ry[0]

walls = list(zip(*np.where(plan == "#")))
walls = [wall[1] + 1j * wall[0] for wall in walls]
walls = set(walls)

boxes = list(zip(*np.where(plan == "[")))
boxes_l = [box[1] + 1j * box[0] for box in boxes]
boxes_l = set(boxes_l)
boxes_r = [box[1] + 1 + 1j * box[0] for box in boxes]
boxes_r = set(boxes_r)


robot_pos = starting_pos_robot.copy()


def move_character(
    move: str, robot_pos: complex, boxes_l: set[complex], boxes_r: set[complex]
) -> tuple[complex, set[complex], set[complex]]:
    # print(move)
    move = dir_map[move]
    movement_check = True
    boxes_to_move_l = set()
    boxes_to_move_r = set()
    i = 1
    to_check = {robot_pos + move}
    while movement_check:
        i += 1
        cont = False
        for tc in to_check:
            if tc in boxes_l:
                boxes_l = boxes_l - {tc}
                boxes_r = boxes_r - {tc + 1}
                boxes_to_move_l.add(tc)
                boxes_to_move_r.add(tc + 1)
                to_check = to_check.union({tc + move, tc + 1 + move})
                cont = True
            elif tc in boxes_r:
                boxes_l = boxes_l - {tc - 1}
                boxes_r = boxes_r - {tc}
                boxes_to_move_l.add(tc - 1)
                boxes_to_move_r.add(tc)
                to_check = to_check.union({tc - 1 + move, tc + move})
                cont = True
            elif tc in walls:
                movement_check = False
                boxes_l = boxes_l.union(boxes_to_move_l)
                boxes_r = boxes_r.union(boxes_to_move_r)
                cont = True
                break
        if not cont:
            movement_check = False
            robot_pos += move
            boxes_l = boxes_l - boxes_to_move_l
            boxes_l = boxes_l.union({box + move for box in boxes_to_move_l})
            boxes_r = boxes_r - boxes_to_move_r
            boxes_r = boxes_r.union({box + move for box in boxes_to_move_r})
            break
    # for row in print_plan(robot_pos, boxes_l, boxes_r, walls):
    #     print("".join(row))
    return robot_pos, boxes_l, boxes_r


# window is necessary for pygame, but the game is played in terminal
scale_factor = 15
window_height = (plan.shape[0] + 5) * scale_factor
window_width = plan.shape[1] * scale_factor


def load_colormap(cmap: str = "default"):
    if cmap == "default":
        COL_ROBOT = "#555568"
        COL_BOX = "#a0a08b"
        COL_WALL = "#555568"
        COL_WALL_HIGHLIGHT = COL_BOX
        COL_BG = "#e9efec"
        COL_SCORE = COL_ROBOT
        COL_SCOREBOARD = "#211e20"

    elif cmap == "hard":
        COL_ROBOT = "#5fc75d"
        COL_BOX = "#36868f"
        COL_WALL = "#0f052d"
        COL_WALL_HIGHLIGHT = COL_ROBOT
        COL_BG = "#203671"
        COL_SCORE = COL_ROBOT
        COL_SCOREBOARD = "#203671"
    elif cmap == "gb":
        COL_ROBOT = "#405010"
        COL_BOX = "#708028"
        COL_WALL = "#405010"
        COL_WALL_HIGHLIGHT = COL_BOX
        COL_BG = "#d0d058"
        COL_SCORE = COL_BG
        COL_SCOREBOARD = "#405010"

    elif cmap == "hk":
        COL_ROBOT = "#ff8acd"
        COL_BOX = "#ffffff"
        COL_WALL = "#ff8acd"
        COL_WALL_HIGHLIGHT = COL_BOX
        COL_BG = "#4aedff"
        COL_SCORE = COL_BG
        COL_SCOREBOARD = "#b03e80"

    elif cmap == "ff":
        col0 = "#302387"
        col1 = "#ff3796"
        col2 = "#00faac"
        col3 = "#fffdaf"

        COL_ROBOT = col0
        COL_BOX = col1
        COL_WALL = col0
        COL_WALL_HIGHLIGHT = COL_BOX
        COL_BG = col3
        COL_BOX_FILL = col2
        COL_SCORE = col3
        COL_SCOREBOARD = COL_WALL

    elif cmap == "gb2":
        col0 = "#131018"
        col1 = "#382843"
        col2 = "#7c6d80"
        col3 = "#c7c6c6"

        COL_ROBOT = col0
        COL_BOX = col1
        COL_WALL = col0
        COL_WALL_HIGHLIGHT = col2
        COL_BG = col3
        COL_BOX_FILL = col2
        COL_SCORE = col3
        COL_SCOREBOARD = COL_WALL

    return (
        COL_ROBOT,
        COL_BOX,
        COL_BOX_FILL,
        COL_WALL,
        COL_WALL_HIGHLIGHT,
        COL_BG,
        COL_SCORE,
        COL_SCOREBOARD,
    )


(
    COL_ROBOT,
    COL_BOX,
    COL_BOX_FILL,
    COL_WALL,
    COL_WALL_HIGHLIGHT,
    COL_BG,
    COL_SCORE,
    COL_SCOREBOARD,
) = load_colormap("gb2")
window = pygame.display.set_mode((window_width, window_height))
window.fill(COL_BG)


# Create a custom pattern
pattern_size = scale_factor * 200
pattern_surface = pygame.Surface((pattern_size, pattern_size))
pattern_surface.fill(COL_WALL)  # Background color
for i in range(0, pattern_size, 5):
    pygame.draw.line(
        pattern_surface, COL_WALL_HIGHLIGHT, (0, i), (pattern_size, pattern_size + i), 2
    )  # Diagonal line
    pygame.draw.line(
        pattern_surface, COL_WALL_HIGHLIGHT, (i, 0), (pattern_size + i, pattern_size), 2
    )  # Diagonal line

# Pre-generate a large tiled pattern surface
max_width, max_height = (
    window_width,
    window_height,
)  # Large enough to cover any rectangle
tiled_pattern = pygame.Surface((max_width, max_height))

for x in range(0, max_width, pattern_surface.get_width()):
    for y in range(0, max_height, pattern_surface.get_height()):
        tiled_pattern.blit(pattern_surface, (x, y))


def draw_pattern_filled_rect_optimized(surface, rect, pattern_surface):
    # Clip the surface to the rectangle
    surface.set_clip(rect)
    # Blit the pre-tiled pattern to the surface
    surface.blit(pattern_surface, rect.topleft, rect)
    # Remove the clipping
    surface.set_clip(None)


def draw(robot, walls, boxes):
    for wall in walls:
        draw_pattern_filled_rect_optimized(
            window,
            pygame.Rect(
                (wall.real * scale_factor, wall.imag * scale_factor),
                (1 * scale_factor, 1 * scale_factor),
            ),
            tiled_pattern,
        )
    for box in boxes:
        pygame.draw.rect(
            window,
            COL_BOX_FILL,
            pygame.Rect(
                (box.real * scale_factor, box.imag * scale_factor),
                (2 * scale_factor, 1 * scale_factor),
            ),
            border_radius=3,
        )
        pygame.draw.rect(
            window,
            COL_BOX,
            pygame.Rect(
                (box.real * scale_factor, box.imag * scale_factor),
                (2 * scale_factor, 1 * scale_factor),
            ),
            width=2,
            border_radius=3,
        )
    pygame.draw.circle(
        window,
        COL_ROBOT,
        ((robot.real + 0.5) * scale_factor, (robot.imag + 0.5) * scale_factor),
        scale_factor // 2,
    )


FPS = pygame.time.Clock()
GAME_FONT = pygame.freetype.SysFont(pygame.freetype.get_default_font(), 26)
FPS.tick(60)

count = 0
window.fill(COL_BG)
pygame.draw.rect(
    window,
    COL_SCOREBOARD,
    pygame.Rect((0, window_height - 5 * scale_factor, window_width, 5 * scale_factor)),
)
draw(
    robot_pos,
    walls,
    boxes_l,
)
GAME_FONT.render_to(
    window,
    (40, window_height - 4 * scale_factor),
    "GPS Score: " + str(score_boxes(boxes_l)),
    COL_SCORE,
)
pygame.display.update()
pygame.image.save(window, "15/screenshot.png")
try:
    while True:
        if play:
            for event in pygame.event.get():
                if event.type == QUIT or (
                    event.type == KEYDOWN and event.key == K_ESCAPE
                ):
                    print("Quitting Game")
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN and event.key == K_d:
                    robot_pos, boxes_l, boxes_r = move_character(
                        ">", robot_pos, boxes_l, boxes_r
                    )
                if event.type == KEYDOWN and event.key == K_a:
                    robot_pos, boxes_l, boxes_r = move_character(
                        "<", robot_pos, boxes_l, boxes_r
                    )
                if event.type == KEYDOWN and event.key == K_s:
                    robot_pos, boxes_l, boxes_r = move_character(
                        "v", robot_pos, boxes_l, boxes_r
                    )
                if event.type == KEYDOWN and event.key == K_w:
                    robot_pos, boxes_l, boxes_r = move_character(
                        "^", robot_pos, boxes_l, boxes_r
                    )
            window.fill(COL_BG)
            pygame.draw.rect(
                window,
                COL_SCOREBOARD,
                pygame.Rect(
                    (
                        0,
                        window_height - 5 * scale_factor,
                        window_width,
                        5 * scale_factor,
                    )
                ),
            )
            draw(
                robot_pos,
                walls,
                boxes_l,
            )
            GAME_FONT.render_to(
                window,
                (40, window_height - 4 * scale_factor),
                "GPS Score: " + str(score_boxes(boxes_l)),
                COL_SCORE,
            )

            pygame.display.update()

            if save_imgs:
                pygame.image.save(window, f"15/frames/{count:05d}.png")
            count += 1
        else:
            for event in pygame.event.get():
                if event.type == QUIT or (
                    event.type == KEYDOWN and event.key == K_ESCAPE
                ):
                    print("Quitting Game")
                    pygame.quit()
                    sys.exit()

            robot_pos, boxes_l, boxes_r = move_character(
                moves[count], robot_pos, boxes_l, boxes_r
            )

            window.fill(COL_BG)
            pygame.draw.rect(
                window,
                COL_SCOREBOARD,
                pygame.Rect(
                    (
                        0,
                        window_height - 5 * scale_factor,
                        window_width,
                        5 * scale_factor,
                    )
                ),
            )
            draw(
                robot_pos,
                walls,
                boxes_l,
            )
            GAME_FONT.render_to(
                window,
                (40, window_height - 4 * scale_factor),
                "GPS Score: " + str(score_boxes(boxes_l)),
                COL_SCORE,
            )

            pygame.display.update()
            if save_imgs:
                pygame.image.save(window, f"15/frames/{count:05d}.png")
            count += 1
            if count >= len(moves):
                break
finally:
    pygame.quit()
    print("Final Score:", score_boxes(boxes_l))
