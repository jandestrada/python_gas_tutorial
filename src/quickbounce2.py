from visual import * 
from random import uniform
from visual.graph import *
print """ 
Right button drag to rotate "camera" to view scene. 
Middle button to drag up or down to zoom in or out. 
""" 
no_particles=50 
maxV=400 
side = 5.0 
ballradius=0.4 
thk = 0.3 
acceleration=vector(0,-9.8,0)
molecularmass=1e20 * 1.7e-27 #kg
Pressure=0.2 #kgm-2
 
##collisions=0
##lastoutput=0
##outputs=0
ltriang=fromfunction(lambda i,j: less_equal(j,i),[no_particles,no_particles])

dt = ballradius/maxV /2.
maxpos=side-.5*thk-ballradius 
D2=(2*ballradius)**2 
s2 = 2*side + thk 
s3 = 2*side - thk


wallR = box (pos=( side, side/2, 0), length=thk, height=s2+2*side, width=s3, color = color.red) 
wallL = box (pos=(-side, side/2, 0), length=thk, height=s2+2*side, width=s3, color = color.red) 
wallB = box (pos=(0, -side, 0), length=s3, height=thk, width=s3, color = color.blue) 
wallT = box (pos=(0, side, 0), length=s3, height=thk, width=s3, color = color.blue) 
wallBK = box(pos=(0, side/2, -side), length=s3+2*thk, height=s2+2*side, width=thk, color = (0.7,0.7,0.7))

wallT.mass=Pressure/(s2**2)
wallT.velocity=0

 
balls=[]
plist=[] 
poslist=[]
hlist=[]
for i in arange(no_particles): 
    ball = sphere(color = color.green, radius=ballradius)  
    p=[maxV*uniform(-1,1),maxV*uniform(-1,1),maxV*uniform(-1,1)]
    plist.append(p) 
    position=[maxpos*uniform(-1,1),maxpos*uniform(-1,1),maxpos*uniform(-1,1)]
    poslist.append(position) 
    ball.pos=vector(position) 
    balls.append(ball) 

varray=array(plist) 
posarray=array(poslist)  


##print '''taking data
##    set   time  kinetic energy   average speed   potential energy'''
#for t in arange(0,500./maxV,dt):
while(1):
    rate(100)
    posarray=posarray+varray*dt
    wallT.y=wallT.y+wallT.velocity*dt
    maxheight=wallT.y-0.5*thk-ballradius
    maxarray=array([maxpos,maxheight,maxpos])
    varray=varray+acceleration*dt
    wallT.velocity=0.999*wallT.velocity+acceleration[1]*dt

    hit=greater(posarray[:,1],maxheight)
    hitlist=sort(nonzero(hit))[0]
    for i in hitlist:
        wallT.velocity=wallT.velocity+2*varray[i,1]*molecularmass/wallT.mass
 

    putmask(varray,greater(posarray,maxarray),-varray) 
    putmask(posarray,greater(posarray,maxarray),2*maxarray-posarray) 
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

##        collisions=collisions+1

    for i in arange(len(balls)): 
        balls[i].pos=posarray[i]
        
##    if collisions > lastoutput + no_particles:
##      lastoutput = collisions
##      outputs=outputs+1
###      Kenergy=add.reduce(add.reduce(pvarray*varray,-1))/no_particles/2
###      avspeed=add.reduce(sqrt(add.reduce(varray*varray,-1)))/no_particles
###      Penergy=add.reduce(posarray[:,1])
##      print outputs,t,Kenergy,avspeed,Penergy
##      for ball in balls:
##        hlist.append(ball.y)
###graph=gdisplay(xtitle='height',ytitle='density')
###heightdist=ghistogram(bins=arange(0,2*side,1/side),color=color.green)
###heightdist.plot(data=hlist)
