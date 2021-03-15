import matplotlib
matplotlib.use('TKAgg')
import math
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class Spins(object): 

    def __init__(self, size, temp):
        self.sizex = size
        self.sizey = size
        self.kT = temp
        self.J=1.0
        self.nstep = 10300
        self.trialxst = 0
        self.trialyst = 0
        self.trialxst1 = 0
        self.trialyst1 = 0
        self.spinarray = np.zeros((self.sizex,self.sizey),dtype=float)
        

 #UNIVERSAL/DATA VALUE METHODS 
    
    # initialisation for simulation glauber/kawasaki
    def initialisespinsself(self):
        for i in range(self.sizex):
            for j in range(self.sizey):
                r=random.random()
                if(r<0.5): 
                    self.spinarray[i,j]=-1
                if(r>=0.5): 
                    self.spinarray[i,j]=1
        return self.spinarray
    
    # find nearest neighbours of selected spin
    def findnearest(self,valx,valy):
        nn = [1,-1]
        nn_list = []
        for n in range(len(nn)):
            nebx = valx + nn[n]
            neby = valy + nn[n]
            if nebx>=(self.sizex-1):
                nebx = nebx%self.sizex  
            if nebx<0:
                nebx = self.sizex-1
            if neby>=(self.sizey-1):
                neby = neby%self.sizey
            if neby<0:
                neby = self.sizey-1
            nn_list.append([valx,neby])
            nn_list.append([nebx,valy])
        return nn_list
    
    #find overall magnetisation of system for data values - not used for kawasaki as no change in magnetisation
    def magnetisation(self):
        sigma = 0
        for i in range (self.sizex):
            for j in range (self.sizey):
                sigma += self.spinarray[i,j]
        return sigma

    # find overall energy of system for data values
    def avenergy(self):
        neighbouren = 0
        for i in range(self.sizex):
            for j in range (self.sizey):
                neighbours = self.findnearest(i,j)
                sigma = 0
                for p in range(4):   
                    sigma += self.spinarray[neighbours[p][0],neighbours[p][1]]
                neighbouren += (-1)*self.spinarray[i,j]*sigma
        return (0.5*neighbouren)

    

 #GLAUBER METHODS

    # initalisation for accurate calculation of glauber data values (all up) - NOT USED FOR ANIMATION
    def glaubinitialisespinsself(self):
        for i in range(self.sizex):
            for j in range(self.sizey):
                self.spinarray[i,j]=1
        return self.spinarray

    #select one trial spin randomly
    def glaubermarkov(self):
        trialx=np.random.randint(0,self.sizex)
        trialy=np.random.randint(0,self.sizey) 
        self.trialxst = trialx
        self.trialyst = trialy
        return self.spinarray

    # energy diffrence between current and trial state
    def energydiffernce(self):
        sigma = 0
        neighbourlist = self.findnearest(self.trialxst,self.trialyst)
        for i in range(4):
            sigma += self.spinarray[neighbourlist[i][0],neighbourlist[i][1]]
        deltae = 2*self.J*self.spinarray[self.trialxst,self.trialyst]*sigma
        return deltae
    
    # accept state if energy difference is negative or with specified probability
    def metropolis(self):
        r = random.random()
        energyval = self.energydiffernce()
        if energyval<=0:
            self.spinarray[self.trialxst,self.trialyst] = (-1)*self.spinarray[self.trialxst,self.trialyst]
        elif r<=np.exp(-energyval/self.kT):
            self.spinarray[self.trialxst,self.trialyst] = (-1)*self.spinarray[self.trialxst,self.trialyst]
        return self.spinarray
            
    # run glauber simulation + animation and save spin data to file       
    def runglauber(self):
        self.initialisespinsself()
        for n in range(self.nstep):
            for i in range(self.sizex):
                for j in range(self.sizey):
                    self.glaubermarkov()
                    self.metropolis()
            if n%10==0:                    
                f=open('spins.dat','w')
                for i in range(self.sizex):
                    for j in range(self.sizey):
                        f.write('%d %d %lf\n'%(i,j,self.spinarray[i,j]))
                f.close()
                plt.cla()
                im=plt.imshow(self.spinarray, animated=True)
                plt.draw()
                plt.pause(0.0001)

    # run glauber simulation (no animation) to process data values
    def runglaubernoanim(self):
        self.glaubinitialisespinsself()
        magnet = 0
        absmagnet = 0
        magnetsq = 0
        energyv = 0
        energyvsq = 0
        bootsenergy = []
        for n in range(self.nstep):
            for i in range(self.sizex):
                for j in range(self.sizey):
                    self.glaubermarkov()
                    self.metropolis()
            if (n%10==0) and (n>300):  
                valmag = self.magnetisation()
                valen = self.avenergy()
                magnet += valmag
                magnetsq += (valmag**2)
                absmagnet += abs(valmag)
                energyv += valen
                energyvsq += (valen**2)
                bootsenergy.append(valen)
        return magnet, magnetsq, absmagnet, energyv, energyvsq, bootsenergy            


 # KAWASAKI METHODS

    # initalisation for accurate calculation of kawasaki data values (half up) - not used for animation !!!DID NOT LIKE THIS, REMOVED
    #def kawainitialisespinsself(self):
    #    uparray = np.ones((int(self.sizex/2),self.sizey),dtype=float)
    #    downarray = (-1)*np.ones((int(self.sizex/2),self.sizey),dtype=float)
    #    self.spinarray = np.concatenate((uparray,downarray))
    #    return self.spinarray

    # select 2 trial spins randomly
    def kawasakimarkov(self):
        trialx=np.random.randint(0,self.sizex)
        trialy=np.random.randint(0,self.sizey) 
        trialx1=np.random.randint(0,self.sizex)
        trialy1=np.random.randint(0,self.sizey) 
        while self.spinarray[trialx,trialy] == self.spinarray[trialx1,trialy1]: # ensure selected spins are different
            trialx=np.random.randint(0,self.sizex)
            trialy=np.random.randint(0,self.sizey) 
            trialx1=np.random.randint(0,self.sizex)
            trialy1=np.random.randint(0,self.sizey) 
        self.trialxst = trialx
        self.trialyst = trialy
        self.trialxst1 = trialx1
        self.trialyst1 = trialy1
        return self.spinarray
    
    # energy diffrence between current and trial state, correcting for nearest neighbour errors between selected spins
    def kawaenergydiffernce(self):
        val1 = self.spinarray[self.trialxst,self.trialyst]
        val2 = self.spinarray[self.trialxst1,self.trialyst1]
        val1nn = self.findnearest(self.trialxst,self.trialyst)
        val2nn = self.findnearest(self.trialxst1,self.trialyst1)
        #self.spinarray = np.copy(self.spinarray)
        #self.spinarray[self.trialxst,self.trialyst] = val2
        #self.spinarray[self.trialxst1,self.trialyst1] = val1
        sigmai = 0
        sigmaj = 0
        for i in range(4):   
            sigmai += self.spinarray[val1nn[i][0],val1nn[i][1]]
            if [val2nn[i][0],val2nn[i][1]] not in val1nn:
                sigmaj += self.spinarray[val2nn[i][0],val2nn[i][1]]
        deltae = 2*self.J*(val1*sigmai + val2*sigmaj)
        return deltae

    # accept state if energy difference is negative or with specified probability - note that swap was performed in kawaenergydiffernce so rejects and reverts back if probability not satisfied/posistive energy difference
    def kawametropolis(self):
        r = random.random()
        energyval = self.kawaenergydiffernce()
        if energyval<=0:
            self.spinarray[self.trialxst,self.trialyst] = (-1)*self.spinarray[self.trialxst,self.trialyst]
            self.spinarray[self.trialxst1,self.trialyst1] = (-1)*self.spinarray[self.trialxst1,self.trialyst1]
        elif r<=np.exp(-energyval /self.kT):
            self.spinarray[self.trialxst,self.trialyst] = (-1)*self.spinarray[self.trialxst,self.trialyst]
            self.spinarray[self.trialxst1,self.trialyst1] = (-1)*self.spinarray[self.trialxst1,self.trialyst1]
        return self.spinarray

    # run kawasaki simulation + animation and save spin data to file 
    def runkawa(self):
        self.initialisespinsself()
        for n in range(self.nstep):
            for i in range(self.sizex):
                for j in range(self.sizey):
                    self.kawasakimarkov()
                    self.kawametropolis()
            if n%10==0:                    
                l=open('kawaspins.dat','w')
                for i in range(self.sizex):
                    for j in range(self.sizey):
                        l.write('%d %d %lf\n'%(i,j,self.spinarray[i,j]))
                l.close()
                plt.cla()
                im=plt.imshow(self.spinarray, animated=True)
                plt.draw()
                plt.pause(0.0001)

    # run kawasaki simulation (no animation) to process data values    
    def runkawanoanim(self):
        self.initialisespinsself()
        energyv = 0
        energyvsq = 0
        bootsenergy = []
        for n in range(self.nstep):
            for i in range(self.sizex):
                for j in range(self.sizey):
                    self.kawasakimarkov()
                    self.kawametropolis()
            if (n%10==0) and (n>300): 
                valen = self.avenergy()
                energyv += valen
                energyvsq += (valen**2)
                bootsenergy.append(valen)
        return energyv, energyvsq, bootsenergy 
        
