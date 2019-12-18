import numpy as np
import random
import math


import random as rand
from numpy.random import randint

# Tareas
tasks = [5930,3900,1700,6880,6800,2400,5960
        ,5400,8700,900,800,900,5900,7700,6200]


N = len(tasks) # 15 TAREAS 


def allOf(A,num):
    size = len(A)
    for i in range(size):
        if A[i] != num:
            return False
    return True



def Cal_E_T7(T_rate, tasks, N):
    Beta = 5e-7
    
    Cff =730e6 # Energia por ciclo
    Dff =860e3 # Byte/energia
    
    TC=np.zeros(N)
    EC=np.zeros(N)
    
    EL=np.zeros(N)
    Et=np.zeros(N)
    Er=np.zeros(N)
    
    TL=np.zeros(N)
    Tr=np.zeros(N)
    Tt=np.zeros(N)
    
    F_local=500e6
    F_cloud=10e9
    
    D_out=(3*np.random.rand(N))
    D_in= randint(10,31,N)
    
    for ii in range(N):
        D_in[ii] = 1/D_in[ii]
        D_out[ii] = 1/D_out[ii]
        
    Cci=D_in
    for i in range(N):
        EL[i] = tasks[i]/(8*Cff)
        TL[i] = tasks[i]/(8*F_local)
        
        Er[i] = 1/(8*Dff)
        Tr[i] = D_out[i]/T_rate
        Tc_temp = D_in[i] * tasks[i]/(8*F_cloud)
        
        Et[i] = 1/(8*Dff)
        Tt[i] = D_in[i]/T_rate
        
        TC[i] = Tr[i] + Tt[i] + Tc_temp
        EC[i] = Er[i] + Et[i] + Beta * Cci[i]
        
    return EL, EC, TL, TC , Cci
    




populationSize =3

dimention = len(tasks)
numIterations = 1000

lowerLimit = 0
upperLimit = 2
T_constraint=700

population=[]

blackHole={"star":[],"fitness":99999999}


iter1 = 50
E_min=1
T_constraint = 700
T_rate = 3e6

EC = []
EL = []
TL = []
TC = []

EL, EC, TL, TC , Cci = Cal_E_T7(T_rate, tasks, N)

E=np.zeros(N);
T=np.zeros(N);

def printPopulation():
	for i in population:
		print i

def initPopulation():
	for i in range(populationSize):
		star=randint(lowerLimit,upperLimit,dimention)
		individual = {"star":star,"fitness":0}
		population.append(individual)
			

def objetiveFunction(x):
	size_x = len(x)
	for i in range(size_x):
	    E[i]= x[i]*EL[i]+(1-x[i])*EC[i]
	    T[i]= x[i]*TL[i]+(1-x[i])*TC[i]
	    if(sum(T)>T_constraint):
	        return 9999999
	return sum(E)

def evaluatePopulation():
	for individual in population:
		individual["fitness"]=objetiveFunction(individual["star"])

def selectBlackHole():
	global blackHole
	population.sort(key=lambda x: x["fitness"])
	if population[0]["fitness"]<blackHole["fitness"]:	
		blackHole=population.pop(0)
		
		star =randint(lowerLimit,upperLimit,dimention)
		
		individual = {"star":star,"fitness":0}
		population.append(individual)
		
		
def changeLocationsStars():
	for individual in population:
		rand=np.random.rand(dimention)
		#individual["star"]=individual["star"]+(rand*(blackHole["star"]-individual["star"]))
		individual["star"]= np.logical_or(np.logical_not(individual["star"]),blackHole["star"]) #np.logical_or(np.logical_xor(blackHole["star"],individual["star"]),individual["star"])*1

		    
	evaluatePopulation()

def findStartWithLowerCost():
	global blackHole
	population.sort(key=lambda x: x["fitness"])

	if population[0]["fitness"] < blackHole["fitness"]:
		temp = population[0]
		population[0]=blackHole
		blackHole=temp



def crossingEventHorizon():
	sumFi=sum([ i['fitness'] for i in population])	
	R=blackHole["fitness"]/(sumFi)

	for inv in population:
		euclideanDistance=np.linalg.norm(blackHole["star"]-inv["star"]) 
		if euclideanDistance <  R:
			star =np.zeros(dimention)
			for j in range(dimention):
				star[j]=randint(lowerLimit,upperLimit)
			inv["star"]=star
			


def blackHoleAlgorithm():
	print "Inicializando poblacion"
	initPopulation()
	printPopulation()
	evaluatePopulation()
	for i in range(numIterations):
		evaluatePopulation()

		selectBlackHole()
		changeLocationsStars()
		findStartWithLowerCost()
		crossingEventHorizon()
	print blackHole
	print "Energia minima : ", blackHole['fitness']

import time
start_time = time.time()
				
blackHoleAlgorithm()

print("--- %s seconds ---" % (time.time() - start_time))


