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

    # Parse the command line arguments required to animate the Ising model.
    lattice_dimensions = int(sys.argv[1])
    temperature = float(sys.argv[2])
    dynamics_type = sys.argv[3]

    # Instantiate an object of the SpinLattice class to represent the Ising
    # model.
    ising_model = SpinLattice(lattice_dimensions, temperature)

    # Initialise the spin lattice to represent the Ising model.
    ising_model.initialise_spin_lattice()

    # Initialise the plot for the animation.
    fig = plt.figure()
    im=plt.imshow(ising_model.get_spin_lattice(), animated=True)

    # Get the number of steps over which the simulation will run.
    nsteps = ising_model.get_nsteps()

    # Run the animation for Glauber or Kawasaki dynamics depending on the
    # dynamics_type command line argument.
    if dynamics_type == "Glauber":
        for step in range(nsteps):
            for i in range(lattice_dimensions):
                for j in range(lattice_dimensions):
                    ising_model.select_new_state_glauber()
                    delta_E = ising_model.calculate_energy_difference_glauber()
                    ising_model.metropolis_algorithm_glauber(delta_E)

            # Write the spin data of Glauber dynamics to the spins_glauber.dat
            # file every ten steps.
            if(step % 10 == 0):
                print(step, delta_E)
        #       dump output
                spin_lattice = ising_model.get_spin_lattice()
                f = open('../data_files/spins_glauber.dat','w')
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
        for step in range(nsteps):
            for i in range(lattice_dimensions):
                for j in range(lattice_dimensions):
                    ising_model.select_new_state_kawasaki()
                    delta_E = ising_model.calculate_energy_difference_kawasaki()
                    ising_model.metropolis_algorithm_kawasaki(delta_E)

            # Write the spin data of Kawasaki dynamics to the spins_glauber.dat
            # file every ten steps.
            if(step % 10 == 0):
                print(step, delta_E)
        #       dump output
                spin_lattice = ising_model.get_spin_lattice()
                f = open('../data_files/spins_kawasaki.dat','w')
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