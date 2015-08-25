from visual import * 
from random import uniform 
print """ 
Right button drag to rotate "camera" to view scene. 
Middle button to drag up or down to zoom in or out. 
 """ 
 
# parameters describing the size of the walls
thk = 0.3 
side = 4.0  
s2 = 2*side - thk 
s3 = 2*side + thk
#create 5 joining walls
wallR = box (pos=( side, 0, 0), length=thk, height=s2, width=s3, color = color.red) 
wallL = box (pos=(-side, 0, 0), length=thk, height=s2, width=s3, color = color.red) 
wallB = box (pos=(0, -side, 0), length=s3, height=thk, width=s3, color = color.blue) 
wallT = box (pos=(0, side, 0), length=s3, height=thk, width=s3, color = color.blue) 
wallBK = box(pos=(0, 0, -side), length=s2, height=s2, width=thk, color = (0.7,0.7,0.7)) 

#create set of particles with random position and velocity
no_particles=10
ballradius=0.4
maxpos=side-.5*thk-ballradius
maxv=1.0
balls=[] 
for i in arange(no_particles): 
    ball=sphere(color=color.green,radius=ballradius) 
    ball.pos=maxpos*vector(uniform(-1,1),uniform(-1,1),uniform(-1,1)) 
    ball.velocity=maxv*vector(uniform(-1,1),uniform(-1,1),uniform(-1,1)) 
    balls.append(ball)

#set timestep so that collisions won't be missed
timestep = ballradius/maxv*0.5
while (1==1): 
    rate(1/timestep)#keeps the simulation going in 'real' time
    
    for ball in balls: #repeats over list of particles
        ball.pos = ball.pos + ball.velocity*timestep #move ball
        if ball.x > maxpos: #check right wall collisions
            ball.velocity.x = -ball.velocity.x #reflect velocity
            ball.x=2*maxpos-ball.x #reflect position
        if ball.x < -maxpos: #left wall
            ball.velocity.x = -ball.velocity.x 
            ball.x=-2*maxpos-ball.x 
        if ball.y > maxpos: # roof
            ball.velocity.y = -ball.velocity.y 
            ball.y=2*maxpos-ball.y 
        if ball.y < -maxpos: #floor
            ball.velocity.y = -ball.velocity.y 
            ball.y=-2*maxpos-ball.y 
        if ball.z > maxpos: #back wall
            ball.velocity.z = -ball.velocity.z 
            ball.z=2*maxpos-ball.z 
        if ball.z < -maxpos: #front wall
            ball.velocity.z = -ball.velocity.z 
            ball.z=-2*maxpos-ball.z
            
    for i in range(no_particles): 
        for j in range(i+1,no_particles): #loop through all particle pairs
            distance=mag(balls[i].pos-balls[j].pos) 
            if distance<(balls[i].radius+balls[j].radius): #check collision
                direction=norm(balls[i].pos-balls[j].pos) #unit vector in collision direction
                vi=dot(balls[i].velocity,direction) 
                vj=dot(balls[j].velocity,direction) 
                exchange=vj-vi #impact velocity
                balls[i].velocity=balls[i].velocity+exchange*direction #exchange momentum
                balls[j].velocity=balls[j].velocity-exchange*direction 
                overlap=2*ballradius-distance 
                balls[i].pos=balls[i].pos +overlap*direction #adjust position 
                balls[j].pos=balls[j].pos-overlap*direction 
