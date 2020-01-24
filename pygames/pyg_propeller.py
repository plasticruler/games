import pyglet
from pyglet.gl import *
import math
import numpy as np

window = pyglet.window.Window()

@window.event
def on_draw():
    glBegin(GL_LINES)
    glVertex3f(100.0, 100.0, 0.25)
    glVertex3f(200.0, 300.0, -0.75)
    glEnd()    

pyglet.app.run()