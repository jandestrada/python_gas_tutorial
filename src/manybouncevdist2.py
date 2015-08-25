from visual import * 
from random import random
from visual.graph import *
print """ 
Right button drag to rotate "camera" to view scene. 
Middle button to drag up or down to zoom in or out. 
 """ 
no_particles=10 
maxV=1.0 
thk = 0.3 
side = 3.0 
ballradius=0.4
ivoutfile='ivoutlist.data'
voutfile='fvoutlist.data'

dt = ballradius/maxV 
maxpos=side-.5*thk-ballradius 
s2 = 2*side - thk 
s3 = 2*side + thk 

wallR = box (pos=( side, 0, 0), length=thk, height=s2, width=s3, color = color.red) 
wallL = box (pos=(-side, 0, 0), length=thk, height=s2, width=s3, color = color.red) 
wallB = box (pos=(0, -side, 0), length=s3, height=thk, width=s3, color = color.blue) 
wallT = box (pos=(0, side, 0), length=s3, height=thk, width=s3, color = color.blue) 
wallBK = box(pos=(0, 0, -side), length=s2, height=s2, width=thk, color = (0.7,0.7,0.7)) 

balls=[] 
for i in arange(no_particles): 
    ball = sphere(color = color.green, radius=ballradius) 
    ball.velocity = vector (2*maxV*(random()-.5),2*maxV*(random()-.5) ,2*maxV*(random()-.5))
    ball.pos = vector (2*maxpos*(random()-0.5), 2*maxpos*(random()-0.5), 2*maxpos*(random()-0.5)) 
    balls.append(ball) 
  
ivoutput=open(ivoutfile,'a')
vlist=[]
for ball in balls:
        vlist.append(tuple(ball.velocity))
pickle.dump(vlist,ivoutput)
ivoutput.close
print vlist

##ivoutput=open(ivoutfile,'r')
##file_end=0
##inputs=0
##while not file_end:
##    try: nlist=pickle.load(ivoutput)
##    except(KeyError,EOFError):
##        file_end=1
##        print 'read', inputs, 'inputs'
##    else: inputs = inputs+1
##
##print nlist

output_interval=no_particles*10
next_output=output_interval
collisions=0

while (1==1): 
    rate(10) 

    for ball in balls: 
        ball.pos = ball.pos + ball.velocity*dt 

        if ball.x > maxpos: 
            ball.velocity.x = -ball.velocity.x 
            ball.x=2*maxpos-ball.x 
        if ball.x < -maxpos: 
            ball.velocity.x = -ball.velocity.x 
            ball.x=-2*maxpos-ball.x 
        if ball.y > maxpos: 
            ball.velocity.y = -ball.velocity.y 
            ball.y=2*maxpos-ball.y 
        if ball.y < -maxpos: 
            ball.velocity.y = -ball.velocity.y 
            ball.y=-2*maxpos-ball.y 
        if ball.z > maxpos: 
            ball.velocity.z = -ball.velocity.z 
            ball.z=2*maxpos-ball.z 
        if ball.z < -maxpos: 
            ball.velocity.z = -ball.velocity.z 
            ball.z=-2*maxpos-ball.z 

    for i in arange(len(balls)): 
        for j in arange(i+1,len(balls)): 
            distance=mag(balls[i].pos-balls[j].pos) 
            if distance<(balls[i].radius+balls[j].radius): 
                direction=norm(balls[i].pos-balls[j].pos) 
                vi=dot(balls[i].velocity,direction) 
                vj=dot(balls[j].velocity,direction) 
                exchange=vi-vj 
                balls[i].velocity=balls[i].velocity-exchange*direction 
                balls[j].velocity=balls[j].velocity+exchange*direction
                
                overlap=2*ballradius-distance 
                balls[i].pos=balls[i].pos +overlap*direction 
                balls[j].pos=balls[j].pos -overlap*direction

                collisions=collisions+1
    if collisions>next_output:       
        next_output=next_output+output_interval
        vlist=[]
        for ball in balls:
            vlist.append(tuple(ball.velocity))
        voutput=open(voutfile,'a')
        pickle.dump(vlist,voutput)
        voutput.close
        print 'collisions =',collisions,'ouput velocity to', voutfile


