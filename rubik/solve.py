from solve_cube import Solve_Cube
from constants import *


class Solve:
    def __init__(self, cube_str):
        self.cube = Solve_Cube(cube_str)
        # getting the center colors of the faces
        self.left_center = self.cube.left_center()
        self.right_center = self.cube.right_center()
        self.front_center = self.cube.front_center()
        self.back_center = self.cube.back_center()
        self.up_center = self.cube.up_center()
        self.down_center = self.cube.down_center()

        self.up_color = self.up_center.colors[1]
        self.cube.debug = True
        print(self.cube, "\n start")
        self.cross(True)
        # self.down_corners(False)
        # self.second_layer(False)
        # self.oll_edges(False)
        # self.oll_corners(False)
        # self.pll_corners(False)
        # print(self.cube)
        # self.pll_edges(False)

        # print(self.translate_to_move_list(), len(self.translate_to_move_list()))

    def translate_to_move_list(self):
        m_list = []
        for m in self.cube.move_list:
            move = m[0]
            d = m[1]

            if   move == RIGHT and d ==  1: m_list.append("R" )
            elif move == RIGHT and d == -1: m_list.append("Ri")
            elif move == LEFT  and d ==  1: m_list.append("L" )
            elif move == LEFT  and d == -1: m_list.append("Li")
            elif move == BACK  and d ==  1: m_list.append("B" )
            elif move == BACK  and d == -1: m_list.append("Bi")
            elif move == FRONT and d ==  1: m_list.append("F" )
            elif move == FRONT and d == -1: m_list.append("Fi")
            elif move == UP    and d ==  1: m_list.append("U" )
            elif move == UP    and d == -1: m_list.append("Ui")
            elif move == DOWN  and d ==  1: m_list.append("D" )
            elif move == DOWN  and d == -1: m_list.append("Di")
        return m_list

    def orient_edge(self, front_face, side_face, d):
        self.cube.turn_face(self.up_center, d)
        self.cube.turn_face(side_face, d)
        self.cube.turn_face(front_face, -d)
        self.cube.turn_face(side_face, -d)

    def cross(self, debug):
        print(self.cube)
        down_edges = [
                        self.cube.solved_edge(self.down_center, self.right_center),  # dr
                        self.cube.solved_edge(self.down_center, self.left_center),   # dl
                        self.cube.solved_edge(self.down_center, self.front_center),  # df
                        self.cube.solved_edge(self.down_center, self.back_center)    # dl
                     ]
        # bring the edge to the up layer
        # if the edge is on the correct face but not the correct position turn it so that it is on the opposite face
        for edge in down_edges:
            if debug: print(edge, "start \n")
            if debug: print(self.cube)

            # check if the cubie is solved

            # figure out if the cubie is on an x-face or a z-face
            index = None
            for i in range(0, 3, 2):  # i = 0 then i = 2
                if self.cube.get_adj_centers(edge)[i].pos != 0:
                    index = i
            assert index is not None
            face = self.cube.get_adj_centers(edge)[index]
            if edge.colors[1] == self.down_center.colors[1] and edge.colors[index] == face.colors[index]:
                if debug: print(edge, "done")
                continue

            xzface = self.cube.get_adj_centers(edge)[index].pos
            if edge[1] == -1:  # the cubie is on the down face
                if debug: print("on down face")
                self.cube.turn_face(xzface, 1)

                self.cube.turn_face(xzface, 1)

            elif edge[1] == 0:  # the cubie is on the equator
                if debug: print("on equator layer")
                l_r_face = self.cube.get_adj_centers(edge)[0]
                if debug: print("on back face")
                d = edge[0] * edge[2]
                if debug: print(self.cube, '\n')
                self.cube.turn_face( l_r_face, d)
                self.cube.turn_face(self.up_center, 1)
                self.cube.turn_face(l_r_face, -d)

            if debug: print("on up layer")

            # step 2 bring the edge above the solved spot
            for i in range(0, 3, 2):  # i = 0 then i = 2
                if self.cube.get_adj_centers(edge)[i].pos != 0:
                    index = i

            # edge on top layer
            for i in range(3):
                if edge != self.cube.solved_edge(self.cube.get_adj_centers(edge)[index], self.cube.down_center()):
                    if debug: print("no match")
                    self.cube.turn_face(self.cube.get_adj_centers(edge)[1].pos, 1)
                    for j in range(0, 3, 2):  # j = 0 then j = 2
                        if self.cube.get_adj_centers(edge)[j].pos != 0:
                            index = j
                else:
                    if debug: print("match")
                    if debug: print(self.cube)
                    break

            # check if the edge is oriented correctly
            if edge.colors[1] != self.down_center.colors[1]:
                if debug: print("not oriented ")
                front_face = Point(edge["x"], edge["y"] - 1, edge["z"])
                side_face = self.cube.get_side_faces(front_face)[0]
                if debug: print("front case")
                self.orient_edge(front_face, side_face, 1)
                if debug: print(edge, "oriented")
            # the edge is oriented
            else:
                if debug: print("oriented")
                if debug: print(self.cube, '\n')

                index = None
                for j in range(0, 3, 2):
                    if self.cube.get_adj_centers(edge)[j].pos != 0:
                        index = j
                self.cube.turn_face(self.cube.get_adj_centers(edge)[index].pos, 1)
                self.cube.turn_face(self.cube.get_adj_centers(edge)[index].pos, 1)
            if debug: print(edge, "done")
        print(self.cube,"edges done!")

    def down_corners(self, debug):
        down_corners = [
                        self.cube.solved_corner(self.down_center, self.right_center, self.front_center),  # drf
                        self.cube.solved_corner(self.down_center, self.left_center, self.front_center),  # dlf
                        self.cube.solved_corner(self.down_center, self.left_center,self.back_center),  # df
                        self.cube.solved_corner(self.down_center, self.right_center,self.back_center)  # dl
                        ]
        for corner in down_corners:
            # if debug: print(corner, "start")
            self.cube.debug = False
            if corner["y"] == -1:
                face = self.cube.get_adj_centers(corner)[0]
                d = corner["x"] * corner["z"]
                self.cube.turn_face(face, d)
                self.cube.turn_face(self.up_center, d)
                self.cube.turn_face(face, -d)
            if debug: print("on top layer")
            if debug: print("move above solved position")
            for i in range(3):
                faces = self.cube.get_adj_centers(corner)
                if corner != self.cube.solved_corner(faces[0], faces[1].pos * -1, faces[2]):
                    if debug: print("no match")
                    self.cube.turn_face(self.up_center, 1)
                else:
                    if debug: print("match")
                    if debug: print(self.cube)
                    break
            if debug: print("orient and solve corner")
            d = corner["x"] * corner["z"]
            face = self.cube.get_adj_centers(corner)[0]
            if corner.colors[0] == self.down_center.colors[1]:
                if debug: print("D on right or left")
                self.cube.turn_face(face, d)
                self.cube.turn_face(self.up_center, d)
                self.cube.turn_face(face, -d)
            elif corner.colors[1] == self.down_center.colors[1]:
                if debug: print("D on up")
                self.cube.turn_face(face, d)
                self.cube.turn_face(self.up_center, -d)
                self.cube.turn_face(face, -d)
                self.cube.turn_face(self.up_center, -d)
                self.cube.turn_face(self.up_center, -d)
                self.cube.turn_face(face, d)
                self.cube.turn_face(self.up_center, d)
                self.cube.turn_face(face, -d)
            elif corner.colors[2] == self.down_center.colors[1]:
                if debug: print("D on front or back")
                self.cube.turn_face(self.up_center, d)
                self.cube.turn_face(face, d)
                self.cube.turn_face(self.up_center, -d)
                self.cube.turn_face(face, -d)
            if debug: print(corner, "end")
        print(self.cube, "corners done!")

    def _enter_edge(self, front, lr_face, d):
        # if d is pos the edge is on the left else it is on the right
        self.cube.turn_face(self.up_center,  d)
        self.cube.turn_face(lr_face,   d)
        self.cube.turn_face(self.up_center,  d)
        self.cube.turn_face(lr_face,  -d)
        self.cube.turn_face(self.up_center, -d)
        self.cube.turn_face(front,    -d)
        self.cube.turn_face(self.up_center, -d)
        self.cube.turn_face(front,     d)

    def second_layer(self, debug):
        if debug: print("solving second layer")
        edges = [
                self.cube.solved_edge(self.front_center, self.right_center),  # fr
                self.cube.solved_edge(self.front_center, self.left_center),  # fl
                self.cube.solved_edge(self.back_center, self.right_center),  # br
                self.cube.solved_edge(self.back_center, self.left_center)  # bl
                ]
        for edge in edges:
            if debug: print(edge, "start...")
            face = self.cube.get_adj_centers(edge)
            if edge["y"] == 0 and edge.colors[0] == face[0].colors[0] and edge.colors[2] == face[2].colors[2]:
                if debug: print("edge in right spot and correct orientation")
                continue
            face = None

            if edge["y"] == 0:
                if debug: print("edge is on equator not solved")
                # bring to the top layer
                front = side = d = None
                face = self.cube.get_adj_centers(edge)
                if edge["x"] == -1:
                    if debug: print("on equator layer on left face")
                    front = self.left_center
                    d = edge["z"]
                elif edge["x"] == 1:
                    if debug: print("on equator layer and on right face")
                    front = self.right_center
                    d = -edge["z"]
                if debug: print(self.cube)

                side = face[2].pos
                self._enter_edge(front, side, d)

            if debug: print("edge on top layer")

            # bring above the solved center
            for i in range(3):
                front_face = face_index = None
                face = self.cube.get_adj_centers(edge)
                for j in range(0, 3, 2):
                    if edge.colors[j] is not None:
                        front_face = face[j]
                        face_index = j
                if edge.colors[face_index] != front_face.colors[face_index]:
                    if debug: print("no match")
                    self.cube.turn_face(self.up_center, 1)

            if debug: print("match")
            if debug: print(self.cube)

            # get the front face axis and the side face axis
            front_face_index = side_face_index = None
            for i in range(0, 3, 2):
                if edge.colors[i] is not None:
                    front_face_index = i
                else:
                    side_face_index = i
            front_face = self.cube.get_adj_centers(edge)[front_face_index]
            side_faces = self.cube.get_side_faces(front_face)
            side_face = None
            # checking if the edge is on the z face or the x face
            for i in range(2):
                if edge.colors[1] == side_faces[i].colors[side_face_index]:
                    side_face = side_faces[i]
            d = 1

            # may or may not be complete lol
            if   front_face.pos == self.front_center.pos and side_face.pos == self.left_center.pos : d = -1
            elif front_face.pos == self.left_center.pos and side_face.pos == self.back_center.pos  : d = -1
            elif front_face.pos == self.back_center.pos and side_face.pos == self.right_center.pos : d = -1
            elif front_face.pos == self.right_center.pos and side_face.pos == self.front_center.pos: d = -1

            self._enter_edge(front_face, side_face, d)
            if debug: print(edge)
        print(self.cube, "second layer done")

    def across(self, front , side, d):
        self.cube.turn_face(front, d)
        self.cube.turn_face(side, d)
        self.cube.turn_face(self.up_center, d)
        self.cube.turn_face(side, -d)
        self.cube.turn_face(self.up_center, -d)
        self.cube.turn_face(front, -d)

    def diag(self, front, side , d):
        self.cube.turn_face(front, d)
        self.cube.turn_face(side, d)
        self.cube.turn_face(self.up_center, -d)
        self.cube.turn_face(side, -d)
        self.cube.turn_face(self.up_center, -d)
        self.cube.turn_face(side, d)
        self.cube.turn_face(self.up_center, d)
        self.cube.turn_face(side, -d)
        self.cube.turn_face(front, -d)

    def orient_edges(self, front, side, d):
        # F R U r u f
        self.across(front, side, d)

        self.cube.turn_face(self.up_center, d)
        self.cube.turn_face(self.up_center, d)

        # F R u r u R U r f
        self.diag(front, side, d)

    def oll_edges(self, debug):
        # getting the edges that are not oriented
        up = self.cube.face(self.up_center.pos)
        u_edges = []
        for cubie in up:
            if cubie.type == "edge" and cubie.colors[1] != self.up_color:
                u_edges.append(cubie)
                print(cubie)
        if len(u_edges) == 4:
            if debug: print("no edges oriented")
            self.orient_edges(self.front_center, self.right_center, 1)
        print(self.cube)
        if len(u_edges) == 2:
            print("2 edges oriented")
            # 2 cases
            """
            F R u r u R U r f
            edges diagonal to each other
            - U -
            U U W
            - W -
            """


            """
            F R U r u f
            edges opposite to each other
            - W -
            U U U
            - W -
            """
            self.cube.turn_face(self.up_center, -1)
            self.cube.turn_face(self.up_center, -1)
            self.cube.turn_face(self.up_center, -1)

            if u_edges[0].pos + u_edges[1].pos == Point(0,2,0):
                if debug: print("edges across from each other")
                faces = self.cube.get_adj_centers(u_edges[0])
                if faces[0].pos == 0:
                    front = faces[2]
                    side = self.cube.get_side_faces(front)[1]

                else:
                    front = faces[0]
                    side = self.cube.get_side_faces(front)[1]
                print(front, side, "degubber")
                d = 1
                self.cube.turn_face(front, d)
                self.cube.turn_face(side, d)
                self.cube.turn_face(self.up_center, d)
                self.cube.turn_face(side, -d)
                self.cube.turn_face(self.up_center, -d)
                self.cube.turn_face(front, -d)
            elif Point(u_edges[0].pos + u_edges[1].pos).abs_length() == 4:
                if debug: print("edges diag from each other")
                front = self.cube.get_adj_centers(u_edges[0])[0]
                if front.pos == 0:
                    front = self.cube.get_adj_centers(u_edges[0])[2]
                side = self.cube.get_adj_centers(u_edges[1])[0]
                if side.pos == 0:
                    side = self.cube.get_adj_centers(u_edges[1])[2]
                d = 1
                if   front == self.front_center and side == self.left_center : d = -1
                elif front == self.left_center  and side == self.back_center : d = -1
                elif front == self.back_center  and side == self.right_center: d = -1
                elif front == self.right_center and side == self.front_center: d = -1
                self.diag(front, side, d)
        print("OLL edges done \n", self.cube)

    def corner_orientation(self, face, d):
        self.cube.turn_face(face, -d)
        self.cube.turn_face(self.up_center, -d)
        self.cube.turn_face(face, d)
        self.cube.turn_face(self.up_center, -d)
        self.cube.turn_face(face, -d)
        self.cube.turn_face(self.up_center, d)
        self.cube.turn_face(self.up_center, d)
        self.cube.turn_face(face, d)

    def oll_corners(self, debug):

        corners = [
                    self.cube.solved_corner(self.up_center, self.left_center,  self.front_center),  # ulf
                    self.cube.solved_corner(self.up_center, self.left_center,  self.back_center),   # ulb
                    self.cube.solved_corner(self.up_center, self.right_center, self.back_center),   # urb
                    self.cube.solved_corner(self.up_center, self.right_center, self.front_center)   # urf
                  ]
        # no up yellows or 2 up yellows
        count = None
        up = self.cube.face(self.up_center)
        count = 0
        for cubie in up:
            if cubie.type == "corner" and cubie.colors[1] == self.up_color:
                count += 1

        while count != 1:
            if debug: print("either none or 2 up corners")
            good_corner = None
            # find the corner that has a good orientation
            corner = self.cube.get_cubie(Point(-1,1,1))
            k = 0
            for i in range(4):
                # go cw around the corners
                if corner.colors[k] == self.up_color:
                    good_corner = corner
                    if debug: print("good corner = ", good_corner)
                    break
                corner = self.cube.get_cubie(ROT_XZ_CW * corner.pos)
                if k == 0: k = 2
                else: k = 0

            # bring the good corner to (-1,1,1)
            if good_corner is not None:
                for i in range(3):
                    if good_corner.pos != Point(-1,1,1):
                        self.cube.turn_face(self.up_center, 1)
                        if debug:print("good corner not in correct pos yet")
                if debug: print("good corner in the bottom left\n", self.cube)
                self.corner_orientation(self.right_center, -1)

            else:
                if debug: print("no good corner")
                self.corner_orientation(self.right_center, -1)

            up = self.cube.face(self.up_center)
            count = 0
            for cubie in up:
                if cubie.type == "corner" and cubie.colors[1] == self.up_color:
                    count += 1

        # there is only one up corner now
        if debug: print("one up corner\n", self.cube)
        oriented_c = None
        for c in corners:
            if c.colors[1] == self.up_color:
                oriented_c = c
                break
        cw_cubie = self.cube.get_cubie(Point(ROT_XZ_CW * oriented_c.pos))
        cc_cubie = self.cube.get_cubie(Point(ROT_XZ_CC * oriented_c.pos))

        for i in range(4):
            if oriented_c.pos == Point(1,1,1) and cw_cubie.colors[2] == self.up_color:
                if debug: print("oriented corner in the bottom right\n", self.cube)
                self.corner_orientation(self.left_center, 1)
            elif oriented_c.pos == Point(-1,1,1) and cc_cubie.colors[2] == self.up_color:
                if debug: print("oriented corner in the bottom left\n", self.cube)
                self.corner_orientation(self.right_center, -1)
            else:
                self.cube.turn_face(self.up_center, 1)
        print("OLL corners done \n", self.cube)

    def swap_corners(self, front , side, d):
        # R U r u r F r r u r u R U r f
        self.cube.turn_face(side, d)
        self.cube.turn_face(self.up_center, d)
        self.cube.turn_face(side, -d)
        self.cube.turn_face(self.up_center, -d)
        self.cube.turn_face(side, -d)
        self.cube.turn_face(front, d)
        self.cube.turn_face(side, d)
        self.cube.turn_face(side, d)
        self.cube.turn_face(self.up_center, -d)
        self.cube.turn_face(side, -d)
        self.cube.turn_face(self.up_center, -d)
        self.cube.turn_face(side, d)
        self.cube.turn_face(self.up_center, d)
        self.cube.turn_face(side, -d)
        self.cube.turn_face(front, -d)

    def swap_diag_corners(self, d):

        self.cube.turn_face(self.front_center, d)
        self.cube.turn_face(self.right_center, d)
        self.cube.turn_face(self.up_center, -d)

        self.cube.turn_face(self.right_center, -d)
        self.cube.turn_face(self.up_center, -d)
        self.cube.turn_face(self.right_center, d)

        self.cube.turn_face(self.up_center, d)
        self.cube.turn_face(self.right_center, -d)
        self.cube.turn_face(self.front_center, -d)

        self.cube.turn_face(self.right_center, d)
        self.cube.turn_face(self.up_center, d)
        self.cube.turn_face(self.right_center, -d)

        self.cube.turn_face(self.up_center, -d)
        self.cube.turn_face(self.right_center, -d)
        self.cube.turn_face(self.front_center, d)

        self.cube.turn_face(self.right_center, d)
        self.cube.turn_face(self.front_center, -d)

    def pll_corners(self, debug):
        # self.cube.turn_face(self.up_center, -1)
        corners = [c for c in self.cube.face(self.up_center) if c.type == "corner"]
        if debug: print("start \n", self.cube)
        # check if any of the corners are permutated
        corner = self.cube.get_cubie(-1,1,1)
        s = 0
        oriented_pairs = 0
        x_or_z = None
        pairs = []
        front = side = None
        faces = [self.left_center, self.back_center, self.right_center, self.front_center]
        # counting the number of permutated pairs
        for i in range(4):
            cw = self.cube.get_cubie(ROT_XZ_CW * corner.pos)
            if corner.colors[s] == cw.colors[s]:
                oriented_pairs += 1
                print(oriented_pairs)
                # keep track of the face that the permutated pair is on

                x_or_z = s
                pairs.append(corner)
                pairs.append(cw)
                front = faces[i-1]
                side = faces[i-2]

            if s == 0: s = 2
            else: s = 0
            corner = cw
        if debug: print("num oriented pairs:", oriented_pairs)
        # 3. no corners permutated
        if oriented_pairs == 0:
            self.swap_diag_corners(1)
        # 2 corners permutated
        elif oriented_pairs == 1:
            d = 1
            if front == self.front_center and side == self.left_center:
                d = -1
            elif front == self.left_center and side == self.back_center:
                d = -1
            elif front == self.back_center and side == self.right_center:
                d = -1
            elif front == self.right_center and side == self.front_center:
                d = -1
            if debug: print("side:", side,"front:", front, d)
            self.swap_corners(front, side, d)
        else:
            # all corners permutated
            pass
        if debug: print("corners permutated \n", self.cube)

    def rotate_edges(self, front, d):
        left, right = self.cube.get_side_faces(front)
        self.cube.turn_face(front, 1)
        self.cube.turn_face(front, 1)
        self.cube.turn_face(self.up_center, d)
        self.cube.turn_face(left, 1)
        self.cube.turn_face(right, -1)
        self.cube.turn_face(front, 1)
        self.cube.turn_face(front, 1)
        self.cube.turn_face(left, -1)
        self.cube.turn_face(right, 1)
        self.cube.turn_face(self.up_center, d)
        self.cube.turn_face(front, 1)
        self.cube.turn_face(front, 1)

    def pll_edges(self, debug):
        # check if a rotation is needed
        faces = [self.left_center, self.back_center, self.right_center, self.front_center]
        s = 0
        edge = self.cube.get_cubie(-1, 1, 0)
        corner = self.cube.get_cubie(-1, 1, -1)
        matches = 0
        front = None
        for i in range(4):
            if edge.colors[s] == corner.colors[s]:
                matches += 1
                front = faces[i - 2]
            else:
                if debug: print("no match")
            if s == 0: s = 2
            else: s = 0
            edge = self.cube.get_cubie(ROT_XZ_CW * edge.pos)
            corner = self.cube.get_cubie(ROT_XZ_CW * corner.pos)
            # if a there is only one match a rotaion is needed
        if matches == 1:
            # find which direction the edges need to be rotated
            adj_faces = self.cube.get_adj_centers(front)
            left, right = self.cube.get_side_faces(adj_faces)
            for i in range(0,3,2):
                if front.colors[i] is not None:
                    s = i
            if front.colors[s] == left.colors[s]:
                d = -1
            else: d = 1
            self.rotate_edges(front, d)
        # turn the up layer until it is the cube is solved
        for i in range(4):
            if self.cube.get_cubie(-1,1,1).colors[0] != self.left_center.colors[0]:
                self.cube.turn_face(self.up_center, 1)
