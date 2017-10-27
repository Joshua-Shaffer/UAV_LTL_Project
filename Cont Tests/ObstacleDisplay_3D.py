import math
import sys
import atexit
import numpy
import time
from Cont_controller_3D_multiObs import ExampleCtrl
#from controller_obs3 import ExampleCtrl

import pygame
import OpenGL.GL as ogl
import OpenGL.GLU as oglu

#sys.path.append('..')
import spyre
import zoe_objects as zoeobj
import polytope as pc

# TODO for general cases. Create "System class" that will interpret controller
# and create necessary classes based on number of systems and environment (
# i.e. populate the grid and initial environments)
# TODO npt toolbox in Matlab
Ctrl = ExampleCtrl()

ScaleFactor = 1

Listing = Ctrl.Partition()
List_pos = list()
ii = 0
for x in Listing:
    List_pos.append(ScaleFactor*Listing[ii].chebXc)
    ii = ii + 1




obs_pos = 1

class CheckerUp(object):

    def Updated(self, park):
        yout = Ctrl.move(park)
        return List_pos[yout["loc"]]

    def Check(self, x, y, z,spot = numpy.array):
        eps = 0.001
        if (abs(spot[0]-x) <= eps and abs(spot[1]-y) <= eps and abs(spot[2]-z) <= eps):
            return True
        else:
            return False


Park_Signal = False
MoverSign = 0
MoverSign2 = 0
l = CheckerUp()
position_ell = numpy.array([0.0,0.0,0.0])
position_ell2 = numpy.array([0.0, 1.0, 0.0])

# TODO create 2 more classes for park locations and goals?
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
        global Park_Signal
        global ScaleFactor
        if (MoverSign == 1):
            position_ell[0] = self.x
            position_ell[1] = self.y
            position_ell[2] = self.z
            if (Park_Signal == False):
                spot = l.Updated(Park_Signal)
            elif (Park_Signal == True):
                spot = l.Updated(Park_Signal)

            #if (position_ell2[0] == 0.0 and position_ell2[1] == 1.0 and position_ell2[2] == 0.0):
            #    spot = l.Updated(0)
            #elif (position_ell2[0] == 0.0 and position_ell2[1] == 2.0 and position_ell2[2] == 1.0):
            #    spot = l.Updated(1)
            #elif (position_ell2[0] == 0.0 and position_ell2[1] == 0.0 and position_ell2[2] == 2.0):
            #    spot = l.Updated(2)

            #DISTANCE = numpy.subtract(spot, position_ell)
            position_ell[0] = spot[0]
            position_ell[1] = spot[1]
            position_ell[2] = spot[2]

            self.x = position_ell[0]
            self.y = position_ell[1]
            self.z = position_ell[2]
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

class Gridlines(spyre.Object):
    """draws a dumbbell object """
    def __init__(self, height, radius, x=0, y=0, z=0, x2=0, y2=0, z2=0,ind = 0):
        global ScaleFactor
        spyre.Object.__init__(self)
        self.height = 2*ScaleFactor*height
        self.radius = ScaleFactor*radius
        self.x      = ScaleFactor*x
        self.y      = ScaleFactor*y
        self.z      = ScaleFactor*z
        self.x2      = ScaleFactor*x2
        self.y2      = ScaleFactor*y2
        self.z2      = ScaleFactor*z2
        self.quad   = oglu.gluNewQuadric()
        self.indicator = ind


    def display(self):
        ogl.glColor4f(85.0, 91.0, 57.0, 1)
        ogl.glPushMatrix()

        if(self.indicator == 1):
            if (self.x > self.x2):
                ogl.glTranslate(self.x2, self.y, self.z)
            elif (self.x2 >= self.x):
                ogl.glTranslate(self.x, self.y, self.z)
            ogl.glRotate(90,0,1,0)
        elif(self.indicator == 2):
            if (self.y > self.y2):
                ogl.glTranslate(self.x, self.y2, self.z)
            elif (self.y2 >= self.y):
                ogl.glTranslate(self.x, self.y, self.z)
            ogl.glRotate(90,-1,0,0)
        elif(self.indicator == 3):
            if (self.z > self.z2):
                ogl.glTranslate(self.x, self.y, self.z2)
            elif (self.z2 >= self.z):
                ogl.glTranslate(self.x, self.y, self.z)
            pass


        ogl.glMaterialfv(ogl.GL_FRONT, ogl.GL_AMBIENT, [0.1745, 0.0, 0.1, 0.0])
        ogl.glMaterialfv(ogl.GL_FRONT, ogl.GL_DIFFUSE, [0.5, 0.5, 0.5, 0.1])
        ogl.glMaterialfv(ogl.GL_FRONT, ogl.GL_SPECULAR, [0.7, 0.6, 0.8, 0.0])
        ogl.glMaterialf(ogl.GL_FRONT, ogl.GL_SHININESS, 50)


        if(self.indicator == 1):
            oglu.gluCylinder(self.quad , self.radius/8.0, self.radius/8.0,abs(self.x-self.x2), 60, 70)
        elif(self.indicator == 2):
            oglu.gluCylinder(self.quad , self.radius/8.0, self.radius/8.0,abs(self.y2-self.y), 60, 70)
        elif(self.indicator == 3):
            oglu.gluCylinder(self.quad , self.radius/8.0, self.radius/8.0,abs(self.z-self.z2), 60, 70)


        ogl.glPopMatrix()



class userinput(spyre.PivotingInterface):

    def keyPressed(self, key):
        global MoverSign
        global MoverSign2
        global position_ell2
        global Park_Signal
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
        elif(key == 'p'):
            Park_Signal = True
        elif(key == 'o'):
            Park_Signal = False

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
    global ScaleFactor
    pygame.init()

    # create the engine
    engine = spyre.Engine()
    ie = userinput(engine)

    engine.studio = spyre.StudioColorMat(engine)


    # add the various objects to the engine

    engine.add(zoeobj.AxesObject())
    engine.add(zoeobj.GridObject())
    #engine.add(DumbBell(2*ScaleFactor*2,2*ScaleFactor*.25))
    #engine.add(Obstacle(2,.25))

    ii = 0
    from itertools import product

    for x in Listing:
        D = pc.extreme(Listing[ii])
        ii = ii+1
        Shp = D.shape
        Check = numpy.zeros((Shp[0],Shp[0]))
        jj = 0
        for row in D:
            ll = 0
            for row2 in D:
                if abs(row[0]-row2[0])<0.0001 and abs(row[1]-row2[1])<0.0001 and abs(row[2]-row2[2])<0.0001:
                    pass
                elif (abs(row[0]-row2[0])<0.0001 and abs(row[1]-row2[1])<0.0001):
                    if Check[jj,ll] == 0:
                        engine.add(Gridlines(2,.25,row[0],row[1],row[2],row2[0],row2[1],row2[2],3))
                    Check[jj,ll] = 1
                    Check[ll,jj] = 1
                elif (abs(row[0]- row2[0])<0.0001 and abs(row[2]-row2[2])<0.0001):
                    if Check[jj,ll] == 0:
                        engine.add(Gridlines(2,.25,row[0],row[1],row[2],row2[0],row2[1],row2[2],2))
                    Check[jj,ll] = 1
                    Check[ll,jj] = 1
                elif (abs(row[1]- row2[1])<0.0001 and abs(row[2]-row2[2])<0.0001):
                    if Check[jj,ll] == 0:
                        engine.add(Gridlines(2,.25,row[0],row[1],row[2],row2[0],row2[1],row2[2],1))
                    Check[jj,ll] = 1
                    Check[ll,jj] = 1
                ll = ll + 1
            jj = jj + 1


    # TODO setup user interface for accessing variable change on click or text
    # entering. Mainly "Move" command and the "park" command
    atexit.register(postMortem, engine)

    # run the event loop
    engine.go()

if __name__ == '__main__':
    main()
