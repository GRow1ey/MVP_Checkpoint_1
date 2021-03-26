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
        self.itrial_1 = 0
        self.jtrial_1 = 0

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

    def get_itrial(self):
        """Method to return itrial."""
        return self.itrial

    def get_jtrial(self):
        """Method to return itrial."""
        return self.jtrial

    def get_itrial_1(self):
        """Method to return itrial."""
        return self.itrial_1

    def get_jtrial_1(self):
        """Method to return itrial."""
        return self.jtrial_1

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
        if (itrial + 1) >= (number_columns - 1):
            right = (((itrial + 1) % number_columns), jtrial)
        else:
            right = ((itrial + 1), jtrial)
        if (jtrial - 1) < 0:
            above = (itrial, (number_rows - 1))
        else:
            above = (itrial, (jtrial - 1))
        if (jtrial + 1) >= (number_rows - 1):
            below = (itrial, ((jtrial + 1) % number_rows))
        else:
            below = (itrial, (jtrial + 1))
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

    def calculate_average_energy(self):
        """"""
        number_rows = self.get_lattice_dimensions()
        number_columns = self.get_lattice_dimensions()
        spin_lattice = self.get_spin_lattice()
        energy_neighbours = 0
        for column in range(number_columns):
            for row in range(number_rows):
                nearest_neighbours_indices = \
                    self.find_nearest_neighbours(column, row)
                sum_over_nearest_neighbours = 0
                for neighbour in nearest_neighbours_indices:
                    sum_over_nearest_neighbours += spin_lattice[neighbour[0], 
                                        neighbour[1]]
                energy_neighbours += (-1) * spin_lattice[column, row] * \
                                sum_over_nearest_neighbours

    def calculate_boltzmann_weight(self, energy_difference):
        """"""
        temperature = self.get_temperature()
        return np.exp(-energy_difference / temperature)

    def calculate_magnetisation(self):
        """"""
        number_rows = self.get_lattice_dimensions()
        number_columns = self.get_lattice_dimensions()
        spin_lattice = self.get_spin_lattice()
        sum_over_spins = 0
        for row in range(number_rows):
            for column in range(number_columns):
                sum_over_spins += spin_lattice[row, column]
        return sum_over_spins
        
    # Glauber Methods

    def select_new_state_glauber(self):
        """Calculate the new state."""
        number_rows = self.get_lattice_dimensions()
        number_columns = self.get_lattice_dimensions()
        spin_lattice = self.get_spin_lattice()
        
        #select spin randomly
        self.itrial = np.random.randint(0, number_rows)
        self.jtrial = np.random.randint(0, number_columns)

    def calculate_energy_difference_glauber(self):
        """"""
        nearest_neighbours_indices = self.find_nearest_neighbours(self.itrial, self.jtrial)
        sum_over_nearest_neighbours = 0
        spin_lattice = self.get_spin_lattice()
        J = self.get_J()
        for neighbour in nearest_neighbours_indices:
            sum_over_nearest_neighbours += spin_lattice[neighbour[0], 
                                        neighbour[1]]
        delta_E = 2 * J * spin_lattice[self.itrial, self.jtrial] * \
                sum_over_nearest_neighbours
        return delta_E

    def metropolis_algorithm_glauber(self, energy_difference):
        """"""
        random_number = random.random()
        spin_lattice = self.get_spin_lattice()
        boltzmann_weight = self.calculate_boltzmann_weight(energy_difference)
        if energy_difference <= 0:
            spin_lattice[self.itrial, self.jtrial] *= -1
        elif random_number <= boltzmann_weight:
            spin_lattice[self.itrial, self.jtrial] *= -1

    # Kawasaki Methods

    def select_new_state_kawasaki(self):
            """Select the new state."""
            number_rows = self.get_lattice_dimensions()
            number_columns = self.get_lattice_dimensions()
            spin_lattice = self.get_spin_lattice()
            
            # Select two trial spins randomly
            self.itrial = np.random.randint(0, number_rows)
            self.jtrial = np.random.randint(0, number_columns)
            self.itrial_1 = np.random.randint(0, number_rows)
            self.jtrial_1 = np.random.randint(0, number_columns)

            while self.spin_lattice[self.itrial, self.jtrial] == \
                self.spin_lattice[self.itrial_1, self.jtrial_1]:
                self.itrial = np.random.randint(0, number_rows)
                self.jtrial = np.random.randint(0, number_columns)
                self.itrial_1 = np.random.randint(0, number_rows)
                self.jtrial_1 = np.random.randint(0, number_columns)

    def calculate_energy_difference_kawasaki(self):
            """"""
            itrial = self.get_itrial()
            jtrial = self.get_jtrial()
            itrial_1 = self.get_itrial_1()
            jtrial_1 = self.get_jtrial_1()
            nearest_neighbours_indices_state_0 = \
                                    self.find_nearest_neighbours(itrial, jtrial)
            nearest_neighbours_indices_state_1 = \
                                    self.find_nearest_neighbours(itrial_1, 
                                                                jtrial_1)
            sum_over_nearest_neighbours_state_0 = 0
            sum_over_nearest_neighbours_state_1 = 0
            spin_lattice = self.get_spin_lattice()
            J = self.get_J()
            for i in range(len(nearest_neighbours_indices_state_0)):
                sum_over_nearest_neighbours_state_0 += \
                            spin_lattice[nearest_neighbours_indices_state_0[i][0], 
                                        nearest_neighbours_indices_state_0[i][1]]
                if [nearest_neighbours_indices_state_1[i][0], 
                    nearest_neighbours_indices_state_1[i][1]] not in \
                    nearest_neighbours_indices_state_0:
                    sum_over_nearest_neighbours_state_1 += \
                            spin_lattice[nearest_neighbours_indices_state_1[i][0],
                                        nearest_neighbours_indices_state_1[i][1]]
            delta_E = 2 * J * spin_lattice[itrial, jtrial] * \
                    (sum_over_nearest_neighbours_state_0 + 
                    sum_over_nearest_neighbours_state_1)
            return delta_E

    def metropolis_algorithm_kawasaki(self, energy_difference):
            """"""
            random_number = random.random()
            spin_lattice = self.get_spin_lattice()
            boltzmann_weight = self.calculate_boltzmann_weight(energy_difference)
            if energy_difference <= 0:
                spin_lattice[self.itrial, self.jtrial] *= -1
                spin_lattice[self.itrial_1, self.jtrial_1] *= -1
            elif random_number <= boltzmann_weight:
                spin_lattice[self.itrial, self.jtrial] *= -1
                spin_lattice[self.itrial_1, self.jtrial_1] *= -1