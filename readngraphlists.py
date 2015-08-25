from visual import *
from visual.graph import *

##ivoutfile='ivdist_uv1n50s5.data'
voutfile='ivoutlist.data'

vlist=[]
file_end=0
inputs=0
voutput=open(voutfile)
while not file_end:
    try:
        input=pickle.load(voutput)
    except EOFError:
        file_end=1
        voutput.close
        print 'read', inputs, 'inputs'
    else:
        for velocity in input:
            vlist.append(velocity)
        inputs=inputs+1

print 'effective number of particles', len(vlist)

tot_energy=0
avx_energy=0
ke_list=[]
kex_list=[]
speed_list=[]
vx_list=[]
for v in vlist:
    vx_list.append(abs(v[0]))
    k_energy=(v[0]**2+v[1]**2+v[2]**2)/2.
    ke_list.append(k_energy)
    speed_list.append(sqrt(k_energy*2.))
    x_energy=v[0]**2/2.
    kex_list.append(x_energy)
    tot_energy=tot_energy+k_energy
    avx_energy=avx_energy+ x_energy

av_energy=tot_energy/len(vlist)
avx_energy=avx_energy/len(vlist)
Vchar=sqrt(2*av_energy)
Vxchar=sqrt(2*avx_energy)
print 'average kinetic energy =',av_energy
print 'average kinetic energy in x direction =',avx_energy

graph2=gdisplay(xtitle='v',ytitle='final velocity distribution')
velocity_dist=ghistogram(bins=arange(0,4*Vxchar,4*Vxchar/len(vlist)*10))
velocity_dist.plot(data=vx_list)

E_vx_dist=gcurve(color=color.green)
for v in arange(0,4*Vxchar,4*Vxchar/40):
    E_vx_dist.plot(pos=( v , 30*exp(-v**2/(av_energy*4./3.)) ))

graph3=gdisplay(xtitle='v',ytitle='number of particles',title='final speed distribution')
speed_dist=ghistogram(bins=arange(0,4*Vchar,4*Vchar/len(vlist)*10))
speed_dist.plot(data=speed_list)

E_speed_dist=gcurve(color=color.green)
for v in arange(0,3*Vchar,3*Vchar/40):
    E_speed_dist.plot(pos=(v,50*v**2/sqrt(av_energy**3)*exp(-v**2/(av_energy*4./3.))))


graph4=gdisplay(xtitle='energy',ytitle='number of particles',title='energy distribution in x')
kex_dist=ghistogram(bins=arange(0,5*avx_energy,5*avx_energy/len(vlist)*10))
kex_dist.plot(data=kex_list)

E_kex_dist=gcurve(color=color.green)
for u in arange(avx_energy/40.,5*avx_energy,5*avx_energy/40.):
    E_kex_dist.plot(pos=(u,10/sqrt(u)*exp(-u/(2*avx_energy))))

graph5=gdisplay(xtitle='energy',ytitle='number of particles',title='final energy distribution')
KE_dist=ghistogram(bins=arange(0,5*av_energy,5*av_energy/len(vlist)*10))
KE_dist.plot(data=ke_list)

E_KE_dist=gcurve(color=color.green)
for u in arange(0,5*av_energy,5*av_energy/40.):
    E_KE_dist.plot(pos=(u,150*sqrt(u)*exp(-u/(av_energy*2./3.))))
