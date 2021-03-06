# CENG 487 Assignment4 by
# Elif Duran
# StudentId: 230201002
# December 2019

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from scene import Scene

ESCAPE = '\033'
window = 0

if len(sys.argv) < 2:
    input = "tori.obj"
else:
    input = sys.argv[1]
scene = Scene(input)
scene.init()


def InitGL(Width, Height):
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width) / float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


def ReSizeGLScene(Width, Height):
    if Height == 0:
        Height = 1

    glViewport(0, 0, Width, Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width) / float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


def DrawGLScene():
    global scene
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    glTranslatef(0.0, -0.4, -3.0)
    glRotatef(-40, 1.0, 0.0, 0.0)
    scene.render()
    glutSwapBuffers()


def keyPressed(*argv):
    if argv[0] == b'\x1b':
        sys.exit()
    elif argv[0] == b'a':
        scene.key_pressed('increase')
    elif argv[0] == b'e':
        scene.key_pressed('decrease')
    elif argv[0] == b'r':
        scene.key_pressed('reset')


def special_key(key, x, y):
    global scene
    if key == GLUT_KEY_LEFT:
        scene.key_pressed('left')
    elif key == GLUT_KEY_RIGHT:
        scene.key_pressed('right')


def main():
    global window
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow("Elofin")
    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyPressed)
    glutSpecialFunc(special_key)
    InitGL(640, 480)
    glutMainLoop()


print("Hit ESC key to quit.")
print("Press 'a' to increase subdivision.")
print("Press 'e' to decrease subdivision.")
print("Press 'r' to reset subdivision.")
main()
