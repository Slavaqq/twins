"""PyWeek 25
Game: Twins
"""

import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 384

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

        self.erika_sprite = arcade.Sprite("female_idle.png", .8)
        self.erika_sprite.center_x = 90
        self.erika_sprite.center_y = 90
        self.erika_list.append(self.erika_sprite)
        self.quentin_sprite = arcade.Sprite("player_idle.png", .9)
        self.quentin_sprite.center_x = 90
        self.quentin_sprite.center_y = 250
        self.quentin_sprite.alpha = 0
        self.quentin_list.append(self.quentin_sprite)
        
        for y, angle in [(16, 0), (368, 180)]:
            for x in range(16, 800, 32):
                wall = arcade.Sprite("stoneMid.png", .25, center_x=x, center_y=y)
                wall.angle = angle
                self.walls.append(wall)

        for x, angle in [(16, 270), (784, 90)]:
            for y in range(48, 337, 32):
                wall = arcade.Sprite("stoneMid.png", .25, center_x=x, center_y=y)
                wall.angle = angle
                self.walls.append(wall)

        wall = arcade.Sprite("stoneMid.png", .25, center_x=752, center_y=48)
        self.walls.append(wall)
        wall = arcade.Sprite("stoneMid.png", .25, center_x=752, center_y=80)
        self.walls.append(wall)
    
        for x in range(48, 161, 32):
            wall = arcade.Sprite("stoneMid.png", .25, center_x=x, center_y=176)
            self.walls.append(wall)

        self.physics_erika = arcade.physics_engines.PhysicsEnginePlatformer(self.erika_sprite, self.walls)
        self.physics_quentin = arcade.physics_engines.PhysicsEnginePlatformer(self.quentin_sprite, self.walls, .2)

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
        self.physics_erika.update()
        self.physics_quentin.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.D:
            self.active_sprite().change_x = 3

        if key == arcade.key.A:
            self.active_sprite().change_x = -3

        if key == arcade.key.W:
            if self.erika_active and self.physics_erika.can_jump():
                self.erika_sprite.change_y = 10
            if self.quentin_active and self.physics_quentin.can_jump():
                self.quentin_sprite.change_y = 10

    def on_key_release(self, key, modifiers):
        if key == arcade.key.Q:
            arcade.set_background_color(arcade.color.AERO_BLUE)
            self.quentin_active = True
            self.quentin_sprite.alpha = 1
            self.erika_active = False
            self.erika_sprite.alpha = 0

        if key == arcade.key.E:
            arcade.set_background_color(arcade.color.AMAZON)
            self.erika_active = True
            self.erika_sprite.alpha = 1
            self.quentin_active = False
            self.quentin_sprite.alpha = 0

        if key == arcade.key.D:
            self.active_sprite().change_x = 0

        if key == arcade.key.A:
            self.active_sprite().change_x = 0

        

def main():
    game = Game()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
