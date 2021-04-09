import matplotlib
matplotlib.use('TKAgg')

import sys
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
class SpinLattice():
    """A class to represent the lattice of spins in the Ising model."""

    def __init__(self, lattice_dimensions, temperature):
        self.lattice_dimensions = lattice_dimensions
        self.spin_lattice = np.zeros((lattice_dimensions, lattice_dimensions), 
                                    dtype=float)
        self.temperature = temperature
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

    def get_J(self):
        """Method to return J."""
        return self.J

    def get_nsteps(self):
        """Method to return nsteps"""
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
        lattice_dimensions = self.get_lattice_dimensions()
        spin_lattice = self.get_spin_lattice()

        for row in range(lattice_dimensions):
            for column in range(lattice_dimensions):
                random_number = random.random()
                if random_number < 0.5:
                    spin_lattice[row, column] = -1
                elif random_number >= 0.5:
                    spin_lattice[row, column] = 1
    
    def find_nearest_neighbours(self, itrial, jtrial):
        """Find the nearest neighbours of the current state."""
        lattice_dimensions = self.get_lattice_dimensions()
        left = 0
        right = 0
        above = 0
        below = 0
        if (itrial - 1) < 0:
            left = ((lattice_dimensions - 1), jtrial)
        else:
            left = ((itrial - 1), jtrial)
        if (itrial + 1) >= (lattice_dimensions - 1):
            right = (((itrial + 1) % lattice_dimensions), jtrial)
        else:
            right = ((itrial + 1), jtrial)
        if (jtrial - 1) < 0:
            above = (itrial, (lattice_dimensions - 1))
        else:
            above = (itrial, (jtrial - 1))
        if (jtrial + 1) >= (lattice_dimensions - 1):
            below = (itrial, ((jtrial + 1) % lattice_dimensions))
        else:
            below = (itrial, (jtrial + 1))
        return [left, right, above, below]

    def calculate_mean_total_energy(self):
        """
        Calculate the mean total energy of the lattice of spins 
        representing the Ising model.
        """
        lattice_dimensions = self.get_lattice_dimensions()
        spin_lattice = self.get_spin_lattice()
        energy_neighbours = 0
        for column in range(lattice_dimensions):
            for row in range(lattice_dimensions):
                nearest_neighbours_indices = \
                    self.find_nearest_neighbours(column, row)
                sum_over_nearest_neighbours = 0
                for neighbour in nearest_neighbours_indices:
                    sum_over_nearest_neighbours += spin_lattice[neighbour[0], 
                                        neighbour[1]]
                energy_neighbours += (-1) * spin_lattice[column, row] * \
                                sum_over_nearest_neighbours

        return 0.5 * energy_neighbours

    def calculate_boltzmann_weight(self, energy_difference):
        """Calculate the Boltzman weight."""
        temperature = self.get_temperature()
        return np.exp(-energy_difference / temperature)

    def calculate_magnetisation(self):
        """
        Calculate the magnetisation of the spin lattice representing the
        Ising model.
        """
        lattice_dimensions = self.get_lattice_dimensions()
        spin_lattice = self.get_spin_lattice()
        sum_over_spins = 0
        for row in range(lattice_dimensions):
            for column in range(lattice_dimensions):
                sum_over_spins += spin_lattice[row, column]
        return sum_over_spins
        
    # Glauber Methods
    def initialise_spin_lattice_glauber(self):
        """
        Initialise the spin lattice for Glauber dynamics
        to allow accurate calculation of observables.
        All spins are initialised as being up (1).
        This is not used for animating the Ising model.
        """
        lattice_dimensions = self.get_lattice_dimensions()
        spin_lattice = self.get_spin_lattice()

        for row in range(lattice_dimensions):
            for column in range(lattice_dimensions):
                spin_lattice[row, column] = 1

    def select_new_state_glauber(self):
        """Calculate the new state."""
        lattice_dimensions = self.get_lattice_dimensions()
        
        # Select spin randomly
        self.itrial = np.random.randint(0, lattice_dimensions)
        self.jtrial = np.random.randint(0, lattice_dimensions)

    def calculate_energy_difference_glauber(self):
        """
        Calculate the energy difference between the original state
        and the generated trial state.
        """
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
        """
        Determine if the new trial state should be accepted, by
        comparing the energy difference.
        The new state is accepted if the energy difference is less
        than or equal to zero or less than or equal to the Boltzmann
        probability distribution.
        """
        random_number = random.random()
        spin_lattice = self.get_spin_lattice()
        boltzmann_weight = self.calculate_boltzmann_weight(energy_difference)
        if energy_difference <= 0:
            spin_lattice[self.itrial, self.jtrial] *= -1
        elif random_number <= boltzmann_weight:
            spin_lattice[self.itrial, self.jtrial] *= -1

    def calculate_observables_glauber(self):
        """
        Calculate the observables using Glauber dynamics.
        """
        nsteps = self.get_nsteps()
        lattice_dimensions = self.get_lattice_dimensions()
        self.initialise_spin_lattice_glauber()

        total_magnetisation = 0
        absolute_magnetisation = 0
        total_magnetisation_squared = 0
        total_energy = 0
        total_energy_squared = 0
        bootstrap_energies = []

        for step in range(nsteps):
            for i in range(lattice_dimensions):
                for j in range(lattice_dimensions):
                    self.select_new_state_glauber()
                    delta_E = self.calculate_energy_difference_glauber()
                    self.metropolis_algorithm_glauber(delta_E)

            if (step % 10 == 0) and (step > 400):
                current_magnetisation = self.calculate_magnetisation()
                current_energy = self.calculate_mean_total_energy()

                # Sum over magnetisation values
                total_magnetisation += current_magnetisation
                total_magnetisation_squared += current_magnetisation ** 2
                absolute_magnetisation += abs(current_magnetisation)

                # Sum over energy values
                total_energy += current_energy
                total_energy_squared += current_energy ** 2

                # Append current energy to boostrap energies list
                bootstrap_energies.append(current_energy)

        return total_magnetisation, total_magnetisation_squared, \
                absolute_magnetisation, total_energy, \
                total_energy_squared, bootstrap_energies

    def bootstrap(self, energies, temperature):
        """
        Calculate the resampled scaled heat capacity using bootstrap
        method to resample the energy values.
        """
        lattice_dimensions = self.get_lattice_dimensions()
        resampled_energies = []
        length_energies = len(energies)
        for i in range(length_energies):
            random_number = random.random()
            energy_index = int(random_number * length_energies) - 1

            resampled_energies.append(energies[energy_index])
            
        mean_sum_squared_resampled_energy = \
            (sum([resampled_energy ** 2 for resampled_energy in \
                resampled_energies])) / 1000
        mean_sum_resampled_energy = sum(resampled_energies) / 1000

        # Calculate the resampled scaled heat capacity
        resampled_scaled_heat_capacity = \
            (1 / ((lattice_dimensions ** 2) * temperature)) * \
            (mean_sum_squared_resampled_energy - \
                mean_sum_resampled_energy ** 2)

        return resampled_scaled_heat_capacity


    # Kawasaki Methods

    def select_new_state_kawasaki(self):
            """Calculate the new state."""
            lattice_dimensions = self.get_lattice_dimensions()
            
            # Select two trial spins randomly
            self.itrial = np.random.randint(0, lattice_dimensions)
            self.jtrial = np.random.randint(0, lattice_dimensions)
            self.itrial_1 = np.random.randint(0, lattice_dimensions)
            self.jtrial_1 = np.random.randint(0, lattice_dimensions)

            while self.spin_lattice[self.itrial, self.jtrial] == \
                self.spin_lattice[self.itrial_1, self.jtrial_1]:
                self.itrial = np.random.randint(0, lattice_dimensions)
                self.jtrial = np.random.randint(0, lattice_dimensions)
                self.itrial_1 = np.random.randint(0, lattice_dimensions)
                self.jtrial_1 = np.random.randint(0, lattice_dimensions)

    def calculate_energy_difference_kawasaki(self):
            """
            Calculate the energy difference between the original state
            and the generated trial state.
            """
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
            delta_E = 2 * J * ((spin_lattice[itrial, jtrial] * \
                sum_over_nearest_neighbours_state_0) + \
                    (spin_lattice[itrial_1, jtrial_1] * \
                        sum_over_nearest_neighbours_state_1))
            return delta_E

    def metropolis_algorithm_kawasaki(self, energy_difference):
        """
        Determine if the new trial state should be accepted, by
        comparing the energy difference.
        The new state is accepted if the energy difference is less
        than or equal to zero or less than or equal to the Boltzmann
        probability distribution.
        """
        random_number = random.random()
        spin_lattice = self.get_spin_lattice()
        boltzmann_weight = self.calculate_boltzmann_weight(energy_difference)
        if energy_difference <= 0:
            spin_lattice[self.itrial, self.jtrial] *= -1
            spin_lattice[self.itrial_1, self.jtrial_1] *= -1
        elif random_number <= boltzmann_weight:
            spin_lattice[self.itrial, self.jtrial] *= -1
            spin_lattice[self.itrial_1, self.jtrial_1] *= -1

    def calculate_observables_kawasaki(self):
        """
        Calculate the observables using Kawasaki dynamics.
        """
        nsteps = self.get_nsteps()
        lattice_dimensions = self.get_lattice_dimensions()
        self.initialise_spin_lattice()

        total_energy = 0
        total_energy_squared = 0
        bootstrap_energies = []

        for step in range(nsteps):
            for i in range(lattice_dimensions):
                for j in range(lattice_dimensions):
                    self.select_new_state_kawasaki()
                    delta_E = self.calculate_energy_difference_kawasaki()
                    self.metropolis_algorithm_kawasaki(delta_E)

            if (step % 10 == 0) and (step > 400):
                current_energy = self.calculate_mean_total_energy()

                # Sum over energy values
                total_energy += current_energy
                total_energy_squared += current_energy ** 2

                # Append current energy to boostrap energies list
                bootstrap_energies.append(current_energy)

        return total_energy, total_energy_squared, bootstrap_energies
        