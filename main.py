from classes import *

if __name__ == "__main__":
    pygame.init()
    display = (1280, 720)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    #background color
    #245,178,81
    glClearColor(245/255,178/255,81/255,0)
    gluOrtho2D(0, display[0], display[1], 0)
    
    width=64
    path=[]
    for i in range(int(display[0]/width)+1):
        if i%2==0:
            path.append(floor(0,i*width,width))
        else:
            path.append(floor(1,i*width,width))
    
    boxes_path=[]
    position_q=[1000]
    x=1000

    for i in range(20):
        x=x+choice([200,300])
        position_q.append(x)

    for i in position_q:
        boxes_path.append(boxes(i,width))

    counter = 0
    end=False
    score=0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        if not end:
            b1 = background(width, display[1])
            b1.draw()

            for i in path:
                i.draw()

            stick1 = stick(100, width)

            
            jump = False
            x = 1200
            x_coord = []
            for i in boxes_path:
                x_coord.append(i.x)
            for i in boxes_path:
                if i.x < -width/2:
                    # update i.x
                    x = max(x_coord)+choice([200, 300])
                    i.x = x
                    score+=1
                i.draw()

            keys = pygame.key.get_pressed()  # checking pressed keys
            if keys[pygame.K_SPACE] and counter < 20:
                stick1.jump()
                counter += 1
            else:
                stick1.draw()
                for i in x_coord:
                    if i-width<=stick1.x<=i+width:
                        end=True
                counter = 0

            draw_text(430,620,"STICK RUN GAME",64,(255,0,0,255),(245,178,81,255))
            draw_text(10,670,f" SCORE = {score} ",32,(0,0,0,255),(245,178,81,255))
        else:
            glClearColor(0,0,0,1)
            draw_text(100,400," GAME OVER ",200,(255,0,0,255),(0,0,0,255))
            draw_text(350,200,f" SCORE = {score} ",120,(251,199,55,2550),(0,0,0,255))
            draw_text(270,100," NIKUNJ MAHESHWARI | CED18I038 ",48,(255,255,255,255),(0,0,0,255))
            
                
        pygame.display.flip()
        pygame.time.wait(100)
