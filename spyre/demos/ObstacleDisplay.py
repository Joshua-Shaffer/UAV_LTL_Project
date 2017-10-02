import math
import sys
import atexit
import numpy
import time
from controller_obs3 import ExampleCtrl

import pygame
import OpenGL.GL as ogl
import OpenGL.GLU as oglu

sys.path.append('..')
import spyre
import zoe_objects as zoeobj

# TODO for general cases. Create "System class" that will interpret controller
# and create necessary classes based on number of systems and environment (
# i.e. populate the grid and initial environments)
# TODO npt toolbox in Matlab
Ctrl = ExampleCtrl()
X0 = numpy.array([0.0, 0.0, 0.0])
X1 = numpy.array([0.0, 1.0, 0.0])
X2 = numpy.array([0.0, 2.0, 0.0])
X3 = numpy.array([0.0, 0.0, 1.0])
X4 = numpy.array([0.0, 1.0, 1.0])
X5 = numpy.array([0.0, 2.0, 1.0])
X6 = numpy.array([0.0, 0.0, 2.0])
X7 = numpy.array([0.0, 1.0, 2.0])
X8 = numpy.array([0.0, 2.0, 2.0])

List_pos = dict()
List_pos['X0'] = X0
List_pos['X1'] = X1
List_pos['X2'] = X2
List_pos['X3'] = X3
List_pos['X4'] = X4
List_pos['X5'] = X5
List_pos['X6'] = X6
List_pos['X7'] = X7
List_pos['X8'] = X8


obs_pos = 1

class CheckerUp(object):

    def Updated(self, obs_pos):
        yout = Ctrl.move(obs_pos)
        return List_pos[yout["loc"]]

    def Check(self, x, y, z,spot = numpy.array):
        eps = 0.001
        if (abs(spot[0]-x) <= eps and abs(spot[1]-y) <= eps and abs(spot[2]-z) <= eps):
            return True
        else:
            return False



MoverSign = 0
MoverSign2 = 0
l = CheckerUp()
PARTICLES = 1 # the number of particles
position_ell = numpy.array([0,0,0])
position_ell2 = numpy.array([0.0, 1.0, 0.0])
print("Hello")

# TODO create 2 more classes for park locations and goals?
# TODO include in those classes method for turning on and off (might have to
# move far off grid)
class DumbBell(spyre.Object):
    """draws a dumbbell object """
    def __init__(self, height, radius, x=0, y=0, z=0):
        spyre.Object.__init__(self)
        self.height = height
        self.radius = radius
        self.x      = x
        self.y      = y
        self.z      = z
        self.quad   = oglu.gluNewQuadric()

    def display(self):
        ogl.glColor4f(0.5, 0.5, 0.5, 1)
        ogl.glPushMatrix()
        ogl.glTranslate(self.x, self.y, self.z)

        ogl.glMaterialfv(ogl.GL_FRONT, ogl.GL_AMBIENT, [0.1745, 0.0, 0.1, 0.0])
        ogl.glMaterialfv(ogl.GL_FRONT, ogl.GL_DIFFUSE, [0.5, 0.5, 0.5, 0.1])
        ogl.glMaterialfv(ogl.GL_FRONT, ogl.GL_SPECULAR, [0.7, 0.6, 0.8, 0.0])
        ogl.glMaterialf(ogl.GL_FRONT, ogl.GL_SHININESS, 50)
        oglu.gluSphere(self.quad, self.radius, 60, 60)


        ogl.glPopMatrix()

    def update(self):
        global position_ell
        global MoverSign
        global position_ell2
        if (MoverSign == 1):
            position_ell[0] = self.x
            position_ell[1] = self.y
            position_ell[2] = self.z

            if (position_ell2[0] == 0.0 and position_ell2[1] == 1.0 and position_ell2[2] == 0.0):
                spot = l.Updated(0)
            elif (position_ell2[0] == 0.0 and position_ell2[1] == 2.0 and position_ell2[2] == 1.0):
                spot = l.Updated(1)
            elif (position_ell2[0] == 0.0 and position_ell2[1] == 0.0 and position_ell2[2] == 2.0):
                spot = l.Updated(2)

            #DISTANCE = numpy.subtract(spot, position_ell)
            position_ell[0] = spot[0]
            position_ell[1] = spot[1]
            position_ell[2] = spot[2]

            self.x = round(position_ell[0])
            self.y = round(position_ell[1])
            self.z = round(position_ell[2])
            ogl.glTranslate(self.x, self.y, self.z)
            MoverSign = 0
        else:
            pass

class Obstacle(spyre.Object):
    """draws a dumbbell object """
    def __init__(self, height, radius, x=0, y=1, z=0):
        spyre.Object.__init__(self)
        self.height = height
        self.radius = radius
        self.x      = x
        self.y      = y
        self.z      = z
        self.quad   = oglu.gluNewQuadric()

    def display(self):
        ogl.glColor4f(0.5, 1, 0.5, 1)
        ogl.glPushMatrix()
        ogl.glTranslate(self.x, self.y, self.z)

        ogl.glMaterialfv(ogl.GL_FRONT, ogl.GL_AMBIENT, [0.1745, 0.0, 0.1, 0.0])
        ogl.glMaterialfv(ogl.GL_FRONT, ogl.GL_DIFFUSE, [0.5, 0.5, 0.5, 0.1])
        ogl.glMaterialfv(ogl.GL_FRONT, ogl.GL_SPECULAR, [0.7, 0.6, 0.8, 0.0])
        ogl.glMaterialf(ogl.GL_FRONT, ogl.GL_SHININESS, 50)

        oglu.gluSphere(self.quad, self.radius, 60, 60)

        ogl.glPopMatrix()

    def update(self):
        global position_ell2
        self.x = position_ell2[0]
        self.y = position_ell2[1]
        self.z = position_ell2[2]
        ogl.glTranslate(position_ell2[0],position_ell2[1],position_ell2[2])




class userinput(spyre.PivotingInterface):

    def keyPressed(self, key):
        global MoverSign
        global MoverSign2
        global position_ell2
        if (key == 'm'):
            MoverSign = 1
            MoverSign2 = 1
        elif(key == 'q'):
            position_ell2[0] = 0.0
            position_ell2[1] = 1.0
            position_ell2[2] = 0.0
        elif(key == 'w'):
            position_ell2[0] = 0.0
            position_ell2[1] = 2.0
            position_ell2[2] = 1.0
        elif(key == 'e'):
            position_ell2[0] = 0.0
            position_ell2[1] = 0.0
            position_ell2[2] = 2.0

def postMortem(engine):
    """ displays frame rate to stderr at end of run """
    print >> sys.stderr, "frame %d rate %.2f" % \
               (spyre.Object.runTurn, engine.runTimer.frameRate)
    print >> sys.stderr, "ortho %d, %d, %d, %d, %d, %d" % \
                (engine.camera.left, engine.camera.right,
                 engine.camera.top, engine.camera.bottom,
                 engine.camera.near, engine.camera.far)
    print >> sys.stderr, "eye <%f %f %f> " % engine.camera.eye





def main():
    """ main block """
    pygame.init()

    # create the engine
    engine = spyre.Engine()
    ie = userinput(engine)

    engine.studio = spyre.StudioColorMat(engine)


    # add the various objects to the engine
    engine.add(zoeobj.AxesObject())
    engine.add(zoeobj.GridObject())
    engine.add(DumbBell(2,.25))
    engine.add(Obstacle(2,.25))

    # TODO setup user interface for accessing variable change on click or text
    # entering. Mainly "Move" command and the "park" command
    atexit.register(postMortem, engine)

    # run the event loop
    engine.go()

if __name__ == '__main__':
    main()
