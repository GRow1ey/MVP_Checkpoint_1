import matplotlib
matplotlib.use('TKAgg')

import sys
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
        self.itrial = 0
        self.jtrial = 0

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
    def get_J(self):
        """Method to return J."""
        return self.J

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
    
    def calculate_new_state(self):
        """Calculate the new state."""
        number_rows = self.get_lattice_dimensions()
        number_columns = self.get_lattice_dimensions()
        spin_lattice = self.get_spin_lattice()
        
        #select spin randomly
        self.itrial = np.random.randint(0, number_rows)
        self.jtrial = np.random.randint(0, number_columns)
        new_spin = -spin_lattice[self.itrial, self.jtrial]
                            
        return new_spin

    def find_nearest_neighbours(self, itrial, jtrial):
        """Find the nearest neighbours of the current state."""
        number_rows = self.get_lattice_dimensions()
        number_columns = self.get_lattice_dimensions()
        left = 0
        right = 0
        above = 0
        below = 0
        if (itrial - 1) < 0:
            left = ((number_columns - 1), jtrial)
        else:
            left = ((itrial - 1), jtrial)
        if (itrial + 1) > (number_columns - 1):
            right = (((itrial + 1) % number_columns), jtrial)
        else:
            right = ((itrial + 1), jtrial)
        if (jtrial - 1) < 0:
            above = (itrial, (number_rows - 1))
        else:
            above = (itrial, (jtrial - 1))
        if (jtrial + 1) > (number_rows - 1):
            below = (itrial, ((jtrial + 1) % number_rows))
        else:
            below = (itrial, (jtrial + 1))
        return [left, right, above, below]

    def calculate_mean_total_energy(self, itrial, jtrial):
        """"""
        J = self.get_J()
        nearest_neighbours_indices = self.find_nearest_neighbours(itrial, jtrial)
        spin_lattice = self.get_spin_lattice()
        sum_over_nearest_neighbours = 0
        for nearest_neighbour_index in nearest_neighbours_indices:
            sum_over_nearest_neighbours += spin_lattice[itrial, jtrial] * \
                                    spin_lattice[nearest_neighbour_index[0], 
                                                nearest_neighbour_index[1]]

        return -J * sum_over_nearest_neighbours

    def calculate_energy_difference(self, itrial, jtrial):
        """"""
        return self.calculate_mean_total_energy(itrial, jtrial) - \
            self.calculate_mean_total_energy(itrial, jtrial)

    def metropolis_algorithm(self, new_spin, energy_difference):
        """"""
        random_number = random.random()
        spin_lattice = self.get_spin_lattice()
        boltzmann_weight = self.calculate_boltzmann_weight(energy_difference)
        if energy_difference <= 0:
            self.spin_lattice[self.itrial, self.jtrial] = new_spin
        elif random_number <= boltzmann_weight:
            spin_lattice[self.itrial, self.jtrial] = new_spin

    def calculate_boltzmann_weight(self, energy_difference):
        """"""
        temperature = self.get_temperature()
        return np.exp(-energy_difference / temperature)

    