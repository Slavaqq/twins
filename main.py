"""PyWeek 25
Game: Twins
"""

import arcade
import math
import random

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 512
VIEWPORT_MARGIN = 40
PLAYER_SCALE = .8
NUMBER_OF_GEMS = 40
LIMIT = 40

INTRO = 0
GAME = 1
OVER = 2
WIN = 3

FACE_RIGHT = 1
FACE_LEFT = 2


def get_map(map_file):
    with open(map_file, "r") as f:
        map_array = []
        for line in f:
            map_array.append(line.strip().split(","))
    return map_array


class Game(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Twins")
        self.walls = None
        self.ambi = None
        self.physics = None
        self.gems = None
        self.first_world = True
        self.score = None
        self.time = None
        self.view_left = None
        self.view_bottom = None
        self.game_state = INTRO

    def setup(self):
        arcade.set_background_color((20, 20, 20))
        self.player_list = arcade.SpriteList()
        self.ambi = arcade.SpriteList()
        self.walls = arcade.SpriteList()
        self.gems = arcade.SpriteList()
        self.score = 0
        self.time = 0.0
        self.view_left = 0
        self.view_bottom = 0

        self.player_sprite = AnimatedSprite(scale=PLAYER_SCALE, center_x=90, center_y=80)
        self.player_sprite.stand_right_textures = []
        self.player_sprite.stand_left_textures = []
        self.player_sprite.walk_right_textures = []
        self.player_sprite.walk_left_textures = []
        self.player_sprite.jump_right_textures = []
        self.player_sprite.jump_left_textures = []
        self.player_sprite.stand_right_textures.append(arcade.load_texture("img/player_stand.png", scale=.8))
        self.player_sprite.stand_left_textures.append(arcade.load_texture("img/player_stand.png", scale=.8, mirrored=True))
        self.player_sprite.walk_right_textures.append(arcade.load_texture("img/player_walk1.png", scale=.8))
        self.player_sprite.walk_right_textures.append(arcade.load_texture("img/player_walk2.png", scale=.8))
        self.player_sprite.walk_left_textures.append(arcade.load_texture("img/player_walk1.png", scale=.8, mirrored=True))
        self.player_sprite.walk_left_textures.append(arcade.load_texture("img/player_walk2.png", scale=.8, mirrored=True))
        self.player_sprite.jump_right_textures.append(arcade.load_texture("img/player_jump.png", scale=.8)) 
        self.player_sprite.jump_left_textures.append(arcade.load_texture("img/player_jump.png", scale=.8, mirrored=True)) 
        self.player_list.append(self.player_sprite)

        for row_index, row in enumerate(get_map("map.map")):
            for column_index, item in enumerate(row):

                x = 16 + column_index * 32
                y = SCREEN_HEIGHT - (16 + row_index * 32)
                if item == "0": # empty space
                    continue
                elif item == "1":
                    self.walls.append(arcade.Sprite("img/boxCrate_double.png", .25, center_x=x, center_y=y))
                elif item == "2":
                    self.walls.append(arcade.Sprite("img/sandMid.png", .25, center_x=x, center_y=y))
                elif item == "3":
                    self.walls.append(arcade.Sprite("img/sandCenter.png", .25, center_x=x, center_y=y))
                elif item == "4":
                    self.walls.append(arcade.Sprite("img/sandCliff_left.png", .25, center_x=x, center_y=y))
                elif item == "5":
                    self.walls.append(arcade.Sprite("img/sandCliff_right.png", .25, center_x=x, center_y=y))
                elif item == "8":
                    self.ambi.append(arcade.Sprite("img/rock.png", .25, center_x=x, center_y=y))
                elif item == "9":
                    self.ambi.append(arcade.Sprite("img/signRight.png", .5, center_x=x, center_y=y))

        self.physics = arcade.physics_engines.PhysicsEnginePlatformer(self.player_sprite, self.walls, .4)

        for __ in range(NUMBER_OF_GEMS):

            gem = arcade.Sprite("img/gemRed.png", .3)
            gem_placed = False

            while not gem_placed:
                gem.center_x = random.randrange(2200) 
                gem.center_y = random.randrange(SCREEN_HEIGHT)

                wall_hit_list = len(arcade.check_for_collision_with_list(gem, self.walls)) == 0
                gem_hit_list = len(arcade.check_for_collision_with_list(gem, self.gems)) == 0
                player_hit_list = len(arcade.check_for_collision_with_list(gem, self.player_list)) == 0
                
                if wall_hit_list and gem_hit_list and player_hit_list:
                    gem_placed = True

            self.gems.append(gem)

    def on_draw(self):
        arcade.start_render()
        
        if self.game_state == INTRO:
            self.draw_intro()
        elif self.game_state == GAME:
            self.draw_game()
        elif self.game_state == OVER:
            self.draw_game_over()
        elif self.game_state == WIN:
            self.draw_win()

    def draw_intro(self):
        arcade.draw_text("Twins", 385, 410, (255, 255, 255), 54)
        arcade.draw_text("Collect gems before time runs out.", 235, 350, (255, 255, 255), 24)
        arcade.draw_text("Walk left: A, Walk right: D", 245, 250, (255, 255, 255), 24)
        arcade.draw_text("Jump: W, Switch worlds: SPACE", 240, 200, (255, 255, 255), 24)
        arcade.draw_text("Press ENTER to start", 330, 100, (255, 255, 255), 24)

    def draw_game_over(self):
        arcade.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)
        arcade.draw_text("Sorry, game over!", 215, 400, (255, 255, 255), 54)
        arcade.draw_text("Press ENTER to restart", 325, 100, (255, 255, 255), 24)

    def draw_win(self):        
        arcade.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)
        arcade.draw_text("That was amazing!", 215, 400, (255, 255, 255), 54)
        arcade.draw_text("Press ENTER to restart", 325, 100, (255, 255, 255), 24)

    def draw_game(self):
        arcade.start_render()
        self.ambi.draw()
        self.player_list.draw()
        self.walls.draw()
        self.gems.draw()
        time = LIMIT - int(self.time)
        if time <= 0:
            try:
                arcade.sound.play_sound("sound/Jingle_Lose_01.wav")
            except Exception:
                pass
            self.game_state = OVER
        left = NUMBER_OF_GEMS - (self.score)
        if left == 0:
            try:
                arcade.sound.play_sound("sound/Jingle_Win_00.wav")
            except Exception:
                pass
            self.game_state = WIN
        arcade.draw_text(f"Time: {time} Gems: {left}", self.view_left + 825, self.view_bottom + 495, (255, 255, 255), 12)

    def update(self, delta_time):
        self.player_list.update_animation()
        self.physics.update()

        hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.gems)
        
        for gem in hit_list:
            gem.kill()
            self.score += 1

        self.gems.update()

        self.time += delta_time

        scrolled = False

        left_boundary = self.view_left + VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            scrolled = True

        right_boundary = self.view_left + SCREEN_WIDTH - VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            scrolled = True

        top_boundary = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary 
            scrolled = True

        bottom_boundary = self.view_bottom + VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            scrolled = True

        if scrolled:
            arcade.set_viewport(self.view_left, self.view_left + SCREEN_WIDTH, self.view_bottom, self.view_bottom + SCREEN_HEIGHT)


    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            if self.game_state == INTRO:
                self.setup()
                self.game_state = GAME
            elif self.game_state == OVER or self.game_state == WIN:
                self.setup()
                self.game_state = GAME

        if key == arcade.key.SPACE and self.game_state == GAME:
            try:
                arcade.sound.play_sound("sound/Pickup_02.wav")
            except Exception:
                pass
            if self.first_world:
                self.first_world = False
                arcade.set_background_color((5, 5, 5))
            else:
                self.first_world = True
                arcade.set_background_color((20, 20, 20))
 
        if key == arcade.key.D:
            self.player_sprite.change_x = 8 if self.first_world else 3

        if key == arcade.key.A:
            self.player_sprite.change_x = -8 if self.first_world else -3

        if key == arcade.key.W and self.physics.can_jump():
            try:
                arcade.sound.play_sound("sound/Jump_00.wav")
            except Exception:
                pass
            self.player_sprite.change_y = 7 if self.first_world else 13

    def on_key_release(self, key, modifiers):
        if key == arcade.key.D:
            self.player_sprite.change_x = 0

        if key == arcade.key.A:
            self.player_sprite.change_x = 0


class AnimatedSprite(arcade.AnimatedWalkingSprite):
    """Sprite class with jump animation support."""
    
    def __init__(self, scale=1, image_x=0, image_y=0, center_x=0, center_y=0):
        super().__init__(scale=scale, image_x=image_x, image_y=image_y, center_x=center_x, center_y=center_y)
        self.jump_right_textures = None
        self.jump_left_textures = None
        self.texture_change_distance = 15

    def update_animation(self):
        x1 = self.center_x
        x2 = self.last_texture_change_center_x
        y1 = self.center_y
        y2 = self.last_texture_change_center_y
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        texture_list = []

        walking = False
        jumping = False
        if self.change_x > 0  and self.change_y == 0 and self.walk_right_textures and len(self.walk_right_textures) > 0:
            self.state = FACE_RIGHT
            walking = True
        elif self.change_x < 0 and self.change_y == 0 and self.walk_left_textures and len(self.walk_left_textures) > 0:
            self.state = FACE_LEFT
            walking = True
        elif self.change_y > 0:
            if self.change_x > 0 and self.jump_right_textures and len(self.jump_right_textures):
                self.state = FACE_RIGHT
                jumping = True
            elif self.change_x < 0 and self.jump_left_textures and len(self.jump_left_textures):
                self.state = FACE_LEFT
                jumping = True
        
        if self.change_x == 0 and self.change_y == 0:
            if self.state == FACE_LEFT:
                self.texture = self.stand_left_textures[0]
            elif self.state == FACE_RIGHT:
                self.texture = self.stand_right_textures[0]

        elif walking or jumping:
            if distance > self.texture_change_distance:
                self.last_texture_change_center_x = self.center_x
                self.last_texture_change_center_y = self.center_y
                self.cur_texture_index += 1

            if self.state == FACE_LEFT:
                if walking:
                    texture_list = self.walk_left_textures
                if jumping:
                    texture_list = self.jump_left_textures
                if texture_list is None or len(texture_list) == 0:
                    raise RuntimeError("update_animation was called on a sprite that doesn't have a "
                                       "list of walk left textures.")
            elif self.state == FACE_RIGHT:
                if walking:
                    texture_list = self.walk_right_textures
                if jumping:
                    texture_list = self.jump_right_textures
                if texture_list is None or len(texture_list) == 0:
                    raise RuntimeError("update_animation was called on a sprite that doesn't have a list of "
                                       "walk right textures.")
             
            if self.cur_texture_index >= len(texture_list):
                self.cur_texture_index = 0
            self.texture = texture_list[self.cur_texture_index]


def main():
    game = Game()
    game.set_mouse_visible(False)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
