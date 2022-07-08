from abstract_cubie import Abstract_Cubie
from constants import *
from maths import Point


class Abstract_Cube:
    """
    cube_str looks like:
        UUU                       0  1  2
        UUU                       3  4  5
        UUU                       6  7  8

    LLL FFF RRR BBB    9 10 11 | 12 13 14 | 15 16 17 | 18 19 20
    LLL FFF RRR BBB   21 22 23 | 24 25 26 | 27 28 29 | 30 31 32
    LLL FFF RRR BBB   33 34 35 | 36 37 38 | 39 40 41 | 42 43 44

        DDD                      45 46 47
        DDD                      48 49 50
        DDD                      51 52 53
    Note that the back side is mirrored in the horizontal axis during unfolding.
    Each 'sticker' must be a single character.
    """
    def __init__(self, cube_str, Cubie):
        self.cube_str = cube_str
        self.debug = False
        self.move_list = []
        self.centers = (
            Cubie(pos=RIGHT, colors=(cube_str[28], None, None)),
            Cubie(pos=LEFT, colors=(cube_str[22], None, None)),
            Cubie(pos=UP, colors=(None, cube_str[4], None)),
            Cubie(pos=DOWN, colors=(None, cube_str[49], None)),
            Cubie(pos=FRONT, colors=(None, None, cube_str[25])),
            Cubie(pos=BACK, colors=(None, None, cube_str[31])),
            Cubie(pos=Point(0, 0, 0), colors=(None, None, None)))
        self.edges = (
            Cubie(pos=RIGHT + UP, colors=(cube_str[16], cube_str[5], None)),
            Cubie(pos=RIGHT + DOWN, colors=(cube_str[40], cube_str[50], None)),
            Cubie(pos=RIGHT + FRONT, colors=(cube_str[27], None, cube_str[26])),
            Cubie(pos=RIGHT + BACK, colors=(cube_str[29], None, cube_str[30])),
            Cubie(pos=LEFT + UP, colors=(cube_str[10], cube_str[3], None)),
            Cubie(pos=LEFT + DOWN, colors=(cube_str[34], cube_str[48], None)),
            Cubie(pos=LEFT + FRONT, colors=(cube_str[23], None, cube_str[24])),
            Cubie(pos=LEFT + BACK, colors=(cube_str[21], None, cube_str[32])),
            Cubie(pos=UP + FRONT, colors=(None, cube_str[7], cube_str[13])),
            Cubie(pos=UP + BACK, colors=(None, cube_str[1], cube_str[19])),
            Cubie(pos=DOWN + FRONT, colors=(None, cube_str[46], cube_str[37])),
            Cubie(pos=DOWN + BACK, colors=(None, cube_str[52], cube_str[43])),
        )
        self.corners = (
            Cubie(pos=RIGHT + UP + FRONT, colors=(cube_str[15], cube_str[8], cube_str[14])),
            Cubie(pos=RIGHT + UP + BACK, colors=(cube_str[17], cube_str[2], cube_str[18])),
            Cubie(pos=RIGHT + DOWN + FRONT, colors=(cube_str[39], cube_str[47], cube_str[38])),
            Cubie(pos=RIGHT + DOWN + BACK, colors=(cube_str[41], cube_str[53], cube_str[42])),
            Cubie(pos=LEFT + UP + FRONT, colors=(cube_str[11], cube_str[6], cube_str[12])),
            Cubie(pos=LEFT + UP + BACK, colors=(cube_str[9], cube_str[0], cube_str[20])),
            Cubie(pos=LEFT + DOWN + FRONT, colors=(cube_str[35], cube_str[45], cube_str[36])),
            Cubie(pos=LEFT + DOWN + BACK, colors=(cube_str[33], cube_str[51], cube_str[44])),
        )
        self.cubies = self.centers + self.corners + self.edges
    
    def right_center(self): return self.centers[0]
    def left_center(self) : return self.centers[1]
    def up_center(self)   : return self.centers[2]
    def down_center(self) : return self.centers[3]
    def front_center(self): return self.centers[4]
    def back_center(self) : return self.centers[5]
    
    def face(self, face):
        """
        :param face: face of the cube ie RIGHT LEFT UP DOWN etc.
        :return: a list of the pieces in the face
        """
        if isinstance(face, Abstract_Cubie):
            face = face.pos
        if face.count(0) != 2:
            raise TypeError("Face must be one of RIGHT, LEFT, UP... etc")
        return [p for p in self.cubies if p.pos.dot(face) > 0]
    
    def slice_(self, _slice):
        """
        :param _slice: either m for middle layer or e for equator layer
        :return: all the cubies that are in that slice
        """
        assert _slice == "e" or _slice == "m"
        index = None
        if _slice == "e":
            index = 1
        elif _slice == "m":
            index = 0
        return [p for p in self.cubies if p.pos[index] == 0]
    
    def sort_slice(self, slice_):
        res = []
        for z in range(-1,2):
            row = [p for p in slice_ if p[2] == z]
            for i in range(3):
                if row[i][0] == -1:
                    row[i], row[0] = row[0], row[i]
                elif row[i][0] == 0:
                    row[i], row[1] = row[1], row[i]
            res += row
        return res
    
    def color_list(self):
        # sorting the top face

        sorted_top = self.sort_slice(self.face(UP))
        sorted_eq = self.sort_slice(self.slice_("e"))
        sorted_bottom = self.sort_slice(self.face(DOWN))
        sorted_cube = [sorted_top, sorted_eq, sorted_bottom]
        color_list = []

        color_list += [c.colors[1] for c in sorted_top]

        for i in range(3):
            color_list += [sorted_cube[i][0].colors[0], sorted_cube[i][3].colors[0], sorted_cube[i][6].colors[0]]
            color_list += [sorted_cube[i][6].colors[2], sorted_cube[i][7].colors[2], sorted_cube[i][8].colors[2]]
            color_list += [sorted_cube[i][8].colors[0], sorted_cube[i][5].colors[0], sorted_cube[i][2].colors[0]]
            color_list += [sorted_cube[i][2].colors[2], sorted_cube[i][1].colors[2], sorted_cube[i][0].colors[2]]
        row = ""
        for i in range(8,-1,-1):
            row += sorted_bottom[i].colors[1]
            if i % 3 == 0:
                # reverse the row
                reversed_row = ""
                for j in range(2,-1,-1):
                    reversed_row += row[j]
                color_list += reversed_row
                row = ""
        return color_list
    
    def __str__(self):
        template = ("{}{}{}\n"
                    "    {}{}{}\n"
                    "    {}{}{}\n"
                    "{}{}{} {}{}{} {}{}{} {}{}{}\n"
                    "{}{}{} {}{}{} {}{}{} {}{}{}\n"
                    "{}{}{} {}{}{} {}{}{} {}{}{}\n"
                    "    {}{}{}\n"
                    "    {}{}{}\n"
                    "    {}{}{}\n")

        return "    " + template.format(*self.color_list())

    def turn_face(self, face, direction):
        """
        :param face: Point or cubie
        :param direction: int, - 1 or 1
        :return: cube so that this function can be stacked but not sure if this works or not
        """
        if isinstance(face, Abstract_Cubie):
            face = face.pos

        assert direction == -1 or direction == 1
        if face not in CENTERS:
            # print(face)
            # print("exception face must be a center")
            raise Exception("face must be a center")

        if face.count(0) != 2:
            print(face)
            raise TypeError("Face must be one of RIGHT, LEFT, UP... etc face = ", face)
        matrix = None
        if face == RIGHT:
            matrix = ROT_YZ_CW * Matrix(1, 0,         0,
                                        0, direction, 0,
                                        0, 0,         direction)
        elif face == LEFT:
            matrix = ROT_YZ_CW * Matrix(1, 0, 0,
                                        0, -direction, 0,
                                        0, 0, -direction)
        elif face == UP:
            matrix = ROT_XZ_CW * Matrix(direction,0, 0,
                                        0,        1, 0,
                                        0,        0, direction)
        elif face == DOWN:
            matrix = ROT_XZ_CW * Matrix(-direction, 0, 0,
                                        0, 1, 0,
                                        0, 0, -direction)
        elif face == FRONT:
            matrix = ROT_XY_CW * Matrix(direction, 0,         0,
                                        0,         direction, 0,
                                        0,         0,         1)
        elif face == BACK:
            matrix = ROT_XY_CC * Matrix(direction, 0,         0,
                                        0,         direction, 0,
                                        0,         0,         1)
        self.rotate_face(face, matrix)
        self.move_list.append((face, direction))
        if self.debug:
            print(self, face, direction, "\n")

    def rotate_face(self, f, matrix):
        face = self.face(f)
        for p in face:
            p.rotate(matrix)

    def get_cubie(self, x, y=None, z=None):
        """
            the cubie at the given point
        """
        if isinstance(x, Point):
            pos = x
        elif isinstance(x, int):
            pos = Point(x, y, z)
        else:
            raise TypeError("must enter either x,y,z values or a Point")
        for p in self.cubies:
            if p.pos == pos:
                return p