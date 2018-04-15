"""PyWeek 25
Game: Twins
"""

import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

class Game(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Twins")
        self.erika_list = None
        self.quentin_list = None
        self.erika_sprite = None
        self.quentin_sprite = None
        self.walls = None
        self.physics_engine = None

    def setup(self):
        arcade.set_background_color(arcade.color.AMAZON)
        self.erika_list = arcade.SpriteList()
        self.quentin_list = arcade.SpriteList()
        self.walls = arcade.SpriteList()

        self.erika_sprite = arcade.Sprite("female_idle.png", .7)
        self.erika_sprite.center_x = 50
        self.erika_sprite.center_y = 50
        self.erika_list.append(self.erika_sprite)
        self.quentin_sprite = arcade.Sprite("player_idle.png", .7)
        self.quentin_sprite.center_x = 50
        self.quentin_sprite.center_y = 350
        self.quentin_sprite.alpha = 0
        self.quentin_list.append(self.quentin_sprite)
        
        wall = arcade.Sprite("boxCrate_double.png", .4)
        wall.center_x = 200
        wall.center_y = 200
        self.walls.append(wall)


    def on_draw(self):
        arcade.start_render()
        self.erika_list.draw()
        self.quentin_list.draw()
        self.walls.draw()

    def update(self, delta_time):
        pass

    def on_key_release(self, key, modifiers):
        if key == arcade.key.Q:
            arcade.set_background_color(arcade.color.AERO_BLUE)
            self.erika_sprite.alpha = 0
            self.quentin_sprite.alpha = 1

        if key == arcade.key.E:
            arcade.set_background_color(arcade.color.AMAZON)
            self.quentin_sprite.alpha = 0
            self.erika_sprite.alpha = 1

def main():
    game = Game()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
