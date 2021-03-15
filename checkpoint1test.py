import matplotlib
matplotlib.use('TKAgg')
import math
import random
import numpy as np
import matplotlib.pyplot as plt
from checkpoint1 import Spins
import matplotlib.animation as animation

# process data values for glauber simulation for temeratures between 1 and 3 
def glaubnewvalues():
    temperatures = np.arange(1,3,0.1)
    suslist = []
    elist = []
    capaclist = []
    absmagnetlist = []
    sigmaclist = []
    size = int(input("Please enter system size: "))
    for t in range(len(temperatures)):
        v = Spins(size,temperatures[t])
        magnet, magnetsq, absmagnet, energyv, energyvsq, bootsenergy = v.runglaubernoanim()
        mav = magnet/1000
        msqav = magnetsq/1000
        mabs = absmagnet/1000
        eav = energyv/1000
        esqav = energyvsq/1000
        suscept = (msqav-(mav**2))/((size**2)*temperatures[t])
        capacity = (esqav-(eav**2))/((size**2)*(temperatures[t]**2))
        absmagnetlist.append(mabs)
        suslist.append(suscept)
        elist.append(eav)
        capaclist.append(capacity)
        #bootstrap error of specific heat
        resampledcapacitylist = []
        for k in range (1000):
            resampledcapacity = bootstrap(bootsenergy,size,temperatures[t])
            resampledcapacitylist.append(resampledcapacity)
        resq = (sum([number ** 2 for number in resampledcapacitylist]))/1000
        re = (sum(resampledcapacitylist))/1000
        sigma = math.sqrt((resq)-(re**2))
        sigmaclist.append(sigma)
    #write all data to file    
    dataarray = np.vstack((temperatures, np.array(absmagnetlist), np.array(suslist), np.array(elist), np.array(capaclist), np.array(sigmaclist)))
    np.savetxt("glauberdata1.txt",dataarray)

# reampling for bootstrap correction
def bootstrap(energies,size,temp):
    resampled = []
    n = len(energies)
    for q in range(n):
        r = random.random()
        index = int(r*n)-1
        resampled.append(energies[index])
    esqav = (sum([number ** 2 for number in resampled]))/1000
    eav = sum(resampled)/1000
    capacity = (esqav-(eav**2))/((size**2)*(temp))
    return capacity

# process data values for kawasaki simulation for temeratures between 1 and 3 
def kawanewvalues():
    temperatures = np.arange(1,3,0.1)
    elist = []
    capaclist = []
    sigmaclist = []
    size = int(input("Please enter system size: "))
    for t in range(len(temperatures)):
        v = Spins(size,temperatures[t])
        energyv, energyvsq, bootsenergy = v.runkawanoanim()
        eav = energyv/1000
        esqav = energyvsq/1000
        capacity = (esqav-(eav**2))/((size**2)*(temperatures[t]**2))
        print (eav)
        print (capacity)
        elist.append(eav)
        capaclist.append(capacity)
        #bootstrap error of specific heat
        resampledcapacitylist = []
        for k in range (1000):
            resampledcapacity = bootstrap(bootsenergy,size,temperatures[t])
            resampledcapacitylist.append(resampledcapacity)
        resq = (sum([number ** 2 for number in resampledcapacitylist]))/1000
        re = (sum(resampledcapacitylist))/1000
        sigma = math.sqrt((resq)-(re**2))
        sigmaclist.append(sigma)
        print ("error:" +str(sigma))
    #write all data to file
    dataarray = np.vstack((temperatures, np.array(elist), np.array(capaclist), np.array(sigmaclist)))
    np.savetxt("kawadata.txt",dataarray)

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


# main navigation menu
def main():
    choice = input("""
                    A: Glauber 
                    B: Kawasaki 
                    Please enter your choice: """)
    if choice == "A" or choice =="a":
            choice2 = input("""
                    A: Animation 
                    B: Calculate Values for Observables
                    C: Load Average Energy against T Plot
                    D: Load Average Absolute of Magenetisation against T Plot
                    E: Load Specific Heat against T Plot
                    F: Load Susceptibility against Plot
                    G: Back
                    Please enter your choice: """)
            if choice2 == "A" or choice2 =="a":
                size = int(input("Please enter system size: "))
                temp = float(input("Please enter temperature: "))
                v = Spins(size,temp)
                v.runglauber()
            if choice2 == "B" or choice2 =="b":
                glaubnewvalues()
                main()  
            if choice2 == "C" or choice2 =="c":
                glauben()
            if choice2 == "D" or choice2 =="d":
                glaubmag()
            if choice2 == "E" or choice2 =="e":
                glaubsh()
            if choice2 == "F" or choice2 =="f":
                glaubsus()
            if choice2 == "G" or choice2 =="g":
                main()
    elif choice == "B" or choice =="b":
            choice2 = input("""
                    A: Animation 
                    B: Calculate Values for Observables 
                    C: Load Average Energy against T Plot
                    D: Load Specific Heat against T Plot
                    E: Back
                    Please enter your choice: """)
            if choice2 == "A" or choice2 =="a" :
                size = int(input("Please enter system size: "))
                temp = float(input("Please enter temperature: "))
                v = Spins(size,temp)
                v.runkawa()
            if choice2 == "B" or choice2 =="b":
                kawanewvalues()
                main()  
            if choice2 == "C" or choice2 =="c":
                kawaen()
            if choice2 == "D" or choice2 =="d":
                kawash()
            if choice2 == "E" or choice2 =="e":
                main()        
        
            
main()