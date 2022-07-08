from constants import *

class Abstract_Cubie:
    def __init__(self, pos, colors):
        self.pos = pos
        self.colors = colors
        self.type = None
        self.__set_piece_type()

    def __set_piece_type(self):
        count = 0
        for i in self.colors:
            if i is not None:
                count += 1
        if count == 1:
            self.type = CENTER
        elif count == 2:
            self.type = EDGE
        elif count == 3:
            self.type = CORNER

    def __str__(self):
        colors = "".join(c if c is not None else "N" for c in self.colors )
        return f"({self.type}, {colors}, {self.pos})"

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.pos[key]
        elif isinstance(key, str):
            if key == "x":
                return self.pos.x
            if key == "y":
                return self.pos.y
            if key == "z":
                return self.pos.z
        else:
            raise TypeError("must enter an int or a string")

    def __setitem__(self, key, value):
        if isinstance(key, int):
            self.pos[key] = value
            return self.pos[key]
        elif isinstance(key, str):
            if key == "x":
                self.pos.x = key
                return self.pos.x
            if key == "y":
                self.pos.y = key
                return self.pos.y
            if key == "z":
                self.pos.y = key
                return self.pos.z
        else:
            raise TypeError("must enter an int or a string")

    def __eq__(self, other):
        if self.type == other.type and self.pos == other.pos and self.colors == other.colors:
            return True
        return False

    def __ne__(self, other):
        if self.type != other.type or self.pos != other.pos or self.colors != other.colors:
            return True
        return False

    def rotate(self, matrix):
        self.pos = matrix * self.pos

        # rotating the colors of the cubie
        # turn the characters into ascii rep
        col = Point([ord(c) if c is not None else 0 for c in self.colors])

        # then multiply by the rotation matrix
        self.colors = matrix * col

        # remove the negatives and return back to characters
        for i in range(3):
            if self.colors[i] == 0:
                self.colors[i] = None
            else:
                self.colors[i] = chr(abs(self.colors[i]))
