print("ĐANG CHẠY TEST")
from ursina import *
import math 
import json

app = Ursina()

def load_map(map_name):
    with open(map_name, encoding="utf-8") as f_in:
        data = json.load(f_in)

    stage_name = data["stage_name"]
    start_pos = data["start_position"]
    game_map = data["matrix"]

    return (stage_name, start_pos, game_map)

#Config
FLOOR_SIZE = 6
TILE_SIZE = 0.75
BORDER_SIZE = 0.025
TILE_HEIGHT = 0.1
BRIDGE_TILE = {"C": 2, "X": 3, "S": 4}
SPLIT_CAN_PRESS = {"C"}

FLOOR_COLOR = color.rgb32(215, 215, 215)
SPLIT_LOCATION_COLOR = color.rgb32(208, 242, 242)


FRAGILE_COLOR = color.rgb32(247, 120, 47)
SOFT_COLOR = color.rgb32(233, 210, 250)
HEAVY_COLOR = color.rgb32(198, 247, 198)
SPLIT_COLOR = color.rgb32(245, 162, 162)
GOAL_COLOR = color.rgb32(255, 240, 156)

BLOCK_COLOR = color.rgb32(68, 68, 68)
BORDER_COLOR = color.rgb32(255, 255, 255)
SPLIT_INACTIVE_COLOR = color.rgb32(163, 163, 163)
SPLIT_ACTIVE_COLOR = BLOCK_COLOR


SYMBOL_COLOR = color.rgb32(0, 0, 0)
BUTTON_TEXT_COLOR = color.rgb32(158, 17, 36)
BUTTON_COLOR = color.rgb32(0,0,0)

BRIDGE_COLOR = FLOOR_COLOR
LOSE_COLOR = color.rgb32(252, 214, 210)
WIN_COLOR = color.rgb32(136, 247, 171)

DIRECTIONS = {
    "right": (1, 0),
    "left":  (-1, 0),
    "up":    (0, 1),    # away from the camera (+row)
    "down":  (0, -1),
}

STAND, LIE_X, LIE_Z = "stand", "lie_x", "lie_z"
TRANSITIONS = {
    (STAND, "right"): (LIE_X, +1, 0),
    (STAND, "left"):  (LIE_X, -2, 0),
    (STAND, "up"):    (LIE_Z, 0, -2),
    (STAND, "down"):  (LIE_Z, 0, +1),

    (LIE_X, "right"): (STAND, +2, 0),
    (LIE_X, "left"):  (STAND, -1, 0),
    (LIE_X, "up"):    (LIE_X, 0, -1),
    (LIE_X, "down"):  (LIE_X, 0, +1),

    (LIE_Z, "up"):    (STAND, 0, -1),
    (LIE_Z, "down"):  (STAND, 0, +2),
    (LIE_Z, "right"): (LIE_Z, +1, 0),
    (LIE_Z, "left"):  (LIE_Z, -1, 0),
}

#cÁCH XOAY CHO TỪNG HƯỚNG: (AXIS, ANGEL)
ROLL = {
    "right": ("rotation_z", 90),
    "left":  ("rotation_z", -90),
    "up":    ("rotation_x", 90),
    "down":  ("rotation_x", -90),
}

SPLIT_STEPS = {
    "up":    (0, -1),
    "down":  (0, 1),
    "left":  (-1, 0),
    "right": (1, 0),
}

def grid_to_local(COLS, ROWS, CENTER):
    """Map (col, row) -> local position inside the floor parent."""
    return Vec3(
        COLS * TILE_SIZE - CENTER.x,
        0,
        CENTER.z - ROWS * TILE_SIZE
    )

def create_floor(map_data, CENTER, bridge_entities):
    bridge_entities.clear()
    ROWS = len(map_data)
    COLS = len(map_data[0])

    floor_parent = Entity(
        position=CENTER,
        rotation_y=-10
    )

    border_y = TILE_HEIGHT / 2 + 0.002

    for row in range(ROWS):
        for col in range(COLS):

            #Không có tile
            if map_data[row][col] == 0:
                continue

            #Vị trí của tile
            pos = grid_to_local(col, row, CENTER)

            #Màu tile
            if map_data[row][col] == 1:
                tile_color = FLOOR_COLOR

            elif map_data[row][col] == "G":
                tile_color = GOAL_COLOR

            elif map_data[row][col] == "F":
                tile_color = FRAGILE_COLOR

            elif map_data[row][col] == "C":
                tile_color = SOFT_COLOR

            elif map_data[row][col] == "X":
                tile_color = HEAVY_COLOR

            elif map_data[row][col] == "S":
                tile_color = SPLIT_COLOR

            elif map_data[row][col] in (2,3):
                tile_color = BRIDGE_COLOR

            elif map_data[row][col] == 4:
                tile_color = SPLIT_LOCATION_COLOR
            else:
                continue


            first_child = len(floor_parent.children)
            
            #Tạo tile
            Entity(
                parent=floor_parent,
                model="cube",
                scale=Vec3(
                    TILE_SIZE,
                    TILE_HEIGHT,
                    TILE_SIZE
                ),
                position=pos,
                color=tile_color
            )


            #Border trước sau
            for sz in (-TILE_SIZE / 2, TILE_SIZE / 2):

                Entity(
                    parent=floor_parent,
                    model="cube",
                    scale=Vec3(
                        TILE_SIZE,
                        BORDER_SIZE,
                        BORDER_SIZE
                    ),
                    position=Vec3(
                        pos.x,
                        border_y,
                        pos.z + sz
                    ),
                    color=BORDER_COLOR
                )

            #Border trái phải
            for sx in (-TILE_SIZE / 2, TILE_SIZE / 2):
                Entity(
                    parent=floor_parent,
                    model="cube",

                    scale=Vec3(
                        BORDER_SIZE,
                        BORDER_SIZE,
                        TILE_SIZE
                    ),

                    position=Vec3(
                        pos.x + sx,
                        border_y,
                        pos.z
                    ),

                    color=BORDER_COLOR
                )

            if map_data[row][col] in (2, 3):
                parts = floor_parent.children[first_child:]
                for e in parts:
                    e.enabled = False
                bridge_entities[(col, row)] = parts
            


            symbol = None
            if map_data[row][col] == "G":
                symbol = "G"
    
            elif map_data[row][col] == "C":
                symbol = "O"

            elif map_data[row][col] == "X":
                symbol = "X"

            elif map_data[row][col] == "S":
                symbol = "()"

            if symbol is not None:
                Text(
                    parent=floor_parent,
                    text=symbol,
                    position=Vec3(pos.x, TILE_HEIGHT / 2 + 0.02, pos.z),
                    rotation_x=90,
                    origin=(0, 0),
                    scale=TILE_SIZE * 30,
                    color=SYMBOL_COLOR
                )

    return floor_parent

# BLOCK
def create_cube_part(parent, offset):

    SIZE = TILE_SIZE         
    BORDER = BORDER_SIZE
    L = SIZE + BORDER 
    h = SIZE / 2

    #Inside
    Entity(
        parent=parent,
        model="cube",
        scale=Vec3(SIZE, SIZE, SIZE),
        position=offset,
        color=BLOCK_COLOR
    )

    #Ox
    for sy in (-h, h):
        for sz in (-h, h):
            Entity(parent=parent, model="cube",
                   scale=Vec3(L, BORDER, BORDER),
                   position=Vec3(offset.x, offset.y + sy, offset.z + sz),
                   color=BORDER_COLOR)

    #Oz
    for sy in (-h, h):
        for sx in (-h, h):
            Entity(parent=parent, model="cube",
                   scale=Vec3(BORDER, BORDER, L),
                   position=Vec3(offset.x + sx, offset.y + sy, offset.z),
                   color=BORDER_COLOR)

    #Oy
    for sx in (-h, h):
        for sz in (-h, h):
            Entity(parent=parent, model="cube",
                   scale=Vec3(BORDER, L, BORDER),
                   position=Vec3(offset.x + sx, offset.y, offset.z + sz),
                   color=BORDER_COLOR)


class Block:
    LIFT = 0.003    
    MOVE_TIME = 0.175 

    def __init__(self, floor_parent, col, row, CENTER, move_text, game):
        self.CENTER = CENTER
        self.floor = floor_parent
        self.col = col
        self.row = row
        self.state = STAND
        self.moving = False
        self.moves = 0
        self.move_text = move_text
        self.game = game

        #
        self.body = Entity(parent=floor_parent)
        create_cube_part(self.body, Vec3(0, -TILE_SIZE / 2, 0))
        create_cube_part(self.body, Vec3(0,  TILE_SIZE / 2, 0))

        #Pivot = the edge the block rotates around while rolling
        self.pivot = Entity(parent=floor_parent)

        self._snap()

    #state helpers

    def cells(self):
        #Tile mà block đang occupy
        c, r = self.col, self.row
        if self.state == STAND:
            return [(c, r)]
        if self.state == LIE_X:
            return [(c, r), (c + 1, r)]
        return [(c, r), (c, r + 1)]

    def _center(self):
        pts = [grid_to_local(c, r, self.CENTER) for c, r in self.cells()]
        x = sum(p.x for p in pts) / len(pts)
        z = sum(p.z for p in pts) / len(pts)
        height = TILE_SIZE * 2 if self.state == STAND else TILE_SIZE
        y = TILE_HEIGHT / 2 + self.LIFT + height / 2
        return Vec3(x, y, z)

    def _snap(self):
        #Đặt gạch cho đjep
        self.body.parent = self.floor
        self.body.position = self._center()
        if self.state == STAND:
            self.body.rotation = Vec3(0, 0, 0)
        elif self.state == LIE_X:
            self.body.rotation = Vec3(0, 0, 90)
        else:
            self.body.rotation = Vec3(90, 0, 0)
        self.pivot.rotation = Vec3(0, 0, 0)

    def move(self, direction):
        if self.moving:
            return
        
        self.moving = True
        self.moves += 1

        dx, dz = DIRECTIONS[direction]
        new_state, dc, dr = TRANSITIONS[(self.state, direction)]

        pts = [grid_to_local(c, r, self.CENTER) for c, r in self.cells()]
        xs = [p.x for p in pts]
        zs = [p.z for p in pts]
        mid_x = sum(xs) / len(xs)
        mid_z = sum(zs) / len(zs)
        half = TILE_SIZE / 2

        if dx > 0:
            px, pz = max(xs) + half, mid_z
        elif dx < 0:
            px, pz = min(xs) - half, mid_z
        elif dz > 0:
            px, pz = mid_x, max(zs) + half
        else:
            px, pz = mid_x, min(zs) - half

        pivot_pos = Vec3(px, TILE_HEIGHT / 2 + self.LIFT, pz)


        body_pos = self.body.world_position

        self.pivot.position = pivot_pos
        self.pivot.rotation = Vec3(0, 0, 0)

        self.body.parent = self.pivot

        self.body.world_position = body_pos

        #ROLL
        axis, angle = ROLL[direction]
        self.pivot.animate(axis, angle, duration=self.MOVE_TIME, curve=curve.in_out_quad)
        invoke(self._finish, new_state, dc, dr, delay=self.MOVE_TIME)

    def _finish(self, new_state, dc, dr):
        if self.move_text is not None:
            self.move_text.text = f"Moves: {self.moves}"
        self.state = new_state
        self.col += dc
        self.row += dr
        self._snap()   
        self.moving = False

        if self.rules.check_block_fall(self):
            self.game.handle_fall(self)
        elif self.rules.check_win(self):
            self.game.handle_win(self)
        else:
            self.game.on_bridges(self)

    def handle_input(self, key):
        keys = {
            "up arrow": "up", "w": "up",
            "down arrow": "down", "s": "down",
            "left arrow": "left", "a": "left",
            "right arrow": "right", "d": "right",
        }
        if key in keys:
            self.move(keys[key])

class GameRules:
    def __init__(self, map_data):
        self.map = map_data
        self.open_bridges = set()

    def tile_at(self, col, row):
        """trả về giá trị của gạch, None nếu fall"""
        if 0 <= row < len(self.map) and 0 <= col < len(self.map[0]):
            return self.map[row][col]
        return None
    
    def has_tile(self, col, row):
        tile = self.tile_at(col, row)
        
        #Ngoài MAP
        if tile is None:
            return False

        #Không có gạch
        if tile == 0:
            return False

        #Thân cầu C
        if tile == 2:
            return "C" in self.open_bridges

        #Thân cầu X
        if tile == 3:
            return "X" in self.open_bridges

        # 1, 4, G, C, X, S, F đều là tile đang tồn tại
        return True

    def apply_bridges(self, block):
        """Mở/Tắt các cầu mà khối đó kích hoạt. Trả về tập hợp các loại đã được mở/tắt."""
        changed = set()

        for kind in self.check_bridge(block):
            if kind in ("C", "X"):
                if kind in self.open_bridges:
                    self.open_bridges.remove(kind)
                else:
                    self.open_bridges.add(kind)

                changed.add(kind)

            elif kind == "S":
                if "S" not in self.open_bridges:
                    self.open_bridges.add("S")
                    changed.add("S")

        return changed

    
    def check_block_fall(self, block):

        occupied_tiles = block.cells()
        for col, row in occupied_tiles:
            if not self.has_tile(col, row):
                return True

        #Check ô vỡ
        return self.check_break(block)

    def check_break(self, block):
        if block.state != STAND:
            return False
        return self.tile_at(block.col, block.row) == "F"


    def check_bridge(self, block):
        """Returns the set of bridge types the block currently activates."""
        active = set()

        for col, row in block.cells():
            tile = self.tile_at(col, row)

            if tile == "C":                     
                active.add("C")

            #X phải STAND
            elif tile == "X" and block.state == STAND:
                active.add("X")

            #S phải STAND
            elif tile == "S" and block.state == STAND:
                active.add("S")

        return active

    def check_win(self, block):
        if block.state != STAND:
            return False
        
        return self.tile_at(block.col, block.row) == "G"



class Game:
    def __init__(self, start_game, back_to_menu):
        self.start_game = start_game
        self.back_to_menu = back_to_menu

        self.CENTER = Vec3(0, 0, 0)
        self.block = None
        self.background = None
        self.floor_entity = None
        self.game_over = False
        self.game_over_text = None
        self.cur_map_name = None
        self.move_text = None
        self.bridge_entities = {}
        self.active_split = 0
        self.is_split = False
        self.rules = None
        self.split_blocks = []
        self.split_moving = False
        self.saved_moves = 0


    def run_game(self, map_name):
        self.move_text = Text(
            parent=camera.ui,
            text="Moves: 0",
            origin=(0, 0),
            position=(0.7, 0.17),
            scale=1.75,
            color=color.white
        )
        self.cur_map_name = map_name

        (stage_name, start_pos, game_map) = load_map(map_name)
        self.stage_name = Text(
                    parent=camera.ui,
                    text=stage_name,
                    position=(0.7, 0.25),
                    origin=(0, 0),
                    scale=1.95,
                    color=color.white
                )


        ROWS = len(game_map)
        COLS = len(game_map[0])
        self.CENTER = Vec3(
        (COLS - 1) * TILE_SIZE / 2,
        0,
        (ROWS - 1) * TILE_SIZE / 2
    )
        if self.background is None:
            BG_DISTANCE = 100
            bg_height = 2 * BG_DISTANCE * math.tan(math.radians(camera.fov / 2))
            self.background = Entity(
                parent=camera,
                model="quad",
                texture="image_bg.jpg",
                z=BG_DISTANCE,
                scale=(bg_height * max(2, window.aspect_ratio), bg_height),
                unlit=True
            )
        self.background.enabled = True

        self.floor_entity = create_floor(game_map, self.CENTER, self.bridge_entities)
        self.block = Block(self.floor_entity, col=start_pos[1], row=start_pos[0], CENTER=self.CENTER, move_text=self.move_text, game=self)   # covers (2,2) and (2,3)
        rule = GameRules(game_map)
        self.rules = rule
        self.block.rules = rule

        # CAMERA
        # Tile size never changes; only the camera backs off for bigger maps
        extent = max(COLS, ROWS) * TILE_SIZE
        distance = 10 + extent * 1.5
        direction = Vec3(-5, 8.5, -15).normalized()
        camera.position = self.CENTER + direction * distance
        camera.look_at(self.CENTER)


        back_button = Button(
                parent=camera.ui,
                text="BACK",
                x = -0.7899,
                y= 0.42,
                scale=(0.15, 0.08),
                origin=(0,0)
            )

        back_button.on_click = Func(self.back_to_menu)

    def find_split_cells(self):
        cells = []
        for r, line in enumerate(self.rules.map):
            for c, v in enumerate(line):
                if v == 4:
                    cells.append((c, r))
        return cells

    def split_pos(self, col, row):
        pos = grid_to_local(col, row, self.CENTER)
        return Vec3(pos.x, TILE_HEIGHT / 2 + Block.LIFT + TILE_SIZE / 2, pos.z)

    def update_split_highlight(self):
        for i, part in enumerate(self.split_blocks):
            inside = part["entity"].children[0]       # first child = the cube's inside
            inside.color = BLOCK_COLOR if i == self.active_split else SPLIT_INACTIVE_COLOR 

    def split_block(self, block):
        if self.is_split:
            return

        spots = self.find_split_cells()[:2]
        if len(spots) < 2:      #Không có split tiles
            return                            

        self.is_split = True
        self.saved_moves = block.moves

        destroy(block.body)
        destroy(block.pivot)
        self.block = None

        self.split_blocks = []
        self.active_split = 0

        for col, row in spots:
            holder = Entity(parent=self.floor_entity, position=self.split_pos(col, row))
            create_cube_part(holder, Vec3(0, 0, 0))   # same look as the big block
            self.split_blocks.append({"entity": holder, "col": col, "row": row})

        self.update_split_highlight()

    def move_split_block(self, direction):
        if not self.is_split or self.split_moving or self.game_over:
            return

        dcol, drow = SPLIT_STEPS[direction]
        part = self.split_blocks[self.active_split]
        other = self.split_blocks[1 - self.active_split]

        new_col = part["col"] + dcol
        new_row = part["row"] + drow

        # can't move onto the other cube
        if (new_col, new_row) == (other["col"], other["row"]):
            return

        part["col"], part["row"] = new_col, new_row
        self.split_moving = True
        self.saved_moves += 1
        if self.move_text is not None:
            self.move_text.text = f"Moves: {self.saved_moves}"

        #roll: pivot on the bottom edge in the move direction
        dx, dz = DIRECTIONS[direction]            # screen-space direction, same as Block
        half = TILE_SIZE / 2
        entity = part["entity"]
        start = Vec3(entity.position)

        pivot = Entity(
            parent=self.floor_entity,
            position=Vec3(
                start.x + dx * half,
                TILE_HEIGHT / 2 + Block.LIFT,
                start.z + dz * half
            )
        )
        entity.parent = pivot
        entity.position = start - pivot.position  # keeps the cube where it was
        entity.rotation = Vec3(0, 0, 0)

        axis, angle = ROLL[direction]
        pivot.animate(axis, angle, duration=0.2, curve=curve.in_out_quad)
        invoke(self.finish_split_roll, part, pivot, delay=0.2)

    def finish_split_roll(self, part, pivot):
        if not self.is_split or part not in self.split_blocks:
            return

        entity = part["entity"]
        entity.parent = self.floor_entity
        entity.rotation = Vec3(0, 0, 0)          
        entity.position = self.split_pos(part["col"], part["row"])
        destroy(pivot)
        self.split_moving = False

        #Lăn vô cầu đóng / ô trống -> té
        if not self.rules.has_tile(part["col"], part["row"]):
            self.split_fall(part)
            return

        #công tắt dưới block
        self.on_split_bridges(part)
        if self.game_over:
            return

        self.check_split_join()


    def on_split_bridges(self, part):
        tile = self.rules.tile_at(part["col"], part["row"])

        if tile not in SPLIT_CAN_PRESS:
            return

        #tắt mở như block bth
        if tile in self.rules.open_bridges:
            self.rules.open_bridges.remove(tile)
        else:
            self.rules.open_bridges.add(tile)

        self.set_bridge_visible(
            self.rules.map,
            tile,
            tile in self.rules.open_bridges
        )

        #check cầu vừa đóng nằm dưới cục block này
        for p in self.split_blocks:
            if not self.rules.has_tile(p["col"], p["row"]):
                self.split_fall(p)
                return


    def split_fall(self, part):
        if self.game_over:
            return

        self.game_over = True
        part["entity"].animate_position(
            part["entity"].position + Vec3(0, -5, 0),
            duration=0.6,
            curve=curve.in_quad
        )
        invoke(self.show_game_over, delay=0.6)


    def check_split_join(self):
        if len(self.split_blocks) != 2:
            return

        first = self.split_blocks[0]
        second = self.split_blocks[1]

        dc = abs(first["col"] - second["col"])
        dr = abs(first["row"] - second["row"])

        #Hai cục nằm cạnh nhau
        if dc + dr == 1:
            self.join_split_blocks()

    def join_split_blocks(self):
        first = self.split_blocks[0]
        second = self.split_blocks[1]

        col1 = first["col"]
        row1 = first["row"]

        col2 = second["col"]
        row2 = second["row"]

        #Xác định state và anchor
        if row1 == row2:
            state = LIE_X
            col = min(col1, col2)
            row = row1
        else:
            state = LIE_Z
            col = col1
            row = min(row1, row2)

        # Xóa 2 cục nhỏ
        for part in self.split_blocks:
            destroy(part["entity"])

        self.split_blocks.clear()

        self.block = Block(
        self.floor_entity,
        col=col,
        row=row,
        CENTER=self.CENTER,
        move_text=self.move_text,
        game=self
    )
        self.block.rules = self.rules            
        self.block.state = state
        self.block.moves = self.saved_moves    
        self.block._snap()

        self.is_split = False
        self.rules.open_bridges.discard("S")    

        if self.rules.check_block_fall(self.block):
            self.handle_fall(self.block)
        elif self.rules.check_win(self.block):
            self.handle_win(self.block)
        else:
            self.on_bridges(self.block)
    

    def set_bridge_visible(self, game_map, kind, visible):
        tile_value = BRIDGE_TILE[kind]

        for (col, row), parts in self.bridge_entities.items():
            if game_map[row][col] == tile_value:
                for e in parts:
                    e.enabled = visible

    def on_bridges(self, block):
        changed = block.rules.apply_bridges(block)

        for kind in changed:
            if kind == "S":
                self.split_block(block)
            else:
                self.set_bridge_visible(
                    block.rules.map,
                    kind,
                    kind in block.rules.open_bridges
                )

        if not self.is_split:
            if block.rules.check_block_fall(block):
                self.handle_fall(block)
    def restart_game(self):
            self.hide_game()
            self.run_game(self.cur_map_name)
    
    def hide_game(self):
    
        if self.background is not None:
            self.background.enabled = False
    
        if self.block is not None:
            destroy(self.block.body)
            destroy(self.block.pivot)
            self.block = None
    
        if self.floor_entity is not None:
            destroy(self.floor_entity)
            self.floor_entity = None
    
        if self.game_over_text is not None:
            destroy(self.game_over_text)
            self.game_over_text = None
    
        if self.move_text is not None:
            destroy(self.move_text)
            self.move_text = None
    
        if self.stage_name is not None:
            destroy(self.stage_name)
            self.stage_name = None
    
        for part in self.split_blocks:
            destroy(part["entity"])
    
        self.bridge_entities.clear()
        self.split_blocks.clear()
        self.is_split = False
        self.split_moving = False
        self.active_split = 0
        self.game_over = False

    def handle_fall(self, fallen_block):
        if self.game_over:
            return

        self.game_over = True
        fallen_block.moving = True

        fallen_block.body.animate_position(
            fallen_block.body.position + Vec3(0, -5, 0),
            duration=0.6,
            curve=curve.in_quad
        )

        invoke(self.show_game_over, delay=0.6)

    def show_game_over(self):
        self.game_over_text = Text(
            text="You fell! Press R to Restart",
            origin=(0, 0),
            position=(0, 0.375),
            scale=2,
            color=LOSE_COLOR,
            background=True
        )
    def handle_win(self, winning_block):
        if self.game_over:
            return

        self.game_over = True
        winning_block.moving = True

        self.game_over_text = Text(
            text="You win!!! Press R to Restart",
            origin=(0, 0),
            position=(0, 0.375),
            scale=2,
            color=WIN_COLOR,
            background=True
        )

    def handle_input(self, key):
        if key == "r" and self.game_over:
            self.restart_game()
            return

        if self.game_over:
            return

        if self.is_split:
            if key in ("space", "tab"):           
                self.active_split = 1 - self.active_split
                self.update_split_highlight()
                return

            keys = {
                "up arrow": "up", "w": "up",
                "down arrow": "down", "s": "down",
                "left arrow": "left", "a": "left",
                "right arrow": "right", "d": "right",
            }
            if key in keys:
                self.move_split_block(keys[key])
            return

        if self.block is not None:
            self.block.handle_input(key)


game = None

def start_game():
    game.restart_game()

def back_to_menu():
    game.hide_game()

def input(key):
    game.handle_input(key)

game = Game(
    start_game=start_game,
    back_to_menu=back_to_menu
)
#chỗ map_2.json mọi người thay tên file map mà mình cần test vào cú pháp tên file là map_{số}.json
'''
QUI ĐỊNH MAP
0: 0 GẠCH
1: CÓ GẠCH BTH
G: GOAL
C: C BRIGDE    (TOUCH )
X: X BRIDGE   (HEAVY SWITCH - STANDING)
S: S-BRIDGE   (SPLIT SWITCH - STANDING AND SPLIT)
F: FRAGILE TILE (Ô MÀ STANDING LÊN THÌ RỚT)
2: thân câu C khi mở
3: thân cầu X khi mở
4: vị trí của các block khi split
Nếu các cầu chưa mở thì những chỗ đó = 0
Block đc đặt vị trí (2,5) => hàng trước cột sau (TỌA ĐỘ LÀ TÍNH THEO 0-INDEXED)
'''
'''
MAP MẪU
{ 
    "stage_name": "Level 6", 
    "start position": [2,5],
    "matrix": [ 
        [1, "G", 1, 1, "F", 1, 1, 1, 1, 1], #Xa màn hình
        ["F", 1, 1, 1, 1, 1, 1, 0, 1, 1], 
        [1, 1, 1, 2, 2, 1, 1, 1, 1, 1], 
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
        ["S", 1, 1, 1, 1, 3, 3, 1, 0, 1], 
        [1, 1, 0, 1, 1, 1, 1, 0, 0, 0],
        [4, 1, 1, 1, 1, 1, "X", 0, 0, 0],
        [0, 1, "C", 1, 1, 1, 1, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [4, 1, 1, 1, 1, 1, 1, 0, 0, 0]  #Gần màn hình
        ]
}

Map có xây to hơn cũng k sao nhé nhưng đừng xây to quá. Ma trận size m x m nhé
'''
'''
Nhấn tab hoặc space thì sẽ chọn đc cục gạch đang bị split để di chuyển
'''
game.run_game("stage_02.json")

app.run()
