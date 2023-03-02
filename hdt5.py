# Universidad del Valle de Guatemala
# Algoritmos y Estructuras de Datos
# Seccion: 30
# Autor: Eunice Anahi Mata Ixcayau 
# Carnet: 21231
# Aux: Cristian no se apellido :P

import simpy, random, time, numpy as np

startingTimes = []
endingTimes = []
# procesos
class myProcess(object):
    
    def processs(env, name, ram_memory, memoryRequired, timeProcess, cantInstructions, cpu_velocity):
    
        #proceso de new
        yield env.timeout(timeProcess)
        startTime = env.now #time of start of process
        startingTimes.append(round(env.now, 6))
        format_time = "{:.6f}".format(timeProcess)
        print()
        print("[%s] [RAM] Starting time %s sec \n\tneeds to use %d of RAM memory\n\tfor %d instructions" % (name,format_time, memoryRequired,cantInstructions))
        #proceso de ready
        print("[%s] [RAM] \n\twill use %d of RAM memory" % (name,memoryRequired))
        yield ram_memory.get(memoryRequired) #takes ram memmory
        #proceso de running
        instructionsDone = 0
        while instructionsDone < cantInstructions:
            with cpu.request() as reqCPU:
                yield reqCPU
                executed = (cpu_velocity) if((cantInstructions - instructionsDone) >= cpu_velocity) else (cantInstructions - instructionsDone)
                print("[%s] [CPU] \n\tCPU runs # instructions:  %d" % (name, executed))
                
                yield env.timeout(1) 
                instructionsDone += executed
                
                print("[%s] [CPU]\n\tInstructions done: %d/%d" % (name,instructionsDone,cantInstructions))

            # proceso de waiting
            if(random.randint(1,2) == 1) and (instructionsDone < cantInstructions):
                print("[%s] waiting..." % (name))
                time.sleep(1)
            #else return to running AKA the while again

        #proceso running continuacion xd    
        yield ram_memory.put(memoryRequired) #returns ram memory
        endTime = env.now
        endingTimes.append(round(env.now, 6))
        format_time2 = "{:.6f}".format(timeProcess)        
        print("[%s] [RAM] Ending time %s sec \n\tRelease %d of RAM memory" % (name,format_time2, memoryRequired))
        print()

# mf random seed
random.seed(42)
# GLOBAL VARIABLES AND SO
env = simpy.Environment()
ram_memory = simpy.Container(env, init=100, capacity=100) #memoria ram
cpu = simpy.Resource(env, capacity=2)
TotalTime = 0
#Data that changes
velocityCPU = 3
cantProcess = int(input("Ingrese la cantidad de procesos a realizar\n"))
interval = int(input("Ingrese el intervalo\n"))
#calling and running process
for i in range(cantProcess):
  timeProcess = random.expovariate(1 / interval)
  memoryCant = random.randint(1,10)
  instructionsToDo = random.randint(1, 10)
  env.process(myProcess.processs(env, ("Process No." + str(i)), ram_memory, memoryCant, timeProcess, instructionsToDo, velocityCPU))

env.run()
averageTime = 0
listOfTimePP = []
for i in range (len(startingTimes)):
    listOfTimePP.append(round(endingTimes[i]-startingTimes[i],6))
    averageTime += (round(endingTimes[i]-startingTimes[i],6))

#avarage
print("-----------------------------------------------------")
print(" Avarage time is: " + str(averageTime/cantProcess) +" seconds ")
print("-----------------------------------------------------")
print(" Standar deviation is: " + str(np.std(listOfTimePP)) +" seconds ")
print("-----------------------------------------------------")
