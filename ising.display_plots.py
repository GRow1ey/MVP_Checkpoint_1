from spin_lattice import SpinLattice
import matplotlib
matplotlib.use('TKAgg')

import sys
import math
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# plot glauber energy
def glauben():
    datafile = np.loadtxt("glauberdata1.txt")
    temperatures = datafile[0]
    yax = datafile[3]
    plt.title('Average Energy against Temperature using Glauber Dynamics')
    plt.xlabel('Temperature, T')
    plt.ylabel('Average Energy, <E>')
    plt.plot(temperatures,yax)
    plt.show()
    main()

# plot glauber absolute magnetism
def glaubmag():
    datafile = np.loadtxt("glauberdata1.txt")
    temperatures = datafile[0]
    yax = datafile[1]
    plt.title('Average Absolute Magnetisation against Temperature using Glauber Dynamics')
    plt.xlabel('Temperature, T')
    plt.ylabel('Average Absolute Magnetisation, <|M|>')
    plt.plot(temperatures,yax)
    plt.show()
    main()

#plot glauber specific heat
def glaubsh():
    datafile = np.loadtxt("glauberdata1.txt")
    temperatures = datafile[0]
    yax = datafile[4]
    bootstraperror = datafile[5]
    plt.title('Specific Heat Capacity against Temperature using Glauber Dynamics')
    plt.xlabel('Temperature, T')
    plt.ylabel('Specific Heat Capacity, C')
    plt.plot(temperatures,yax)
    plt.errorbar(temperatures, yax, yerr=bootstraperror)
    plt.show() 
    main()


# plot glauber susceptibility
def glaubsus():
    datafile = np.loadtxt("glauberdata1.txt")
    temperatures = datafile[0]
    yax = datafile[2]
    plt.title('Susceptibility against Temperature using Glauber Dynamics')
    plt.xlabel('Temperature, T')
    plt.ylabel('Susceptibility, χ')
    plt.plot(temperatures,yax)
    plt.show()
    main()

# plot kawasaki energy
def kawaen():
    datafile = np.loadtxt("kawadata.txt")
    temperatures = datafile[0]
    yax = datafile[1]
    plt.title('Average Energy against Temperature using Kawasaki Dynamics')
    plt.xlabel('Temperature, T')
    plt.ylabel('Average Energy, <E>')
    plt.plot(temperatures,yax)
    plt.show()
    main()

# plot kawasaki specific heat
def kawash():
    datafile = np.loadtxt("kawadata.txt")
    temperatures = datafile[0]
    yax = datafile[2]
    bootstraperror = datafile[3]
    plt.title('Specific Heat Capacity against Temperature using Kawasaki Dynamics')
    plt.xlabel('Temperature, T')
    plt.ylabel('Specific Heat Capacity, C')
    plt.plot(temperatures,yax)
    plt.errorbar(temperatures, yax, yerr=bootstraperror)
    plt.show()
    main()

def main():
