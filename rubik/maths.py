class Point:
    def __init__(self, x=None, y=None, z=None):
        try:
            it = iter(x)
            self.x = next(it)
            self.y = next(it)
            self.z = next(it)
        except TypeError:
            self.x = x
            self.y = y
            self.z = z
        if all((x is None, y is None, z is None)):
            self.x = 0
            self.y = 0
            self.z = 0

    def __getitem__(self, item):  # self[item]
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        elif item == 2:
            return self.z
        else:
            raise IndexError(f"Must have an index between 0-2 inclusive. Got {item}")

    def __str__(self):
        return str((self.x, self.y, self.z))

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        if isinstance(other , Point):
            return Point(self.x * other.x, self.y * other.y, self.z * other.z)
        if isinstance(other, int):
            return Point(self.x * other, self.y * other, self.z * other)

    def __eq__(self, other):
        if isinstance(other, Point):
            if self.x != other.x or self.y != other.y or self.z != other.z:
                return False
        elif isinstance(other, int):
            if self.x != other or self.y != other or self.z != other:
                return False
        return True

    def __setitem__(self, item, value):
        if item == 0:
            self.x = value
        elif item == 1:
            self.y = value
        elif item == 2:
            self.z = value
        else:
            raise IndexError(f"Must have an index between 0-2 inclusive. Got {item}")

    def dot(self, other):
        """Return the dot product"""
        return self.x * other.x + self.y * other.y + self.z * other.z

    def count(self, val):
        """
        return the number of elements that are equal to val
        """
        return int(self.x == val) + int(self.y == val) + int(self.z == val)

    def abs_length(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def length(self):
        return self.x + self.y + self.z


class Matrix:
    def __init__(self, *args):

        if len(args) == 9:
            self.mat = args
        if len(args) == 1:
            self.mat = []
            for i in args:
                for j in i:
                    self.mat.append(j)
        # else:
        #     raise ValueError(f"expected 9 arguments. Got {len(args)}")

    def __mul__(self, other):
        if isinstance(other, Point):
            return Point(other.dot(Point(temp)) for temp in self.rows())

        elif isinstance(other, Matrix):
            # matrix matrix multiplication
            temp = []
            for row in self.rows():
                for col in other.cols():
                    r = Point(row)
                    c = Point(col)
                    temp.append(r.dot(c))
            return Matrix(temp)

        else:
            raise TypeError(f"expected Matrix or Point type got {type(other)}")

    def __getitem__(self, item):
        try:
            if len(item) == 2:
                row = item[0]
                col = item[1]
                index = row * 3 + col
                return self.mat[index]
        except TypeError:
            if item > len(self.mat):
                raise IndexError(f"Index must be less than {len(self.mat)}. Got {item} instead.")
            return self.mat[item]

    def __str__(self):
        return ("[{}, {}, {},\n"
                " {}, {}, {},\n"
                " {}, {}, {}]".format(*self.mat))

    def rows(self):
        yield self.mat[0:3]
        yield self.mat[3:6]
        yield self.mat[6:9]

    def cols(self):
        yield [self.mat[i] for i in range(9) if i % 3 == 0]
        yield [self.mat[i] for i in range(9) if i % 3 == 1]
        yield [self.mat[i] for i in range(9) if i % 3 == 2]

    def get_mat(self):
        return [i for i in self.mat]
