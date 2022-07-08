from solve import Solve
from solve_cubie import Solve_Cubie
from solve_cube import Solve_Cube
# UUUUUUUUULLLFFFRRRBBBLLLFFFRRRBBBLLLFFFRRRBBBDDDDDDDDD
t = "GGWOYBOWRRYBYBYBYRBYYWOOWBBRRWGGRRRYOYOBOOWOWGRWGWGGBG"
n = ""
for i in t:
    if i == "B":
        n += "F"
    elif i == "G":
        n += "B"
    elif i == "O":
        n += "L"
    elif i == "R":
        n += "R"
    elif i == "Y":
        n += "U"
    elif i == "W":
        n += "D"
print(n)
s = Solve(n)
print(s.cube)