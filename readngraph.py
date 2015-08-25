from visual import *
from visual.graph import *
import pickle

##ivoutfile='ivdist_uv1n50s5.data'
fvoutfile='fvdist_uv1n50s5.data'

fvlistx=[]
fvlisty=[]
fvlistz=[]
    
file_end=0
inputs=0
fvoutput=open(fvoutfile)
while not file_end:
    try:
        input=pickle.load(fvoutput)
    except EOFError:
        file_end=1
        fvoutput.close
        print 'read', inputs, 'inputs'
    else:
        fvlistx[-1:]=list(abs(input[:,0]))
        fvlisty[-1:]=list(abs(input[:,1]))
        fvlistz[-1:]=list(abs(input[:,2]))
        inputs=inputs+1



tot_energy=0
avx_energy=0
ke_list=[]
kex_list=[]
speed_list=[]
for i in range(len(fvlistx)):
    k_energy=(fvlistx[i]**2+fvlisty[i]**2+fvlistz[i]**2)/2.
    ke_list.append(k_energy)
    speed_list.append(sqrt(2*k_energy))
    x_energy=fvlistx[i]**2/2.
    kex_list.append(x_energy)
    tot_energy=tot_energy+k_energy
    avx_energy=avx_energy+ x_energy

av_energy=tot_energy/len(fvlistx)
avx_energy=avx_energy/len(fvlistx)
Vchar=sqrt(2*av_energy)
Vxchar=sqrt(2*avx_energy)
print 'average kinetic energy =',av_energy
print 'average kinetic energy in x direction =',avx_energy

graph2=gdisplay(xtitle='v',ytitle='final velocity distribution')
velocity_dist=ghistogram(bins=arange(0,4*Vxchar,4*Vxchar/len(fvlistx)*100))
velocity_dist.plot(data=fvlistx)

E_vx_distribution=gcurve(color=color.green)
for v in arange(0,4*Vxchar,4*Vxchar/40):
    E_vx_distribution.plot(pos=( v , 300*exp(-v**2/(av_energy*4./3.)) ))

graph3=gdisplay(xtitle='v',ytitle='number of particles',title='final speed distribution')
speed_dist=ghistogram(bins=arange(0,4*Vchar,4*Vchar/len(fvlistx)*100))
speed_dist.plot(data=speed_list)

E_speed_distribution=gcurve(color=color.green)
for v in arange(0,3*Vchar,3*Vchar/40):
    E_speed_distribution.plot(pos=(v,600*v**2/sqrt(av_energy**3)*exp(-v**2/(av_energy*4./3.))))

graph4=gdisplay(xtitle='energy',ytitle='number of particles',title='energy distribution in x')
kex_dist=ghistogram(bins=arange(0,8*avx_energy,8*avx_energy/len(fvlistx)*100))
kex_dist.plot(data=kex_list)

E_kex_dist=gcurve(color=color.green)
for u in arange(avx_energy/40.,8*avx_energy,8*avx_energy/40.):
    E_kex_dist.plot(pos=(u,140./sqrt(u)*exp(-u/(2*avx_energy))))

graph5=gdisplay(xtitle='energy',ytitle='number of particles',title='final energy distribution')
KE_dist=ghistogram(bins=arange(0,5*av_energy,5*av_energy/len(fvlistx)*100))
KE_dist.plot(data=ke_list)

E_KE_dist=gcurve(color=color.green)
for u in arange(0,5*av_energy,5*av_energy/40.):
    E_KE_dist.plot(pos=(u,1500*sqrt(u)*exp(-u/(av_energy*2./3.))))
