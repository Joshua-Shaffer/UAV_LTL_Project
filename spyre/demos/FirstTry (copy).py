import math
import sys
import atexit
import numpy
import time
from controller_obs import ExampleCtrl

import pygame
import OpenGL.GL as ogl
import OpenGL.GLU as oglu

sys.path.append('..')
import spyre
import zoe_objects as zoeobj

# TODO for general cases. Create "System class" that will interpret controller
# and create necessary classes based on number of systems and environment (
# i.e. populate the grid and initial environments)

Ctrl = ExampleCtrl()
X0 = numpy.array([0.0, 0.0, 0.0])
X1 = numpy.array([0.0, 1.0, 0.0])
X2 = numpy.array([0.0, 2.0, 0.0])
X3 = numpy.array([0.0, 0.0, 1.0])
X4 = numpy.array([0.0, 1.0, 1.0])
X5 = numpy.array([0.0, 2.0, 1.0])

List_pos = dict()
List_pos['X0'] = X0
List_pos['X1'] = X1
List_pos['X2'] = X2
List_pos['X3'] = X3
List_pos['X4'] = X4
List_pos['X5'] = X5


class CheckerUp(object):

    def Updated(self):
        Tell = True#input("Park? ")
        # Get user input for park
        if (Tell == True):
            park = True
        else:
            park = False

        yout = Ctrl.move(park)
        #print("made it here")
        #print(yout["loc"])
        return List_pos[yout["loc"]]

    def Check(self, x, y, z,spot = numpy.array):
        eps = 0.001
        #print("this is spot")
        #print(spot[0])
        #print(spot[1])
        #print(spot[2])
        #print("this is xyz")
        #print(x)
        #print(y)
        #print(z)
        #print("This is truth statements")
        #print(abs(spot[0]-x) <= eps)
        #print(abs(spot[1]-y) <= eps)
        #print(abs(spot[2]-z) <= eps)
        if (abs(spot[0]-x) <= eps and abs(spot[1]-y) <= eps and abs(spot[2]-z) <= eps):
            return True
        else:
            return False



MoverSign = 0
MoverSign2 = 0
l = CheckerUp()
PARTICLES = 1 # the number of particles
position_ell = numpy.array([0,0,0])
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

        #oglu.gluCylinder(self.quad , self.radius/2.0, self.radius/2.0,
        #             self.height, 60, 70)

        #ogl.glTranslate(0, 0, self.radius)
        oglu.gluSphere(self.quad, self.radius, 60, 60)

        #ogl.glTranslate(0, 0, -self.height-self.radius)
        #oglu.gluSphere(self.quad, self.radius, 60, 60)

        ogl.glPopMatrix()

    def update(self):
        global position_ell
        global MoverSign
        if (MoverSign == 1):
            position_ell[0] = self.x
            position_ell[1] = self.y
            position_ell[2] = self.z

            #time.sleep(1)
            #print(self.pos)
            #zoeobj.Particle.update(self)
            #deltaX = (self.SIGMA*(y - x))*self.DELTA_T
            #deltaY = (self.RHO*x - y - x*z)*self.DELTA_T
            #deltaZ = (-self.B*z + x*y)*self.DELTA_T
            #x += deltaX
            #y += deltaY
            #z += 0.1*deltaZ

            spot = l.Updated()

            DISTANCE = numpy.subtract(spot, position_ell)
            #print(DISTANCE)
            xs, y, z = [x for x in position_ell]
            Inx, Iny, Inz = [x/10.0 for x in DISTANCE]
            #print("This is intervals")
            #print(Inx)
            #print(Iny)https://ntst.umd.edu/testudo/#/main/studentAccountInquiry?null
            #print(Inz)
            # TODO method to grap if global variable was changed then move forward

            while (l.Check(xs,y,z,spot) == False):

                xs = xs + Inx
                #print(xs)
                y = y + Iny
                #print(y)
                z = z + Inz
                #print(z)
                #yololo = input("Yes?")
                position_ell = [x for x in (xs,y,z)]
                #self.t += self.DELTA_T
                #print(xs)
                #print(Inx)

            self.x = round(position_ell[0])
            self.y = round(position_ell[1])
            self.z = round(position_ell[2])
            ogl.glTranslate(self.x, self.y, self.z)
            #self.display()
            MoverSign = 0
        else:
            pass
        #self.pos = [round(x) for x in self.pos]

'''class LorenzParticle(zoeobj.Particle):

    """A Lore        print(Current[1])
        print(Current[2])nz particle simply moves according to the Lorenz
    differential equations described above.
    """
    SIGMA = 10.0
    RHO = 28.0
    B = 8.0/3.0
    DELTA_T = 0.01
    DISTANCE = numpy.array([1.0, 1.0, 1.0])


    trailLength = 2

    def __init__(self, start):
        zoeobj.Particle.__init__(self, start)
        self.t = 0.0

    def update(self):
        global spot
        global MoverSign2
        if (MoverSign2 == 1):
            #time.sleep(1)
            #print(self.pos)
            zoeobj.Particle.update(self)
            #deltaX = (self.SIGMA*(y - x))*self.DELTA_T
            #deltaY = (self.RHO*x - y - x*z)*self.DELTA_T
            #deltaZ = (-self.B*z + x*y)*self.DELTA_T
            #x += deltaX
            #y += deltaY
            #z += 0.1*deltaZ
            spot = l.Updated()

            DISTANCE = numpy.subtract(spot, self.pos)
            #print(DISTANCE)
            xs, y, z = [x for x in self.pos]
            Inx, Iny, Inz = [x/10.0 for x in DISTANCE]
            #print("This is intervals")
            #print(Inx)
            #print(Iny)
            #print(Inz)
            while (l.Check(xs,y,z,spot) == False):

                xs = xs + Inx
                #print(xs)
                y = y + Iny
                #print(y)
                z = z + Inz
                #print(z)
                #yololo = input("Yes?")
                self.pos = [x for x in (xs,y,z)]
                self.t += self.DELTA_T
                #print(xs)
                #print(Inx)

            self.pos = [round(x) for x in self.pos]
            MoverSign2 = 0
        else:
            pass

class LorenzGroup(spyre.Group):

    """A Lorenz group creates a collection of particles that all have
    very nearly the same position, differing only by a very small
    amount."""

    BASE = 0.0 # the starting position
    VARIANCE = 0.0 # the variance of all particles

    def __init__(self, count):
        spyre.Group.__init__(self)
        for i in range(1, count + 1):
            xyz = self.BASE + i*self.VARIANCE/count
            self.append(LorenzParticle((xyz,)*3))'''

class userinput(spyre.PivotingInterface):

    def keyPressed(self, key):
        global MoverSign
        global MoverSign2
        if (key == 'm'):
            MoverSign = 1
            MoverSign2 = 1


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
    #engine.addCamera(spyre.BasicCameraFrustum(engine,(3,3,5),(0,0,0),(0,0,1),-3.0,3.0,-3.0,3.0,1.0,10.0))
    #camera = spyre.BasicCamera(engine,(10,10,10),(0,0,0),(0,0,20))
    #camera.displayViewport()
    engine.studio = spyre.StudioColorMat(engine)

    #light0 = spyre.Bulb([0.5,0.6,0.5,1.0],  # ambient
    #                    [0.6,0.7,0.7,1.0],  # diffuse
    #                    [0.3,0.3,0.3,1.0], ) # specular

    #orbiter = zoeobj.RotatingGroup(0.03, objects=[light0], ray=(1,0,0))
    #engine.studio.addMobileLight(light0, orbiter, (0,10,10))

    # add the various objects to the engine
    engine.add(zoeobj.AxesObject())
    engine.add(zoeobj.GridObject())
    #engine.add(LorenzGroup(PARTICLES))
    #spyre.spyre.BasicCamera.__init__(engine,(0,0,0))
    engine.add(DumbBell(2,.25))
    #engine.add(userinput(engine))
    # TODO setup user interface for accessing variable change on click or text
    # entering. Mainly "Move" command and the "park" command
    atexit.register(postMortem, engine)

    # run the event loop
    engine.go()

if __name__ == '__main__':
    main()
