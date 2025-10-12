#pip install PyOpenGL PyOpenGL_accelerate
# board3d.py
# Requisitos: PyOpenGL, PyOpenGL_accelerate, freeglut
# board3d_bottom.py
# board3d_bottom.py
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

GRID_SIZE = 16
CELL = 1.0
SPHERE_RADIUS = 0.25
CAM_DISTANCE = 22.0

window_width = 900
window_height = 700

user_x = 0
user_y = 0
board = None

def loads(files):
    ll=True
    a=[]
    with open(files,"r") as f1:
        ttt=f1.read()
    yyy=ttt.split("\n")
    yi=len(yyy)
    for y in range(yi):
        xxx=yyy[y].split(",")
        xi=len(xxx)
        if ll:
            a=[[" " for _ in range(xi)] for __ in range(yi)]
        ll=False
        for x in range(xi):
            b=xxx[x].strip()
            a[y][x]=b if b!="" else " "
    return a

def world_pos_from_index(ix, iy):
    half = (GRID_SIZE - 1) * CELL / 2.0
    wx = ix * CELL - half
    wz = iy * CELL - half
    return wx, wz

def init_gl():
    glClearColor(1.0, 1.0, 0.1, 1.0)  # 🌟 fundo amarelo
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, [5.0, 10.0, 5.0, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.9,0.9,0.9,1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [0.6,0.6,0.6,1.0])

angle = 35.0
rot = 0.0

def draw_grid():
    """Desenha o tabuleiro 16x16 tipo xadrez."""
    glDisable(GL_LIGHTING)
    half = (GRID_SIZE - 1) * CELL / 2.0
    glBegin(GL_QUADS)
    for iy in range(GRID_SIZE):
        for ix in range(GRID_SIZE):
            wx = -half + ix * CELL
            wz = -half + iy * CELL
            # cor alternada
            if (ix + iy) % 2 == 0:
                glColor3f(0.85, 0.85, 0.1)  # claro
            else:
                glColor3f(0.65, 0.65, 0.65)  # escuro
            glVertex3f(wx, 0.0, wz)
            glVertex3f(wx + CELL, 0.0, wz)
            glVertex3f(wx + CELL, 0.0, wz + CELL)
            glVertex3f(wx, 0.0, wz + CELL)
    glEnd()
    glEnable(GL_LIGHTING)



def draw_board_spheres():
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.2,0.2,0.2,1.0])
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 30.0)
    for iy in range(min(GRID_SIZE, len(board))):
        row = board[iy]
        for ix in range(min(GRID_SIZE, len(row))):
            if str(row[ix]).strip() != "":
                wx, wz = world_pos_from_index(ix, iy)
                glPushMatrix()
                glTranslatef(wx, SPHERE_RADIUS, wz)
                glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [0.0,0.1,0.8,1.0])
                glutSolidSphere(SPHERE_RADIUS, 20, 20)
                glPopMatrix()

def draw_user_sphere():
    wx, wz = world_pos_from_index(user_x, user_y)
    glPushMatrix()
    glTranslatef(wx, SPHERE_RADIUS, wz)
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [0.9,0.1,0.1,1.0])
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.9,0.9,0.9,1.0])
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 60.0)
    glutSolidSphere(SPHERE_RADIUS*1.15, 24, 24)
    glPopMatrix()

def display():
    global rot
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    eye_y = CAM_DISTANCE * 0.5
    eye_x = 0.0
    eye_z = CAM_DISTANCE
    gluLookAt(eye_x, eye_y, eye_z, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    #glRotatef(-angle, 1.0, 0.0, 0.0)
    #glRotatef(rot, 0.0, 1.0, 0.0)

    glTranslatef(0.0, -5.0, 0.0)   # 🌟 move o tabuleiro para baixo (mais perto do fundo do ecrã)

    glDisable(GL_LIGHTING)
    glColor3f(0.95, 0.95, 0.9)
    half = (GRID_SIZE - 1) * CELL / 2.0 + 1.0
    glBegin(GL_QUADS)
    glVertex3f(-half, -0.001, -half)
    glVertex3f(half, -0.001, -half)
    glVertex3f(half, -0.001, half)
    glVertex3f(-half, -0.001, half)
    glEnd()
    glEnable(GL_LIGHTING)

    draw_grid()
    draw_board_spheres()
    draw_user_sphere()

    glutSwapBuffers()
    rot += 0.2

def reshape(w,h):
    global window_width, window_height
    window_width = w
    window_height = h
    glViewport(0,0,w,h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(w)/float(h if h>0 else 1), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def special_key(key, x, y):
    global user_x, user_y
    if key == GLUT_KEY_LEFT:
        user_x = max(0, user_x - 1)
    elif key == GLUT_KEY_RIGHT:
        user_x = min(GRID_SIZE - 1, user_x + 1)
    elif key == GLUT_KEY_UP:
        user_y = max(0, user_y - 1)
    elif key == GLUT_KEY_DOWN:
        user_y = min(GRID_SIZE - 1, user_y + 1)
    glutPostRedisplay()

def keyboard(key, x, y):
    if key == b'\x1b' or key == b'q':
        sys.exit(0)

def main():
    global board, user_x, user_y
    try:
        board = loads("xy.csv")
        print("xy.csv carregado: {}x{}".format(len(board), len(board[0]) if board else 0))
    except Exception as e:
        print("Erro ao carregar xy.csv:", e)
        board = [[" " for _ in range(GRID_SIZE)] for __ in range(GRID_SIZE)]

    user_x = GRID_SIZE // 2
    user_y = GRID_SIZE // 2

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow(b"Tabuleiro 3D - fundo amarelo")
    init_gl()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutSpecialFunc(special_key)
    glutKeyboardFunc(keyboard)
    glutIdleFunc(glutPostRedisplay)
    glutMainLoop()

if __name__ == "__main__":
    main()
