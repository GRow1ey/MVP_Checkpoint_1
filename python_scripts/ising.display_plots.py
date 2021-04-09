from spin_lattice import SpinLattice
import matplotlib
matplotlib.use('TKAgg')

import sys
import math
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
matplotlib.rcParams['text.usetex'] = True

def display_mean_energy_plot_glauber():
    """Plot the average energy against temperature for Glauber Dynamics."""
    datafile = np.loadtxt("ising_model_glauber_data.txt")
    temperatures = datafile[0]
    mean_energies = datafile[3]
    plt.title('Mean Energy against Temperature for Glauber Dynamics')
    plt.xlabel('Temperature, T')
    plt.ylabel('Mean Energy, $\displaystyle\langle E \\rangle$')
    plt.plot(temperatures, mean_energies)
    plt.show()
    main()

def display_mean_absolute_magnetism_plot_glauber():
    """
    Plot the mean absolute magnetisation against 
    temperature for Glauber Dynamics.
    """
    datafile = np.loadtxt("ising_model_glauber_data.txt")
    temperatures = datafile[0]
    mean_absolute_magnetisms = datafile[1]
    plt.title('Mean Absolute Magnetisation against Temperature for\
         Glauber Dynamics')
    plt.xlabel('Temperature, T')
    plt.ylabel('Mean Absolute Magnetisation, $\displaystyle\langle |M| \\rangle$')
    plt.plot(temperatures, mean_absolute_magnetisms)
    plt.show()
    main()

def display_scaled_specific_heat_plot_glauber():
    """
    Plot the scaled specific heat against 
    temperature for Glauber.
    """
    datafile = np.loadtxt("ising_model_glauber_data.txt")
    temperatures = datafile[0]
    scaled_specific_heat_capacities = datafile[4]
    bootstrap_errors = datafile[5]
    plt.title('Scaled Specific Heat Capacity against Temperature using \
        Glauber Dynamics')
    plt.xlabel('Temperature, T')
    plt.ylabel('Scaled Specific Heat Capacity, C')
    plt.plot(temperatures, scaled_specific_heat_capacities)
    plt.errorbar(temperatures, scaled_specific_heat_capacities, yerr=bootstrap_errors)
    plt.show() 
    main()

def display_susceptibility_plot_glauber():
    """
    Plot the susceptibility against temperature 
    for Glauber Dynamics.
    """
    datafile = np.loadtxt("ising_model_glauber_data.txt")
    temperatures = datafile[0]
    susceptibilities = datafile[2]
    plt.title('Susceptibility against Temperature using Glauber Dynamics')
    plt.xlabel('Temperature, T')
    plt.ylabel('Susceptibility, $\displaystyle \chi$')
    plt.plot(temperatures, susceptibilities)
    plt.show()
    main()

def display_mean_energy_plot_kawasaki():
    """
    Plot the mean energy against temperature for Kawasaki Dynamics.
    """
    datafile = np.loadtxt("ising_model_kawasaki_data.txt")
    temperatures = datafile[0]
    mean_energies = datafile[1]
    plt.title('Mean Energy against Temperature using Kawasaki Dynamics')
    plt.xlabel('Temperature, T')
    plt.ylabel('Average Energy, $\displaystyle\langle E \\rangle$')
    plt.plot(temperatures, mean_energies)
    plt.show()
    main()

def display_scaled_specific_heat_plot_kawasaki():
    """
    Plot the scaled specific heat capacity against temperature
    for Kawasaki Dynamics.
    """
    datafile = np.loadtxt("ising_model_kawasaki_data.txt")
    temperatures = datafile[0]
    scaled_specific_heat_capacities = datafile[2]
    bootstrap_errors = datafile[3]
    plt.title('Specific Heat Capacity against Temperature using Kawasaki Dynamics')
    plt.xlabel('Temperature, T')
    plt.ylabel('Specific Heat Capacity, C')
    plt.plot(temperatures, scaled_specific_heat_capacities)
    plt.errorbar(temperatures, scaled_specific_heat_capacities, 
        yerr=bootstrap_errors)
    plt.show()
    main()

def main():
    if len(sys.argv) != 2:
        print("Usage python3 ising.display_plots.py Glauber/Kawasaki")
        sys.exit()

    dynamics_type = sys.argv[1]
    while True:
        if dynamics_type == "Glauber":
            prompt = "Enter the observable plot you wish to display: \n"
            prompt += "E-(Energy)/AM-(Absolute Magnetisation)/" + \
                "SSH-(Scaled Specific Heat)/S-(Susceptibility)) \n"
            prompt += "(Enter 'q' to quit) "
            observable = input(prompt)
            if observable == "E":
                display_mean_energy_plot_glauber()
                main()
            elif observable == "AM":
                display_mean_absolute_magnetism_plot_glauber()
                main()
            elif observable == "SSH":
                display_scaled_specific_heat_plot_glauber()
                main()
            elif observable == "S":
                display_susceptibility_plot_glauber()
                main()
            elif observable == 'q':
                break
        elif dynamics_type == "Kawasaki":
            prompt = "Enter the observable plot you wish to display: \n"
            prompt += "(E-(Energy)/SSH-(Scaled Specific Heat)) \n"
            prompt += "(Enter 'q' to quit) "
            observable = input(prompt)
            if observable == "E":
                display_mean_energy_plot_kawasaki()
                main()
            elif observable == "SSH":
                display_scaled_specific_heat_plot_kawasaki()
                main()
            elif observable == 'q':
                break

main()