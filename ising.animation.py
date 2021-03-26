from spin_lattice import SpinLattice
import matplotlib
matplotlib.use('TKAgg')

import sys
import math
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def main():
    if len(sys.argv) != 4:
        print("Usage python3 ising.animation.py N T Glauber/Kawasaki")
        sys.exit()

    lattice_dimensions = int(sys.argv[1])
    temperature = float(sys.argv[2])
    dynamics_type = sys.argv[3]
    ising_model = SpinLattice(lattice_dimensions, temperature, dynamics_type)

    ising_model.initialise_spin_lattice()
    fig = plt.figure()
    im=plt.imshow(ising_model.get_spin_lattice(), animated=True)

    nstep = ising_model.get_nsteps()

    if dynamics_type == "Glauber":
        for step in range(nstep):
            for i in range(lattice_dimensions):
                for j in range(lattice_dimensions):
                    ising_model.select_new_state_glauber()
                    delta_E = ising_model.calculate_energy_difference_glauber()
                    ising_model.metropolis_algorithm_glauber(delta_E)

            if(nstep % 10 == 0):
                print(step, delta_E)
        #       dump output
                spin_lattice = ising_model.get_spin_lattice()
                f = open('spins.dat','w')
                for i in range(lattice_dimensions):
                    for j in range(lattice_dimensions):
                        f.write('%d %d %d\n' % (i, j, spin_lattice[i, j]))
                f.close()
        #       show animation
                plt.cla()
                im = plt.imshow(spin_lattice, animated=True)
                plt.draw()
                plt.pause(0.0001)
                
    elif dynamics_type == "Kawasaki":
        for step in range(nstep):
            for i in range(lattice_dimensions):
                for j in range(lattice_dimensions):
                    ising_model.select_new_state_kawasaki()
                    delta_E = ising_model.calculate_energy_difference_kawasaki()
                    ising_model.metropolis_algorithm_kawasaki(delta_E)

            if(nstep % 10 == 0):
                print(step, delta_E)
        #       dump output
                spin_lattice = ising_model.get_spin_lattice()
                f = open('spins.dat','w')
                for i in range(lattice_dimensions):
                    for j in range(lattice_dimensions):
                        f.write('%d %d %d\n' % (i, j, spin_lattice[i, j]))
                f.close()
        #       show animation
                plt.cla()
                im = plt.imshow(spin_lattice, animated=True)
                plt.draw()
                plt.pause(0.0001)
        

main()