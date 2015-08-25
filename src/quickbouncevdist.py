from visual import * 
from random import uniform
from visual.graph import *
print """ 
Right button drag to rotate "camera" to view scene. 
Middle button to drag up or down to zoom in or out. 
""" 
no_particles=20 
maxV=1.0 
side = 5.0 
ballradius=0.4 
thk = 0.3 
 
collisions=0
lastoutput=0
outputs=0
ltriang=fromfunction(lambda i,j: less_equal(j,i),[no_particles,no_particles])

dt = ballradius/maxV /2.
maxpos=side-.5*thk-ballradius 
D2=(2*ballradius)**2 
s2 = 2*side + thk 
s3 = 2*side - thk


wallR = box (pos=( side, 0, 0), length=thk, height=s2, width=s3, color = color.red) 
wallL = box (pos=(-side, 0, 0), length=thk, height=s2, width=s3, color = color.red) 
wallB = box (pos=(0, -side, 0), length=s3, height=thk, width=s3, color = color.blue) 
wallT = box (pos=(0, side, 0), length=s3, height=thk, width=s3, color = color.blue) 
wallBK = box(pos=(0, 0, -side), length=s3+2*thk, height=s2, width=thk, color = (0.7,0.7,0.7))


wallT.velocity=0

 
balls=[]
vlist=[] 
poslist=[]
hlist=[]
for i in arange(no_particles): 
    ball = sphere(color = color.green, radius=ballradius)  
    v=[maxV*uniform(-1,1),maxV*uniform(-1,1),maxV*uniform(-1,1)]
    vlist.append(v) 
    position=[maxpos*uniform(-1,1),maxpos*uniform(-1,1),maxpos*uniform(-1,1)]
    poslist.append(position) 
    ball.pos=vector(position) 
    balls.append(ball) 

varray=array(vlist) 
posarray=array(poslist)  

graphwindow=gdisplay(xtitle='v_x',ytitle='N',ymax=no_particles/4)
velocity_dist=ghistogram(bins=arange(0,2*maxV,maxV/10.),accumulate=1,average=1)
expected_distribution=gcurve(color=color.green)
for v in arange(0,2*maxV,maxV/20):
    expected_distribution.plot(pos=(v,.15*no_particles*exp(-v**2/maxV**2*3/2)))

while(1):
    rate(1000)
    posarray=posarray+varray*dt
 
    putmask(varray,greater(posarray,maxpos),-varray) 
    putmask(posarray,greater(posarray,maxpos),2*maxpos-posarray) 
    putmask(varray,less_equal(posarray,-maxpos),-varray) 
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
        pi=dot(varray[i],direction) 
        pj=dot(varray[j],direction) 
        exchange=pj-pi 
        varray[i]=varray[i]+exchange*direction 
        varray[j]=varray[j]-exchange*direction 

        overlap=2*ballradius-sepmag 
        posarray[i]=posarray[i]-overlap*direction 
        posarray[j]=posarray[j]+overlap*direction

        collisions=collisions+1

    for i in arange(len(balls)): 
        balls[i].pos=posarray[i]
        
    velocity_dist.plot(data=abs(varray[:,2]))
        




