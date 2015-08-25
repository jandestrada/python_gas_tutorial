from visual import * 
print """ 
Right button drag to rotate "camera" to view scene.
Middle button to drag up or down to zoom in or out.
"""

# parameters describing the size of the walls
#set the maximum x, y or z that the centre of the ball can have
#before bouncing off the wall (for a cubic box)
side=4.0
ballradius=0.4
thk=0.3
s2 = 2*side - thk 
s3 = 2*side + thk
maxpos=side-thk/2-ballradius 
maxv=2.0

#create a ball and set its velocity
ball = sphere (color = color.green, radius = ballradius) 
ball.velocity = vector (-1.5, -2.3, +2.7)

#create 5 joining walls
wallR = box (pos=vector( side, 0, 0), size=vector(thk, s2, s3), color = color.red) 
wallL = box (pos=vector(-side, 0, 0), size=vector(thk,s2, s3), color = color.red) 
wallB = box (pos=vector(0, -side, 0), size=vector(s3,thk,s3), color = color.blue) 
wallT = box (pos=vector(0, side, 0), size=vector(s3,thk,s3), color = color.blue) 
wallBK = box(pos=vector(0, 0, -side), size=vector(s2,s2, thk), color = (0.7,0.7,0.7)) 

#set the timestep between motion
timestep = 0.05

while (1==1):
    rate(100)
    #code within this while loop is repeated up to 100 times per second
    #until the program is stopped
    
    ball.pos = ball.pos + ball.velocity*timestep #moves ball

    #check for collisions with the walls
    #right wall
    if ball.pos.x > maxpos: 
        ball.velocity.x = -ball.velocity.x #reflect velocity
        ball.pos.x=2*maxpos-ball.pos.x #reflect position
    #left wall
    if ball.pos.x < -maxpos: 
        ball.velocity.x = -ball.velocity.x 
        ball.pos.x=-2*maxpos-ball.pos.x
    # roof
    if ball.pos.y > maxpos: 
        ball.velocity.y = -ball.velocity.y 
        ball.pos.y=2*maxpos-ball.pos.y
    #floor
    if ball.pos.y < -maxpos: 
        ball.velocity.y = -ball.velocity.y 
        ball.pos.y=-2*maxpos-ball.pos.y
    #back wall
    if ball.pos.z > maxpos: 
        ball.velocity.z = -ball.velocity.z 
        ball.pos.z=2*maxpos-ball.pos.z
    #front wall
    if ball.pos.z < -maxpos: 
        ball.velocity.z = -ball.velocity.z 
        ball.pos.z=-2*maxpos-ball.pos.z 
