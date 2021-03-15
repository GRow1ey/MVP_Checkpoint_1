import matplotlib
matplotlib.use('TKAgg')

import sys
import math
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

J=1.0
nstep=10000

#input

if(len(sys.argv) != 3):
    print("Usage python ising.animation.py N T")
    sys.exit()

lx=int(sys.argv[1]) 
ly=lx 
kT=float(sys.argv[2]) 

spin=np.zeros((lx,ly),dtype=float)

#initialise spins randomly

for i in range(lx):
    for j in range(ly):
        r=random.random()
        if(r<0.5): spin[i,j]=-1
        if(r>=0.5): spin[i,j]=1

fig = plt.figure()
im=plt.imshow(spin, animated=True)

#update loop here - for Glauber dynamics

for n in range(nstep):
    for i in range(lx):
        for j in range(ly):

#select spin randomly
            itrial=np.random.randint(0,lx)
            jtrial=np.random.randint(0,ly)
            spin_new=-spin[itrial,jtrial]

#compute delta E eg via function (account for periodic BC)

#perform metropolis test
            r = random.random()
            if r <= np.exp(-deltae/kT):
                spin[itrial, jtrial] = spin_new

#occasionally plot or update measurements, eg every 10 sweeps
    if(n%10==0): 
        energy = 0.0
        for i in range(lx):
            for j in range(ly):
                iup = i + 1
                if i == (lx - 1) :
                    iup = 0
                if j == (ly - 1):
                    jup = 0
                energy += -j * spin[i, j] * (spin[iup, j] + spin[i, jup])
        print(n, energy)

#       dump output
        f = open('spins.dat','w')
        for i in range(lx):
            for j in range(ly):
                f.write('%d %d %d\n' % (i, j, spin[i, j]))
        f.close()
#       show animation
        plt.cla()
        im = plt.imshow(spin, animated=True)
        plt.draw()
        plt.pause(0.0001)