from helpers import *

class background:
    def __init__(self,width,height):

        #157,137,108
        self.color=(157/255,137/255,108/255)
        self.width=width
        self.height=height


    def draw(self):
        ddapoints=[]

        w=self.width
        width=int((720-(w*2))/2)
        
        x=0
        y=width
        
        while(x<1280):
            x_inc=randint(50,100)
            x2=x+x_inc
            y2=randint(width-50,width+50)
            dda((x,y),(x2,y2),ddapoints)
            x,y=x2,y2
        
        ddapoints.append((1280,self.height))
        ddapoints.append((0,self.height))
    
        #for filling the triangle
        t=triangulate(ddapoints)

        glPointSize(3)
        glBegin(GL_TRIANGLES)
        glColor3fv(self.color)
        for v in t:
            glVertex3f(ROUND(v[0]), ROUND(v[1]), 0)
        glEnd()

class floor:
    def __init__(self,color,x,width):
        self.colorcode=color
        self.width=width
        self.x=x

    def draw(self):
        self.colorcode=1-self.colorcode
        self.color=(self.colorcode,self.colorcode,self.colorcode)
        vertices=[
            (self.x, 720-self.width),
            (self.x, 720),
            (self.x+self.width,720),
            (self.x+self.width,720-self.width)
        ]
        glBegin(GL_POLYGON)
        for vertex in vertices:
            glColor3fv(self.color)
            glVertex3f(vertex[0], vertex[1], 0)
        glEnd()
    

class stick:
    def __init__(self,x,width):
        self.x=x
        self.width=width
        # 2 above from floor
        self.y=720-width-2
        
    def stick_points(self,y):
        x=self.x
        width=self.width
        ddapoints=[]
        
        m=(width/64)
        #legs
        dda((x,y),(x+int(width/2),y-width),ddapoints)
        dda((x+int(width/2),y-width),(x+width,y),ddapoints)
        
        dda((x+int(width/2),y-width),(x+int(width/2),y-width-int(20*m)),ddapoints)
        
        #hands
        dda((x+int(width/2),y-width-int(20*m)),(x,y-width-int(50*m)),ddapoints)
        dda((x+int(width/2),y-width-int(20*m)),(x+width,y-width-int(50*m)),ddapoints)

        dda((x+int(width/2),y-width-int(20*m)),(x+int(width/2),y-width-int(50*m)),ddapoints)

        #face

        center=((x+int(width/2)),(y-width-int(70*m)))
        rx=int(25*m)
        ry=int(25*m)
        arc = Ellipse(center, rx, ry, med)
        arc_edge=arc.edge
        
        return ddapoints,arc_edge

    def draw(self):
        ddapoints,arc_edge=self.stick_points(self.y)
        
        
        glPointSize(5)
        glBegin(GL_POINTS)
        glColor3f(0,0,0)
        for v in ddapoints:
            glVertex3f(ROUND(v[0]), ROUND(v[1]), 0)
        glEnd()
        draw_ellipse(arc_edge)
        
        

    def jump(self):
        y2=round(self.y-(self.width*3))
        ddapoints,arc_edge=self.stick_points(y2)
        
        glPointSize(5)
        glBegin(GL_POINTS)
        glColor3f(0,0,0)
        for v in ddapoints:
            glVertex3f(ROUND(v[0]), ROUND(v[1]), 0)
        glEnd()
        draw_ellipse(arc_edge)

class boxes:
    def __init__(self,position,width):
        self.x=position
        self.width=width
        self.y=720-width

        #dark brown - 171,114,19
        self.color=(0.67,0.44,0.0745)

    def draw(self):
        self.x=self.x-20
        #base box shape
        vertices=[
            (self.x, self.y),
            (self.x, self.y-self.width),
            (self.x+self.width,self.y-self.width),
            (self.x+self.width,self.y)
        ]
        glBegin(GL_POLYGON)
        for vertex in vertices:
            glColor3fv(self.color)
            glVertex3f(vertex[0], vertex[1], 0)
        glEnd()

        #design
        self.ddapoints=[]

        #border
        dda((self.x, self.y),
        (self.x, self.y-self.width),
        self.ddapoints)

        dda((self.x, self.y-self.width),
        (self.x+self.width,self.y-self.width),
        self.ddapoints)

        dda((self.x+self.width,self.y-self.width),
        (self.x+self.width,self.y),
        self.ddapoints)

        dda((self.x+self.width,self.y),
        (self.x, self.y),
        self.ddapoints)

        #Inside design
        dda((self.x+10, self.y-10),
        (self.x+10, self.y-self.width+10),
        self.ddapoints)

        dda((self.x+10, self.y-self.width+10),
        (self.x+self.width-10,self.y-self.width+10),
        self.ddapoints)

        dda((self.x+self.width-10,self.y-self.width+10),
        (self.x+self.width-10,self.y-10),
        self.ddapoints)

        dda((self.x+self.width-10,self.y-10),
        (self.x+10, self.y-10),
        self.ddapoints)

        #diagonals
        dda((self.x+10, self.y-10),
        (self.x+self.width-10,self.y-self.width+10),
        self.ddapoints)

        dda((self.x+10, self.y-self.width+10),
        (self.x+self.width-10,self.y-10),
        self.ddapoints)

        glPointSize(3)
        glBegin(GL_POINTS)
        glColor3f(0,0,0)
        for v in self.ddapoints:
            glVertex3f(ROUND(v[0]), ROUND(v[1]), 0)
        glEnd()


        







