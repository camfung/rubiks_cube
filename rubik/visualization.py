from ursina import *
from abstract_cube import Abstract_Cube
from abstract_cubie import Abstract_Cubie
from constants import *


class Vis_Cube(Abstract_Cube):
    def __init__(self, cube_str, Cubie):
        super().__init__(cube_str, Cubie)
        self.entities = []


class Vis_Cubie(Abstract_Cubie):
    def __init__(self, pos, colors):
        super().__init__(pos, colors)
        self.ent = None


class Game(Ursina):
    def __init__(self, cube_str):
        super().__init__()
        window.fullscreen = False
        EditorCamera()
        Entity(model="quad", scale=60, texture="white_cube", texture_scale=(60,60), rotation_x=90, y=-5)
        camera.world_position = (0,0,-15)
        self.rot = 0
        self.animation_time = .1
        self.cube = Vis_Cube("UUUUUUUUULLLFFFRRRBBBLLLFFFRRRBBBLLLFFFRRRBBBDDDDDDDDD", Vis_Cubie)
        self.model, self.texture = "textures/cubie.obj", "textures/Cube_color.png"
        self.load_game()


    def load_game(self):
        self.PARENT = Entity(model="cube", texture="white_cube")
        # self.cube = Entity(model=self.model, texture=self.texture, position=(1,1,-1))
        index = 0
        for z in range(-1,2):
            for y in range(-1, 2):
                for x in range(-1, 2):
                    # if z != -1 and z != 1:
                    #     self.texture = "textures/cube.png"
                    # else: self.texture = "textures/Cube_color.png"
                    self.cube.entities.append(Entity(model=self.model, texture=self.texture, position=(x,y,z)))
                    self.cube.entities[index].parent = scene
                    cubie = self.cube.get_cubie(x,y,z)
                    cubie.ent = self.cube.entities[index]
                    index += 1
        print(self.cube)

    def turn_face(self, center, d):
        if isinstance(center, Vis_Cubie):
            center = center.pos
        if   center == RIGHT or center == LEFT: rotation_axis = "x"
        elif center == UP    or center == DOWN: rotation_axis = "y"
        elif center == FRONT or center == BACK: rotation_axis = "z"
        else:
            raise TypeError("center is not a center")
        face = self.cube.face(center)
        self.reparent_to_scene()
        for cube in face:
            c = cube.ent
            c.parent = self.PARENT
            eval(f'self.PARENT.animate_rotation_{rotation_axis}({d * 90}, duration=self.animation_time)')

        self.cube.turn_face(center, d)

    def reparent_to_scene(self):
        for cubie in self.cube.cubies:
            c = cubie.ent
            if c.parent == self.PARENT:
                world_pos, world_rot = round(c.world_position, 1), c.world_rotation
                c.parent = scene
                c.position, c.rotation = world_pos, world_rot
        self.PARENT.rotation = 0

    def input(self, key):
        if key == "r":
            self.turn_face(RIGHT, 1)
            # print(self.cube)
        if key == "l":
            self.turn_face(LEFT, -1)
            # print(self.cube)
        if key == "f":
            self.turn_face(BACK, 1)
            # print(self.cube)
        if key == "u":
            self.turn_face(UP, 1)
            # print(self.cube)

        super().input(key)


if __name__ == "__main__":
    game = Game("UUUUUUUUULLLFFFRRRBBBLLLFFFRRRBBBLLLFFFRRRBBBDDDDDDDDD")
    game.run()
