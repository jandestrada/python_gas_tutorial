from visual import * 
from random import random 
print """ 
Right button drag to rotate "camera" to view scene. 
Middle button to drag up or down to zoom in or out. 
""" 
no_particles=30 
maxV=1.0 
side = 5.0 
ballradius=0.4 
thk = 0.3 

 
collisions=0
ltriang=fromfunction(lambda i,j: less_equal(j,i),[no_particles,no_particles])

dt = ballradius/maxV 
maxpos=side-.5*thk-ballradius 
D2=(2*ballradius)**2 
s2 = 2*side - thk 
s3 = 2*side + thk 

wallR = box (pos=( side, 0, 0), length=thk, height=s2, width=s3, color = color.red) 
wallL = box (pos=(-side, 0, 0), length=thk, height=s2, width=s3, color = color.red) 
wallB = box (pos=(0, -side, 0), length=s3, height=thk, width=s3, color = color.blue) 
wallT = box (pos=(0, side, 0), length=s3, height=thk, width=s3, color = color.blue) 
wallBK = box(pos=(0, 0, -side), length=s2, height=s2, width=thk, color = (0.7,0.7,0.7)) 

 
balls=[]
plist=[] 
poslist=[] 
for i in arange(no_particles): 
    ball = sphere(color = color.green, radius=ballradius)  
    p=[2*maxV*(random()-.5), 2*maxV*(random()-.5),2*maxV*(random()-.5)]
    plist.append(p) 
    position=[2*maxpos*(random()-0.5), 2*maxpos*(random()-0.5),2*maxpos*(random()-0.5)]
    poslist.append(position) 
    ball.pos=vector(position) 
    balls.append(ball) 

parray=array(plist) 
posarray=array(poslist)  


while 1: 
    rate(50) 
    posarray=posarray+parray*dt 

    putmask(parray,greater(posarray,maxpos),-parray) 
    putmask(posarray,greater(posarray,maxpos),2*maxpos-posarray) 
    putmask(parray,less_equal(posarray,-maxpos),-parray) 
    putmask(posarray,less_equal(posarray,-maxpos),-2*maxpos-posarray) 

    separation=posarray-posarray[:,None]
    sepmag2=add.reduce(separation*separation,-1)
    
    putmask(sepmag2,ltriang,4*D2) 
    hit=less_equal(sepmag2,D2) 
    hitlist=sort(nonzero(hit.flat))[0]

    for ij in hitlist:
        i, j = divmod(ij,no_particles) 
        sepmag=sqrt(sepmag2[i,j])

        direction=separation[i,j]/sepmag 
        pi=dot(parray[i],direction) 
        pj=dot(parray[j],direction) 
        exchange=pj-pi 
        parray[i]=parray[i]+exchange*direction 
        parray[j]=parray[j]-exchange*direction 

        overlap=2*ballradius-sepmag 
        posarray[i]=posarray[i]-overlap*direction 
        posarray[j]=posarray[j]+overlap*direction

    for i in arange(len(balls)): 
        balls[i].pos=posarray[i] 
