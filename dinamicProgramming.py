import numpy as np
import random as rand
from numpy.random import randint

def allOf(A,num):
    size = len(A)
    for i in range(size):
        if A[i] != num:
            return False
    return True


def Cal_E_T7(T_rate, tasks, N):
    Beta = 5e-7 # B es el 
    
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
    
    F_local=500e6   # CPU rate localy
    F_cloud=10e9    # CPU rateof Cloud
    
    D_out=(3*np.random.rand(N)) # Ouput data size  1 a 3 MB
    D_in= randint(10,31,N)      # Input data size  10 a 30 MB
    
    for ii in range(N):
        D_in[ii] = 1/D_in[ii]
        D_out[ii] = 1/D_out[ii]
        
    Cci=D_in
    for i in range(N):
        
        EL[i] = tasks[i]/(8*Cff) # Consumo de Energia local
        TL[i] = tasks[i]/(8*F_local) # Tiempo por tareas local
        
        Er[i] = 1/(8*Dff)   # Consumo de energia remoto
        Tr[i] = D_out[i]/T_rate # Tiempo de ejecucion remoto
        Tc_temp = D_in[i] * tasks[i]/(8*F_cloud) 
        
        Et[i] = 1/(8*Dff) # Consumo de energia Transmision
        Tt[i] = D_in[i]/T_rate # Tiempo de transmision
        
        TC[i] = Tr[i] + Tt[i] + Tc_temp
        
        EC[i] = Er[i] + Et[i] + Beta * Cci[i]  # 
        
    return EL, EC, TL, TC , Cci
    

def GA(tasks,N):
    mutation_probability = 0.5
    number_of_generations = 100000
    iter1 = 50
    E_min = 1
    T_constraint=700 # 
    T_rate=3e6; 
    EC=[]
    EL=[]
    TL=[]
    TC=[]
    
    EL, EC, TL, TC , Cci = Cal_E_T7(T_rate, tasks, N)

    
    x = randint(0,2,N)
    
    if allOf(x,1) or allOf(x,0):
        x = randint(0,2,N)
    
    E=np.zeros(N)
    T=np.zeros(N)
    
    for k in range(N):
        E[k]=x[k]*EL[k]+(1-x[k])*EC[k]
        T[k]=x[k]*TL[k]+(1-x[k])*TC[k]


    E_min=1e20
    
    
    T_min=1e20
    
    
    Xmin = []
    for j in range(number_of_generations):
        x = randint(0,2,N)
        if allOf(x,1) or allOf(x,0):
            x = randint(0,2,N)
        cut_point=randint(1,N)
        
        x = x[0:cut_point]
        x_2=randint(0,2,N-cut_point)
        x = np.append(x,x_2)
        
        rand_mut = np.random.rand()
        
        if rand_mut < mutation_probability:
            gene_position = randint(0,N,2)
            gene_position = np.sort(gene_position)
            
            a = x[gene_position[0]:gene_position[1]]
            
            fl = -np.sort(-a)
            
        for k in range(N):
            E[k] = x[k]*EL[k]+(1-x[k])*EC[k]
            T[k] = x[k]*TL[k]+(1-x[k])*TC[k]
        if sum(E) <= E_min and sum(T) < T_constraint:
            E_min=sum(E)
            E_min=sum(T)
            Xmin=x
    Decision_Matrix=Xmin
    return Decision_Matrix,E_min, T_min
    



# Programacion dinamica
def dynamicProg(tasks,N):
    iter1 = 50  # Numero de iteraciones
    E_min=1     # E_minimo
    T_constraint = 700  
    T_rate = 3e6  
    
    EC = []
    EL = []
    TL = []
    TC = []

    EL, EC, TL, TC , Cci = Cal_E_T7(T_rate, tasks, N)
    
    print EL
    print EC
    print TL
    print TC

    
    table1 = 2*np.ones((N,N))

    E = np.zeros((N,N))
    E_total = np.zeros(iter1)
    
    T = np.zeros((N,N))
    T_total = np.zeros(iter1)

    visited = np.zeros((N,N))
    table2={}

    Decision_Matrix = np.zeros(N)
    E1 = {}

    for iter in range(iter1):
        M = randint(0,2,N)
        if allOf(M,1) or allOf(M,0):
            M = randint(0,2,N)
        
        i=1
        j=1
        
        table1 = 2*np.ones((N,N))
        
        for k in range(N):
            if M[k] == 0:
                i+=1
                table1[i,j]=M[k]
            else:
                j+=1
                table1[i,j]=M[k]
            
            #M[k]=1
            if visited[i,j]==0:
                E[i,j] = M[k]*EL[k]+(1-M[k])*EC[k] 
                T[i,j] = M[k]*TL[k]+(1-M[k])*TC[k] 
                
                visited[i,j] = 1
                table2[i,j] = M[k]
                E1[k]=E[i,j]

                if E1[k] < 2e-7:
                    Decision_Matrix[k]=M[k]
            else:
                e= M[k]*EL[k]+(1-M[k])*EC[k] 
                t= M[k]*TL[k]+(1-M[k])*TC[k]
                 
                
                if E[i,j] > e:
                    E1[k]=e
                    Decision_Matrix[k]=M[k]
                    table2[i,j]=M[k]
                    E[i,j]=e
                    T[i,j]=t
                    
                elif E[i,j] == e:
                    if e < 2e-7:
                        Decision_Matrix[k]=M[k]
        E_total[iter]= np.sum(E)
        T_total[iter]= np.sum(T)
        
        if iter == iter1/3 and len(Decision_Matrix)==N:
            T_rate=5e6
            EL,EC,TL,TC,Cci = Cal_E_T7(T_rate,tasks,N)
        elif iter== 2*iter1/3 and len(Decision_Matrix)==N :
            T_rate=8e6
            EL,EC,TL,TC,Cci = Cal_E_T7(T_rate,tasks,N)

        if E_total[iter]<=E_min and T_total[iter] < T_constraint and  len(E1)==N:
            E_min=E_total[iter]
            T_min=T_total[iter]
            it=iter
    return Decision_Matrix, E_min, T_min
        
        
        



tasks = [5930,3900,1700,6880,6800,2400,5960
        ,5400,8700,900,800,900,5900,7700,6200]

N = len(tasks)

Decision_Matrix_Dynamic ,E_min, T_min = dynamicProg(tasks,N)
#Decision_Matrix_Dynamic,E_min, T_min = GA(tasks,N)

print Decision_Matrix_Dynamic 
print "Energia minima : " ,E_min
print "Tiempo mminimo : ", T_min
