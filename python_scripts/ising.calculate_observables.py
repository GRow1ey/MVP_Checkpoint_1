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
    if len(sys.argv) != 3:
        print("Usage python3 ising.calculate_observables.py N Glauber/Kawasaki")
        sys.exit()

    lattice_dimensions = int(sys.argv[1])
    dynamics_type = sys.argv[2]

    if dynamics_type == "Glauber":
        temperatures = np.arange(1, 3, 0.1)
        susceptibilities = []
        energies = []
        scaled_heat_capacities = []
        absolute_magnetisms = []
        sum_over_resampled_scaled_heat_capacities = []

        for temperature in temperatures:
            ising_model = SpinLattice(lattice_dimensions, temperature)
            total_magnetisation, total_magnetisation_squared, \
            absolute_magnetisation, total_energy, \
            total_energy_squared, bootstrap_energies = \
                ising_model.calculate_observables_glauber()
            
            # Calculate the mean values of the observables
            # Mean of magnetisation values
            mean_total_magnetisation = total_magnetisation / 1000
            mean_squared_total_magnetisation = \
                                            total_magnetisation_squared / 1000
            mean_absolute_magnetisation = absolute_magnetisation / 1000

            # Mean of energy values
            mean_total_energy = total_energy / 1000
            mean_squared_total_energy = total_energy_squared / 1000
            
            # Calculate the susceptibility
            susceptibility = (1 / ((lattice_dimensions ** 2) * temperature)) \
                * (mean_squared_total_magnetisation - \
                    (mean_total_magnetisation ** 2))

            # Calculate the scaled heat capacity (or heat capacity per spin)
            scaled_heat_capacity = (1 / ((lattice_dimensions ** 2) * \
                temperature)) * (mean_squared_total_energy - \
                    mean_total_energy ** 2)

            # Append the calculated values to their corresponding lists
            absolute_magnetisms.append(mean_absolute_magnetisation)
            susceptibilities.append(susceptibility)
            energies.append(mean_total_energy)
            scaled_heat_capacities.append(scaled_heat_capacity)

            # Resample the data
            resampled_scaled_heat_capacities = []

            for k in range(1000):
                # Calculate the resampled scaled heat capacity
                resampled_scaled_heat_capacity = \
                    ising_model.bootstrap(bootstrap_energies, temperature)

                resampled_scaled_heat_capacities.append(\
                    resampled_scaled_heat_capacity)
            
            # Calculate the resamplings of scaled heat capacity
            mean_sum_squared_resampled_scaled_heat_capacity = \
                (sum([resampled_scaled_heat_capacity ** 2 for 
                resampled_scaled_heat_capacity in 
                resampled_scaled_heat_capacities])) / 1000
            mean_sum_resampled_scaled_heat_capacity = \
                (sum(resampled_scaled_heat_capacities)) / 1000
            
            sum_over_resampled_scaled_heat_capacity = \
                math.sqrt(mean_sum_squared_resampled_scaled_heat_capacity \
                    - (mean_sum_resampled_scaled_heat_capacity ** 2))
            
            sum_over_resampled_scaled_heat_capacities.append(\
                sum_over_resampled_scaled_heat_capacity)

        # Write observable data to file
        observables_data = np.vstack((temperatures, 
            np.array(absolute_magnetisms), np.array(susceptibilities), 
            np.array(energies), np.array(scaled_heat_capacities), 
            np.array(sum_over_resampled_scaled_heat_capacities)))

        np.savetxt("ising_model_glauber_data.txt", observables_data)
            
    elif dynamics_type == "Kawasaki":
        temperatures = np.arange(1, 3, 0.1)
        energies = []
        scaled_heat_capacities = []
        sum_over_resampled_scaled_heat_capacities = []

        for temperature in temperatures:
            ising_model = SpinLattice(lattice_dimensions, temperature)
            total_energy, total_energy_squared, bootstrap_energies = \
                ising_model.calculate_observables_kawasaki()
            
            # Calculate the mean values of the observables
            # Mean of energy values
            mean_total_energy = total_energy / 1000
            mean_squared_total_energy = total_energy_squared / 1000
            
            # Calculate the scaled heat capacity (or heat capacity per spin)
            scaled_heat_capacity = (1 / ((lattice_dimensions ** 2) * \
                temperature)) * (mean_squared_total_energy - \
                    mean_total_energy ** 2)

            # Append the calculated values to their corresponding lists
            energies.append(mean_total_energy)
            scaled_heat_capacities.append(scaled_heat_capacity)

            # Resample the data
            resampled_scaled_heat_capacities = []

            for k in range(1000):
                # Calculate the resampled scaled heat capacity
                resampled_scaled_heat_capacity = \
                    ising_model.bootstrap(bootstrap_energies, temperature)

                resampled_scaled_heat_capacities.append(\
                    resampled_scaled_heat_capacity)
            
            # Calculate the resamplings of scaled heat capacity
            mean_sum_squared_resampled_scaled_heat_capacity = \
                (sum([resampled_scaled_heat_capacity ** 2 for 
                resampled_scaled_heat_capacity in 
                resampled_scaled_heat_capacities])) / 1000
            mean_sum_resampled_scaled_heat_capacity = \
                (sum(resampled_scaled_heat_capacities)) / 1000
            
            sum_over_resampled_scaled_heat_capacity = \
                math.sqrt(mean_sum_squared_resampled_scaled_heat_capacity \
                    - (mean_sum_resampled_scaled_heat_capacity ** 2))
            
            sum_over_resampled_scaled_heat_capacities.append(\
                sum_over_resampled_scaled_heat_capacity)

        # Write observable data to file
        observables_data = np.vstack((temperatures, 
            np.array(energies), np.array(scaled_heat_capacities), 
            np.array(sum_over_resampled_scaled_heat_capacities)))

        np.savetxt("ising_model_kawasaki_data.txt", observables_data)
main()
