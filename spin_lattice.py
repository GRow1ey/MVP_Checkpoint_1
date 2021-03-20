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
    
    def select_new_state(self):
        """Calculate the new state."""
        number_rows = self.get_lattice_dimensions()
        number_columns = self.get_lattice_dimensions()
        spin_lattice = self.get_spin_lattice()
        
        #select spin randomly
        self.itrial = np.random.randint(0, number_rows)
        self.jtrial = np.random.randint(0, number_columns)

    def find_nearest_neighbours(self):
        """Find the nearest neighbours of the current state."""
        number_rows = self.get_lattice_dimensions()
        number_columns = self.get_lattice_dimensions()
        left = 0
        right = 0
        above = 0
        below = 0
        if (self.itrial - 1) < 0:
            left = ((number_columns - 1), self.jtrial)
        else:
            left = ((self.itrial - 1), self.jtrial)
        if (self.itrial + 1) >= (number_columns - 1):
            right = (((self.itrial + 1) % number_columns), self.jtrial)
        else:
            right = ((self.itrial + 1), self.jtrial)
        if (self.jtrial - 1) < 0:
            above = (self.itrial, (number_rows - 1))
        else:
            above = (self.itrial, (self.jtrial - 1))
        if (self.jtrial + 1) >= (number_rows - 1):
            below = (self.itrial, ((self.jtrial + 1) % number_rows))
        else:
            below = (self.itrial, (self.jtrial + 1))
        return [left, right, above, below]

    def calculate_mean_total_energy(self):
        """"""
        J = self.get_J()
        nearest_neighbours_indices = self.find_nearest_neighbours()
        spin_lattice = self.get_spin_lattice()
        sum_over_nearest_neighbours = 0
        for nearest_neighbour_index in nearest_neighbours_indices:
            sum_over_nearest_neighbours += spin_lattice[self.itrial, self.jtrial] * \
                                    spin_lattice[nearest_neighbour_index[0], 
                                                nearest_neighbour_index[1]]

        return sum_over_nearest_neighbours

    def calculate_energy_difference(self):
        """"""
        nearest_neighbours_indices = self.find_nearest_neighbours()
        sum_over_nearest_neighbours = 0
        spin_lattice = self.get_spin_lattice()
        J = self.get_J()
        for neighbour in nearest_neighbours_indices:
            sum_over_nearest_neighbours += spin_lattice[neighbour[0], 
                                        neighbour[1]]
        delta_E = 2 * J * spin_lattice[self.itrial, self.jtrial] * \
                sum_over_nearest_neighbours
        return delta_E

    def metropolis_algorithm(self, energy_difference):
        """"""
        random_number = random.random()
        spin_lattice = self.get_spin_lattice()
        boltzmann_weight = self.calculate_boltzmann_weight(energy_difference)
        if energy_difference <= 0:
            spin_lattice[self.itrial, self.jtrial] *= -1
        elif random_number <= boltzmann_weight:
            spin_lattice[self.itrial, self.jtrial] *= -1

    def calculate_boltzmann_weight(self, energy_difference):
        """"""
        temperature = self.get_temperature()
        return np.exp(-energy_difference / temperature)

    