import numpy as np
import math
import pygame
from random import random,sample, randint, choice
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def ROUND(n):
	return int(n+0.5)


#line drawing
def dda(X,Y,arr):
    x,y=X[0],X[1]
    dx=Y[0]-X[0]
    dy=Y[1]-X[1]
    
    if (abs(dx)>(abs(dy))):
        step=abs(dx)
    else:
        step=abs(dy)

    xinc=dx/float(step)
    yinc=dy/float(step)

    arr.append((x,y))
    for v in range(step):
        x=x+xinc
        y=y+yinc
        arr.append((x,y))

'''
Ellpise drawing
'''

def regions(h, k, x, y):
    # Return the points in the 4 regions
    return [(h+x, k+y), (h+x, k-y), (h-x, k-y), (h-x, k+y)]


def med(c, rx, ry):
    # Mid point ellipse drawing algorithm
    h, k = c
    x, y = 0, ry
    r1 = rx**2
    r2 = ry**2
    # p10
    p1 = (r2 - r1 * ry + (0.25 * r1))
    points = regions(h, k, x, y)

    while r2*x < r1*y:
        if p1 < 0:
            points += regions(h, k, x + 1, y)
            p1 += 2 * r2 * (x + 1) + r2
            x += 1
        else:
            points += regions(h, k, x + 1, y - 1)
            p1 += 2 * r2 * x + r2 - 2 * r1 * y
            x += 1
            y -= 1
    # p20
    p2 = p1
    while y > 0:
        if p2 <= 0:
            points += regions(h, k, x + 1, y - 1)
            p2 += -2 * r1 * y + r1 + 2 * r2 * x
            x += 1
            y -= 1
        else:
            points += regions(h, k, x, y - 1)
            p2 += r1 - 2 * r1 * y
            y -= 1

    return points

class Ellipse():
    # Class that helps in drawing a particular shape
    def __init__(self, centre, rx, ry, edge):
        self.centre = centre
        self.rx = rx
        self.ry = ry
        self.edge = edge(self.centre, self.rx, self.ry)

    # Creating matrix of the size around the polygon drawn
    def in_mat(self):
        x, y = zip(*self.edge)
        return (min(x), max(x)), (min(y), max(y))

    # Generating fill points
    def generate_fill(self):
        fill = []
        rng = self.in_mat()
        for x in range(rng[0][0], rng[0][1]):
            for y in range(rng[1][0], rng[1][1]):
                if (x-self.centre[0])**2/self.rx**2 + (y-self.centre[1])**2/self.ry**2 < 1:
                    fill.append((x, y))
        return fill

def ellpise_points(edge):
    points=[]
    for i in edge:
        for vertex in i:
            points.append(vertex)
    return points

def draw_ellipse(edge):
    glPointSize(5)
    glBegin(GL_POLYGON)
    for i in edge:
        glColor3fv([0, 0, 0])
        glVertex2fv(i)
    glEnd()

def triangulate(polygon, holes=[]):
    """
    Returns a list of triangles.
    Uses the GLU Tesselator functions!
    """
    vertices = []
    def edgeFlagCallback(param1, param2): pass

    def beginCallback(param=None):
        vertices = []

    def vertexCallback(vertex, otherData=None):
        vertices.append(vertex[:2])

    def combineCallback(vertex, neighbors, neighborWeights, out=None):
        out = vertex
        return out

    def endCallback(data=None): pass

    tess = gluNewTess()
    gluTessProperty(tess, GLU_TESS_WINDING_RULE, GLU_TESS_WINDING_ODD)
    # forces triangulation of polygons (i.e. GL_TRIANGLES) rather than returning triangle fans or strips
    gluTessCallback(tess, GLU_TESS_EDGE_FLAG_DATA, edgeFlagCallback)
    gluTessCallback(tess, GLU_TESS_BEGIN, beginCallback)
    gluTessCallback(tess, GLU_TESS_VERTEX, vertexCallback)
    gluTessCallback(tess, GLU_TESS_COMBINE, combineCallback)
    gluTessCallback(tess, GLU_TESS_END, endCallback)
    gluTessBeginPolygon(tess, 0)

    # first handle the main polygon
    gluTessBeginContour(tess)
    for point in polygon:
        point3d = (point[0], point[1], 0)
        gluTessVertex(tess, point3d, point3d)
    gluTessEndContour(tess)

    # then handle each of the holes, if applicable
    if holes != []:
        for hole in holes:
            gluTessBeginContour(tess)
            for point in hole:
                point3d = (point[0], point[1], 0)
                gluTessVertex(tess, point3d, point3d)
            gluTessEndContour(tess)

    gluTessEndPolygon(tess)
    gluDeleteTess(tess)
    return vertices

def draw_text(x, y, text, fontsize=20, fontcolor=(0, 0, 0, 255),background=(255, 255, 0, 255)):
    font = pygame.font.SysFont('calibri', fontsize)
    textSurface = font.render(text, True, fontcolor, background)
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glWindowPos2d(x, y)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(),GL_RGBA, GL_UNSIGNED_BYTE, textData)
