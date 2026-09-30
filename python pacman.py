import pygame
import sys
import random
import os
from enum import Enum


# ============================================================
# CONSTANTS
# ============================================================

TILE = 24
ROWS, COLS = 21, 19
WIDTH, HEIGHT = COLS * TILE, ROWS * TILE + 40

FPS = 60

# Slower movement
PACMAN_SPEED = 2
GHOST_SPEED = 1.5


# ============================================================
# COLORS
# ============================================================

BLACK   = (0, 0, 0)
WHITE   = (255, 255, 255)
YELLOW  = (255, 235, 59)
BLUE    = (25, 25, 112)
RED     = (255, 82, 82)
PINK    = (255, 143, 171)
CYAN    = (0, 229, 255)
ORANGE  = (255, 160, 0)
FRIGHT  = (33, 33, 222)
GREEN   = (0, 255, 100)


# ============================================================
# MAZE 1
# ============================================================

MAZE_1 = [
    "###################",
    "#........#........#",
    "#o##.###.#.###.##o#",
    "#.................#",
    "#.##.#.#####.#.##.#",
    "#....#...#...#....#",
    "####.###.#.###.####",
    "####.#.......#.####",
    "####.#.##-##.#.####",
    "#......#---#......#",
    "####.#.#####.#.####",
    "####.#.......#.####",
    "####.#.#####.#.####",
    "#........#........#",
    "#.##.###.#.###.##.#",
    "#o..#..........#..#",
    "###.#.#.#####.#.###",
    "###.#.#.....#.#.###",
    "#.....#.###.#.....#",
    "###################",
]


# ============================================================
# MAZE 2
# ============================================================

MAZE_2 = [
    "###################",
    "#........#........#",
    "#o###.###.#.###.##",
    "#.................#",
    "#.###.#.#####.#.###",
    "#.....#...#...#...#",
    "#####.###.#.###.###",
    "####..#.......#..##",
    "####.#.##-##.#.####",
    "#......#---#......#",
    "####.#.#####.#.####",
    "##...#.......#...##",
    "###.#.#####.#.#####",
    "#........#........#",
    "#.###.###.#.###.###",
    "#o....#.......#...#",
    "###.#.#.#####.#.###",
    "###.#.#.....#.#.###",
    "#.....#.###.#.....#",
    "###################",
]


# ============================================================
# DIRECTIONS
# ============================================================

class Dir(Enum):

    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


# ============================================================
# INITIALISE PYGAME
# ============================================================

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT)
)

pygame.display.set_caption(
    "PAC-MAN"
)

clock = pygame.time.Clock()

font = pygame.font.Font(
    None,
    28
)

big_font = pygame.font.Font(
    None,
    64
)


# ============================================================
# SOUND SYSTEM
# ============================================================

ASSETS_FOLDER = "assets"


def load_sound(filename):

    """
    Load a sound from the assets folder.

    If the file doesn't exist, the game continues
    without crashing.
    """

    path = os.path.join(
        ASSETS_FOLDER,
        filename
    )

    if not os.path.exists(path):

        print(
            f"Sound not found: {path}"
        )

        return None

    try:

        return pygame.mixer.Sound(path)

    except pygame.error as error:

        print(
            f"Could not load sound {filename}: {error}"
        )

        return None


# Load all game sounds

waka_sound = load_sound(
    "waka.mp3"
)

start_sound = load_sound(
    "start.mp3"
)

death_sound = load_sound(
    "death.mp3"
)

ghost_sound = load_sound(
    "ghost.mp3"
)

gameover_sound = load_sound(
    "gameover.mp3"
)


# ============================================================
# PLAY SOUND SAFELY
# ============================================================

def play_sound(sound):

    """
    Play a sound if it exists.

    Stops the same sound if it is already playing.
    This prevents sound overlap.
    """

    if sound is not None:

        sound.stop()
        sound.play()


# ============================================================
# HIGH SCORE
# ============================================================

HIGH_SCORE_FILE = "highscore.txt"


def load_high_score():

    if not os.path.exists(
        HIGH_SCORE_FILE
    ):

        return 0

    try:

        with open(
            HIGH_SCORE_FILE,
            "r"
        ) as file:

            return int(
                file.read()
            )

    except:

        return 0


def save_high_score(score):

    with open(
        HIGH_SCORE_FILE,
        "w"
    ) as file:

        file.write(
            str(score)
        )


# ============================================================
# BOARD
# ============================================================

class Board:

    def __init__(
        self,
        layout
    ):

        self.grid = [
            list(row)
            for row in layout
        ]

        self.dots = 0

        for y, row in enumerate(
            self.grid
        ):

            for x, ch in enumerate(
                row
            ):

                if ch in (
                    ".",
                    "o"
                ):

                    self.dots += 1


    def is_wall(
        self,
        x,
        y
    ):

        if (
            0 <= x < COLS
            and
            0 <= y < ROWS
        ):

            return (
                self.grid[y][x]
                == "#"
            )

        return True


    def at(
        self,
        x,
        y
    ):

        if (
            0 <= x < COLS
            and
            0 <= y < ROWS
        ):

            return self.grid[y][x]

        return "#"


    def eat(
        self,
        x,
        y
    ):

        if self.grid[y][x] == ".":

            self.grid[y][x] = " "

            self.dots -= 1

            return "dot"


        if self.grid[y][x] == "o":

            self.grid[y][x] = " "

            self.dots -= 1

            return "power"


        return None


# ============================================================
# ACTOR
# ============================================================

class Actor:

    def __init__(
        self,
        x,
        y,
        color,
        speed
    ):

        self.tile_x = x
        self.tile_y = y

        self.px = x * TILE
        self.py = y * TILE

        self.color = color

        self.speed = speed

        self.dir = None
        self.next_dir = None

        self.mouth = 0


    def tile_centered(self):

        return (
            self.px % TILE == 0
            and
            self.py % TILE == 0
        )


    def can_move(
        self,
        d,
        board
    ):

        if d is None:

            return False

        nx = (
            self.tile_x
            + d.value[0]
        )

        ny = (
            self.tile_y
            + d.value[1]
        )

        return not board.is_wall(
            nx,
            ny
        )


    def update_tile(self):

        self.tile_x = round(
            self.px / TILE
        )

        self.tile_y = round(
            self.py / TILE
        )


    def draw(
        self,
        surf
    ):

        cx = (
            self.px
            + TILE // 2
        )

        cy = (
            self.py
            + TILE // 2
            + 40
        )

        pygame.draw.circle(
            surf,
            self.color,
            (cx, cy),
            TILE // 2 - 2
        )


# ============================================================
# PAC-MAN
# ============================================================

class Pacman(Actor):

    def __init__(
        self,
        x,
        y
    ):

        super().__init__(
            x,
            y,
            YELLOW,
            PACMAN_SPEED
        )


    def move(
        self,
        board
    ):

        if self.tile_centered():

            self.update_tile()


            if (
                self.next_dir
                and
                self.can_move(
                    self.next_dir,
                    board
                )
            ):

                self.dir = self.next_dir


            if not self.can_move(
                self.dir,
                board
            ):

                self.dir = None


        if self.dir:

            self.px += (
                self.dir.value[0]
                * self.speed
            )

            self.py += (
                self.dir.value[1]
                * self.speed
            )

            self.mouth = (
                self.mouth + 1
            ) % 30


    def draw(
        self,
        surf
    ):

        cx = (
            self.px
            + TILE // 2
        )

        cy = (
            self.py
            + TILE // 2
            + 40
        )


        if self.dir == Dir.LEFT:

            base = 180

        elif self.dir == Dir.UP:

            base = 90

        elif self.dir == Dir.DOWN:

            base = 270

        else:

            base = 0


        mouth_angle = (
            30
            + 15
            * abs(
                15 - self.mouth
            )
            // 15
        )


        v1 = pygame.math.Vector2(
            1,
            0
        ).rotate(
            base - mouth_angle
        )


        v2 = pygame.math.Vector2(
            1,
            0
        ).rotate(
            base + mouth_angle
        )


        pygame.draw.circle(
            surf,
            YELLOW,
            (cx, cy),
            TILE // 2 - 2
        )


        pygame.draw.polygon(
            surf,
            BLACK,
            [
                (cx, cy),

                (
                    cx
                    + (TILE // 2)
                    * v1.x,

                    cy
                    + (TILE // 2)
                    * v1.y
                ),

                (
                    cx
                    + (TILE // 2)
                    * v2.x,

                    cy
                    + (TILE // 2)
                    * v2.y
                )
            ]
        )


# ============================================================
# GHOST
# ============================================================

class Ghost(Actor):

    COLORS = [
        RED,
        PINK,
        CYAN,
        ORANGE
    ]


    def __init__(
        self,
        x,
        y,
        idx,
        role="chase"
    ):

        super().__init__(
            x,
            y,
            self.COLORS[idx],
            GHOST_SPEED
        )

        self.home = (
            x,
            y
        )

        self.frightened = 0

        self.in_house = (
            idx != 0
        )

        self.role = role


    def choose_dir(
        self,
        board,
        pac
    ):

        options = [
            d
            for d in Dir
            if self.can_move(
                d,
                board
            )
        ]


        if (
            self.dir
            and len(options) > 1
        ):

            reverse = Dir(
                (
                    -self.dir.value[0],
                    -self.dir.value[1]
                )
            )

            options = [
                d
                for d in options
                if d != reverse
            ]


        if not options:

            return None


        if self.frightened > 0:

            return random.choice(
                options
            )


        # Guard ghosts
        if self.role == "guard":

            centre_x = COLS // 2
            centre_y = ROWS // 2

            best = None

            best_distance = float(
                "inf"
            )


            for d in options:

                nx = (
                    self.tile_x
                    + d.value[0]
                )

                ny = (
                    self.tile_y
                    + d.value[1]
                )


                distance = (
                    (nx - centre_x) ** 2
                    +
                    (ny - centre_y) ** 2
                )


                if (
                    distance
                    < best_distance
                ):

                    best_distance = distance
                    best = d


            return best


        # Chase ghosts

        best = None

        best_distance = float(
            "inf"
        )


        for d in options:

            nx = (
                self.tile_x
                + d.value[0]
            )

            ny = (
                self.tile_y
                + d.value[1]
            )


            distance = (
                (nx - pac.tile_x) ** 2
                +
                (ny - pac.tile_y) ** 2
            )


            if (
                distance
                < best_distance
            ):

                best_distance = distance
                best = d


        return best


    def move(
        self,
        board,
        pac
    ):

        if self.frightened > 0:

            self.frightened -= 1


        if self.tile_centered():

            self.update_tile()

            self.dir = self.choose_dir(
                board,
                pac
            )


        if self.dir:

            self.px += (
                self.dir.value[0]
                * self.speed
            )

            self.py += (
                self.dir.value[1]
                * self.speed
            )


    def respawn(self):

        self.px = (
            self.home[0]
            * TILE
        )

        self.py = (
            self.home[1]
            * TILE
        )

        self.tile_x, self.tile_y = (
            self.home
        )

        self.frightened = 0

        self.dir = None


    def increase_speed(self):

        self.speed += 0.5


    def draw(
        self,
        surf
    ):

        cx = (
            self.px
            + TILE // 2
        )

        cy = (
            self.py
            + TILE // 2
            + 40
        )


        if self.frightened > 0:

            color = FRIGHT

        else:

            color = self.color


        pygame.draw.circle(
            surf,
            color,
            (
                cx,
                cy - 2
            ),
            TILE // 2 - 2
        )


        pygame.draw.rect(
            surf,
            color,
            (
                cx - TILE // 2 + 2,
                cy - 2,
                TILE - 4,
                TILE // 2
            )
        )


        # Eyes

        pygame.draw.circle(
            surf,
            WHITE,
            (
                cx - 5,
                cy - 4
            ),
            3
        )


        pygame.draw.circle(
            surf,
            WHITE,
            (
                cx + 5,
                cy - 4
            ),
            3
        )


        pygame.draw.circle(
            surf,
            BLUE,
            (
                cx - 5,
                cy - 4
            ),
            1
        )


        pygame.draw.circle(
            surf,
            BLUE,
            (
                cx + 5,
                cy - 4
            ),
            1
        )


# ============================================================
# FRUIT
# ============================================================

class Fruit:

    def __init__(self):

        self.x = COLS // 2
        self.y = 10

        self.active = True

        self.timer = 600


    def update(self):

        if not self.active:

            return

        self.timer -= 1

        if self.timer <= 0:

            self.active = False


    def eaten(
        self,
        pac
    ):

        if not self.active:

            return False


        if (
            pac.tile_x == self.x
            and
            pac.tile_y == self.y
        ):

            self.active = False

            return True


        return False


    def draw(
        self,
        surf
    ):

        if not self.active:

            return


        cx = (
            self.x
            * TILE
            + TILE // 2
        )

        cy = (
            self.y
            * TILE
            + TILE // 2
            + 40
        )


        pygame.draw.circle(
            surf,
            RED,
            (
                cx - 5,
                cy + 2
            ),
            6
        )


        pygame.draw.circle(
            surf,
            RED,
            (
                cx + 5,
                cy + 2
            ),
            6
        )


        pygame.draw.line(
            surf,
            GREEN,
            (
                cx,
                cy - 3
            ),
            (
                cx + 4,
                cy - 10
            ),
            2
        )


# ============================================================
# CREATE LEVEL
# ============================================================

def create_level(level):

    if level == 1:

        layout = MAZE_1

    else:

        layout = MAZE_2


    board = Board(
        layout
    )


    pac = Pacman(
        9,
        15
    )


    ghost1 = Ghost(
        8,
        9,
        0,
        "chase"
    )


    ghost2 = Ghost(
        9,
        9,
        1,
        "chase"
    )


    ghost3 = Ghost(
        10,
        9,
        2,
        "guard"
    )


    ghost4 = Ghost(
        9,
        8,
        3,
        "guard"
    )


    ghosts = [
        ghost1,
        ghost2,
        ghost3,
        ghost4
    ]


    return (
        board,
        pac,
        ghosts
    )


# ============================================================
# MAIN
# ============================================================

def main():

    board, pac, ghosts = create_level(
        1
    )


    score = 0
    lives = 3
    level = 1

    state = "starting"

    high_score = load_high_score()

    fruit = Fruit()


    # ========================================================
    # KEYBOARD
    # ========================================================

    KEYMAP = {

        pygame.K_UP: Dir.UP,
        pygame.K_DOWN: Dir.DOWN,
        pygame.K_LEFT: Dir.LEFT,
        pygame.K_RIGHT: Dir.RIGHT,

        pygame.K_w: Dir.UP,
        pygame.K_s: Dir.DOWN,
        pygame.K_a: Dir.LEFT,
        pygame.K_d: Dir.RIGHT
    }


    # ========================================================
    # INITIAL SOUND
    # ========================================================

    if start_sound:

        start_sound.play()


    # Wait until initial sound finishes
    start_time = pygame.time.get_ticks()

    start_duration = 3000

    if start_sound:

        start_duration = (
            start_sound.get_length()
            * 1000
        )


    # ========================================================
    # GAME LOOP
    # ========================================================

    while True:

        clock.tick(FPS)


        # ====================================================
        # EVENTS
        # ====================================================

        for e in pygame.event.get():

            if e.type == pygame.QUIT:

                pygame.quit()
                sys.exit()


            if e.type == pygame.KEYDOWN:

                if e.key in KEYMAP:

                    pac.next_dir = (
                        KEYMAP[e.key]
                    )


                if (
                    e.key == pygame.K_r
                    and
                    state in (
                        "win",
                        "gameover"
                    )
                ):

                    main()

                    return


        # ====================================================
        # STARTING SCREEN
        # ====================================================

        if state == "starting":

            elapsed = (
                pygame.time.get_ticks()
                - start_time
            )


            if elapsed >= start_duration:

                state = "play"


        # ====================================================
        # GAMEPLAY
        # ====================================================

        if state == "play":

            pac.move(
                board
            )


            for ghost in ghosts:

                ghost.move(
                    board,
                    pac
                )


            # =================================================
            # EAT DOT
            # =================================================

            item = board.eat(
                pac.tile_x,
                pac.tile_y
            )


            if item == "dot":

                score += 10

                play_sound(
                    waka_sound
                )


            elif item == "power":

                score += 50

                for ghost in ghosts:

                    ghost.frightened = 400

                play_sound(
                    waka_sound
                )


            # =================================================
            # FRUIT
            # =================================================

            fruit.update()


            if fruit.eaten(pac):

                score += 500


            # =================================================
            # GHOST COLLISION
            # =================================================

            for ghost in ghosts:

                if (
                    ghost.tile_x
                    == pac.tile_x
                    and
                    ghost.tile_y
                    == pac.tile_y
                ):


                    # Ghost is frightened
                    if ghost.frightened > 0:

                        score += 200

                        play_sound(
                            ghost_sound
                        )

                        ghost.respawn()


                    # Pac-Man gets eaten
                    else:

                        lives -= 1

                        play_sound(
                            death_sound
                        )


                        pac = Pacman(
                            9,
                            15
                        )


                        for gh in ghosts:

                            gh.respawn()


                        # Game over
                        if lives <= 0:

                            state = "gameover"

                            play_sound(
                                gameover_sound
                            )


            # =================================================
            # LEVEL COMPLETE
            # =================================================

            if board.dots == 0:

                if level == 1:

                    level = 2


                    board, pac, ghosts = (
                        create_level(
                            level
                        )
                    )


                    # Increase ghost speed
                    for ghost in ghosts:

                        ghost.speed += 0.5


                    fruit = Fruit()


                else:

                    state = "win"


        # ====================================================
        # HIGH SCORE
        # ====================================================

        if score > high_score:

            high_score = score

            save_high_score(
                high_score
            )


        # ====================================================
        # DRAW
        # ====================================================

        screen.fill(
            BLACK
        )


        # ====================================================
        # DRAW MAZE
        # ====================================================

        for y, row in enumerate(
            board.grid
        ):

            for x, ch in enumerate(
                row
            ):

                rect = pygame.Rect(
                    x * TILE,
                    y * TILE + 40,
                    TILE,
                    TILE
                )


                if ch == "#":

                    pygame.draw.rect(
                        screen,
                        BLUE,
                        rect
                    )


                elif ch == ".":

                    pygame.draw.circle(
                        screen,
                        WHITE,
                        rect.center,
                        3
                    )


                elif ch == "o":

                    pygame.draw.circle(
                        screen,
                        WHITE,
                        rect.center,
                        7
                    )


        # ====================================================
        # FRUIT
        # ====================================================

        fruit.draw(
            screen
        )


        # ====================================================
        # HUD
        # ====================================================

        screen.blit(
            font.render(
                f"SCORE {score}",
                True,
                WHITE
            ),
            (10, 8)
        )


        screen.blit(
            font.render(
                f"HIGH {high_score}",
                True,
                WHITE
            ),
            (130, 8)
        )


        screen.blit(
            font.render(
                f"LEVEL {level}",
                True,
                WHITE
            ),
            (250, 8)
        )


        screen.blit(
            font.render(
                f"LIVES {'o' * lives}",
                True,
                YELLOW
            ),
            (WIDTH - 120, 8)
        )


        # ====================================================
        # ACTORS
        # ====================================================

        pac.draw(
            screen
        )


        for ghost in ghosts:

            ghost.draw(
                screen
            )


        # ====================================================
        # STARTING MESSAGE
        # ====================================================

        if state == "starting":

            txt = big_font.render(
                "READY!",
                True,
                YELLOW
            )


            screen.blit(
                txt,
                (
                    WIDTH // 2
                    - txt.get_width() // 2,

                    HEIGHT // 2
                )
            )


        # ====================================================
        # GAME OVER
        # ====================================================

        if state == "gameover":

            txt = big_font.render(
                "GAME OVER",
                True,
                RED
            )


            screen.blit(
                txt,
                (
                    WIDTH // 2
                    - txt.get_width() // 2,

                    HEIGHT // 2 - 30
                )
            )


            small = font.render(
                "Press R to restart",
                True,
                WHITE
            )


            screen.blit(
                small,
                (
                    WIDTH // 2
                    - small.get_width() // 2,

                    HEIGHT // 2 + 40
                )
            )


        # ====================================================
        # WIN
        # ====================================================

        if state == "win":

            txt = big_font.render(
                "YOU WIN!",
                True,
                YELLOW
            )


            screen.blit(
                txt,
                (
                    WIDTH // 2
                    - txt.get_width() // 2,

                    HEIGHT // 2 - 30
                )
            )


            small = font.render(
                "Press R to restart",
                True,
                WHITE
            )


            screen.blit(
                small,
                (
                    WIDTH // 2
                    - small.get_width() // 2,

                    HEIGHT // 2 + 40
                )
            )


        pygame.display.flip()


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    main()