"""PyWeek 25
Game: Twins
"""

import arcade
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 384

FACE_RIGHT = 1
FACE_LEFT = 2

class Game(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Twins")
        self.erika_list = None
        self.quentin_list = None
        self.erika_sprite = None
        self.quentin_sprite = None
        self.walls = None
        self.physics_erika = None
        self.physics_quentin = None
        self.erika_active = True
        self.quentin_active = False

    def setup(self):
        arcade.set_background_color(arcade.color.AMAZON)
        self.erika_list = arcade.SpriteList()
        self.quentin_list = arcade.SpriteList()
        self.walls = arcade.SpriteList()

        self.erika_sprite = AnimatedSprite(scale=.8, center_x=90, center_y=90)
        self.erika_sprite.stand_right_textures = []
        self.erika_sprite.stand_left_textures = []
        self.erika_sprite.walk_right_textures = []
        self.erika_sprite.walk_left_textures = []
        self.erika_sprite.jump_right_textures = []
        self.erika_sprite.jump_left_textures = []
        self.erika_sprite.stand_right_textures.append(arcade.load_texture("img/female_stand.png", scale=.8))
        self.erika_sprite.stand_left_textures.append(arcade.load_texture("img/female_stand.png", scale=.8, mirrored=True))
        self.erika_sprite.walk_right_textures.append(arcade.load_texture("img/female_walk1.png", scale=.8))
        self.erika_sprite.walk_right_textures.append(arcade.load_texture("img/female_walk2.png", scale=.8))
        self.erika_sprite.walk_left_textures.append(arcade.load_texture("img/female_walk1.png", scale=.8, mirrored=True))
        self.erika_sprite.walk_left_textures.append(arcade.load_texture("img/female_walk2.png", scale=.8, mirrored=True))
        self.erika_sprite.jump_right_textures.append(arcade.load_texture("img/female_jump.png", scale=.8)) 
        self.erika_sprite.jump_left_textures.append(arcade.load_texture("img/female_jump.png", scale=.8, mirrored=True)) 
        self.erika_list.append(self.erika_sprite)
        self.quentin_sprite = AnimatedSprite(scale=.9, center_x=90, center_y=90)
        self.quentin_sprite.stand_right_textures = []
        self.quentin_sprite.stand_left_textures = []
        self.quentin_sprite.walk_right_textures = []
        self.quentin_sprite.walk_left_textures = []
        self.quentin_sprite.jump_right_textures = []
        self.quentin_sprite.jump_left_textures = []
        self.quentin_sprite.stand_right_textures.append(arcade.load_texture("img/player_stand.png", scale=.8))
        self.quentin_sprite.stand_left_textures.append(arcade.load_texture("img/player_stand.png", scale=.8, mirrored=True))
        self.quentin_sprite.walk_right_textures.append(arcade.load_texture("img/player_walk1.png", scale=.8))
        self.quentin_sprite.walk_right_textures.append(arcade.load_texture("img/player_walk2.png", scale=.8))
        self.quentin_sprite.walk_left_textures.append(arcade.load_texture("img/player_walk1.png", scale=.8, mirrored=True))
        self.quentin_sprite.walk_left_textures.append(arcade.load_texture("img/player_walk2.png", scale=.8, mirrored=True))
        self.quentin_sprite.jump_right_textures.append(arcade.load_texture("img/player_jump.png", scale=.8)) 
        self.quentin_sprite.jump_left_textures.append(arcade.load_texture("img/player_jump.png", scale=.8, mirrored=True)) 
        self.quentin_sprite.alpha = 0
        self.quentin_list.append(self.quentin_sprite)
        
        for y, angle in [(16, 0), (368, 180)]:
            for x in range(16, 800, 32):
                wall = arcade.Sprite("img/stoneMid.png", .25, center_x=x, center_y=y)
                wall.angle = angle
                self.walls.append(wall)

        for x, angle in [(16, 270), (784, 90)]:
            for y in range(48, 337, 32):
                wall = arcade.Sprite("img/stoneMid.png", .25, center_x=x, center_y=y)
                wall.angle = angle
                self.walls.append(wall)

        wall = arcade.Sprite("img/stoneMid.png", .25, center_x=752, center_y=48)
        self.walls.append(wall)
        wall = arcade.Sprite("img/stoneMid.png", .25, center_x=752, center_y=80)
        self.walls.append(wall)
    
        for x in range(48, 161, 32):
            wall = arcade.Sprite("img/stoneMid.png", .25, center_x=x, center_y=176)
            self.walls.append(wall)

        self.physics_erika = arcade.physics_engines.PhysicsEnginePlatformer(self.erika_sprite, self.walls)
        self.physics_quentin = arcade.physics_engines.PhysicsEnginePlatformer(self.quentin_sprite, self.walls, .4)

    def active_sprite(self):
        if self.erika_active:
            return self.erika_sprite
        else:
            return self.quentin_sprite

    def on_draw(self):
        arcade.start_render()
        self.erika_list.draw()
        self.quentin_list.draw()
        self.walls.draw()

    def update(self, delta_time):
        self.erika_list.update_animation()
        self.quentin_list.update_animation()
        self.physics_erika.update()
        self.physics_quentin.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.D:
            self.erika_sprite.change_x = 5
            self.quentin_sprite.change_x = 5

        if key == arcade.key.A:
            self.erika_sprite.change_x = -5
            self.quentin_sprite.change_x = -5

        if key == arcade.key.W:
            if self.physics_quentin.can_jump() and self.physics_erika.can_jump():
                self.erika_sprite.change_y = 10
                self.quentin_sprite.change_y = 10

    def on_key_release(self, key, modifiers):
        if key == arcade.key.TAB:
            if self.erika_sprite.alpha == 0:
                self.quentin_sprite.alpha = 0
                self.erika_sprite.alpha = 1
                arcade.set_background_color(arcade.color.AMAZON)
            elif self.quentin_sprite.alpha == 0:
                self.erika_sprite.alpha = 0
                self.quentin_sprite.alpha = 1
                arcade.set_background_color(arcade.color.ATOMIC_TANGERINE)

        if key == arcade.key.D:
            self.erika_sprite.change_x = 0
            self.quentin_sprite.change_x = 0

        if key == arcade.key.A:
            self.erika_sprite.change_x = 0
            self.quentin_sprite.change_x = 0


class Player(arcade.Sprite):

    def __init__(self):
        super().__init__()


class AnimatedSprite(arcade.AnimatedWalkingSprite):
    
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
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
