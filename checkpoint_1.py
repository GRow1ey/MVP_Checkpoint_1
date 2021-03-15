import matplotlib
matplotlib.use('TKAgg')
import math
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class SpinLattice():
    """A class to represent the lattice of spins in the Ising model."""

    def __init__(self, lattice_dimensions, temperature, dynamics_type):
        self.lattice_dimensions = lattice_dimensions
        self.spin_lattice = np.zeros((lattice_dimensions, lattice_dimensions), 
                                    dtype=float)
        self.temperature = temperature
        self.dynamics_type = dynamics_type
        self.J = 1.0
        self.nsteps = 10000

    def get_lattice_dimensions(self):
        """Method to return the dimensions of the n x n spin lattice."""
        return self.lattice_dimensions

    def get_spin_lattice(self):
        """Method to return the n x n spin lattice."""
        return self.spin_lattice

    def get_temperature(self):
        """Method to return the temperature of the system."""
        return self.temperature

    def get_dynamics_type(self):
        """Method to return the type of dynamics used in the simulation."""
        return self.dynamics_type

    def get_nsteps(self):
        """"""
        return self.nsteps

    def initialise_spin_lattice(self):
        """A method to initialise the lattice of spins."""
        number_rows = self.get_lattice_dimensions()
        number_columns = self.get_lattice_dimensions()
        spin_lattice = self.get_spin_lattice()

        for row in range(number_rows):
            for column in range(number_columns):
                random_number = random.random()
                if random_number < 0.5:
                    spin_lattice[row, column] = -1
                elif random_number >= 0.5:
                    spin_lattice[row, column] = 1
    
    def calculate_new_state(self, itrial, jtrial):
        """Calculate the new state."""
        dynamics_type = self.get_dynamics_type()
        nsteps = self.get_nsteps()
        number_rows = self.get_lattice_dimensions()
        number_columns = self.get_lattice_dimensions()
        spin_lattice = self.get_spin_lattice()
        
        if dynamics_type == "Glauber":
            pass
        
            for step in range(nsteps):
                for row in range(number_rows):
                    for column in range(number_columns):

            #select spin randomly

                        itrial = np.random.randint(0, number_rows)
                        jtrial = np.random.randint(0, number_columns)
                        new_spin = -spin_lattice[itrial, jtrial]

        elif dynamics_type == "Kawasaki":
            pass
        
        return new_spin

    def metropolis_algorithm(self, itrial, jtrial, new_spin):
        """"""
        random_number = random.random()
        spin_lattice = self.get_spin_lattice()
        boltzmann_weight = self.calculate_boltzmann_weight()
        if random_number <= boltzmann_weight:
            spin_lattice[itrial, jtrial] = new_spin

    def calculate_boltzmann_weight(self, energy_difference):
        """"""
        temperature = self.get_temperature()
        return np.exp(-energy_difference / temperature)

    def calculate_energy_difference(self):
        """"""