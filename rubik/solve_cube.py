from abstract_cube import Abstract_Cube
from solve_cubie import Solve_Cubie
from constants import *


class Solve_Cube(Abstract_Cube):
    def __init__(self, cube_str):
        super().__init__(cube_str, Solve_Cubie)
        self.move_list = []
        self.debug = False

    def get_side_faces(self, face):
        """
        :param face: Point or cubie
        :return: left center, right center
        """
        if isinstance(face, Solve_Cubie):
            face = face.pos
        assert face in CENTERS
        if   face == RIGHT: return [self.get_center(FRONT), self.get_center(BACK )]
        elif face == LEFT : return [self.get_center(BACK ), self.get_center(FRONT)]
        elif face == FRONT: return [self.get_center(LEFT ), self.get_center(RIGHT)]
        elif face == BACK : return [self.get_center(RIGHT), self.get_center(LEFT )]

    def get_center(self, center, y=None, z=None):
        """
        :param center: Point
        :return: cubie at the Point
        """
        if y is not None:
            center = Point(center, y, z)
        assert isinstance(center, Point)
        for c in self.centers:
            if c.pos == center:
                return c
        raise Exception("argument is not a center")

    def solved_edge(self, center1, center2):
        """
        :param center1: Point or Cubie
        :param center2: Point or Cubie
        :return: the edge that is solved in between the centers passed
        """
        # assert that center2 and center2 are Cubies
        if isinstance(center1, Point) or isinstance(center2, Point):
            center1 = self.get_center(center1)
            center2 = self.get_center(center2)
        if center1.pos.count(0) != 2:
            raise TypeError("center 1 is not a center")
        if center2.pos.count(0) != 2:
            raise TypeError("center 2 is not a center")

        axis1 = axis2 = None
        for i in range(3):
            if center1.colors[i] is not None:
                axis1 = i
            if center2.colors[i] is not None:
                axis2 = i
        for p in self.edges:
            if center1.colors[axis1] in p.colors and center2.colors[axis2] in p.colors and None in p.colors:
                return p

    def solved_corner(self, center1, center2, center3):
        """
        :param center1: Point or Cubie
        :param center2: Point or Cubie
        :param center3: Point or Cubie
        :return: corner that has the 3 colors
        """
        if isinstance(center1, Point):
            center1 = self.get_center(center1)
        if isinstance(center2, Point):
            center2 = self.get_center(center2)
        if isinstance(center3, Point):
            center3 = self.get_center(center3)

        if center1.pos not in CENTERS or center2.pos not in CENTERS or center3.pos not in CENTERS:
            raise TypeError("center must be a in CENTERS")

        axis1 = axis2 = axis3 = None
        for i in range(3):
            if center1.colors[i] is not None:
                axis1 = center1.colors[i]
            if center2.colors[i] is not None:
                axis2 = center2.colors[i]
            if center3.colors[i] is not None:
                axis3 = center3.colors[i]
        for p in self.corners:
            if axis1 in p.colors and axis2 in p.colors and axis3 in p.colors:
                return p

    def get_adj_centers(self, cubie):
        return [
            self.get_center(Matrix(1, 0, 0,
                                   0, 0, 0,
                                   0, 0, 0) * cubie.pos),
            self.get_center(Matrix(0, 0, 0,
                                   0, 1, 0,
                                   0, 0, 0) * cubie.pos),

            self.get_center(Matrix(0, 0, 0,
                                   0, 0, 0,
                                   0, 0, 1) * cubie.pos)
               ]
