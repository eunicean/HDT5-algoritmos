# Universidad del Valle de Guatemala
# Algoritmos y Estructuras de Datos
# Seccion: 30
# Autor: Eunice Anahi Mata Ixcayau 
# Carnet: 21231
# Aux: Cristian no se apellido :P

import simpy, random, time 

# procesos
class myProcess(object):
    def __init__(self,env):
       self.env = env
       self.instructionsDone = 0
       self.startTime = env.now
    
    def processs(env, name, ram_memory, memoryRequired, timeProcess, cantInstructions, cpu_velocity):
    
        #proceso de new
        yield env.timeout(timeProcess)
        startTime = env.now #time of start of process
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
                
                print(" [%s] [CPU] \n\tCPU runs # instructions:  %d" % (name, executed))
                
                yield env.timeout(executed/cpu_velocity) #cant of instructions left for cpu to do
                instructionsDone += executed
                
                print("[%s] [CPU]\n\tInstructions done: %d/%d" % (name,instructionsDone,cantInstructions))

            # proceso de waiting
            if(random.randint(1,2) == 1) and (instructionsDone < cantInstructions):
                time.sleep(1)
            #else return to running AKA the while again

        #proceso running continuacion xd    
        yield ram_memory.put(memoryRequired) #returns ram memory
        endTime = env.now
        format_time2 = "{:.6f}".format(timeProcess)        
        print("[%s] [RAM] Ending time %s sec \n\tRelease %d of RAM memory" % (name,format_time2, memoryRequired))
        print()
        global TotalTime
        TotalTime += (endTime - startTime) # total time minus the starting time

# mf random seed
random.seed(10)
# GLOBAL VARIABLES AND SO
env = simpy.Environment()
ram_memory = simpy.Container(env, init=100, capacity=100) #memoria ram
cpu = simpy.Resource(env, capacity=1)
TotalTime = 0
#Data that changes
velocityCPU = 3
cantProcess = 25
interval = 10
#calling and running process
for i in range(cantProcess):
  timeProcess = random.expovariate(1 / interval)
  memoryCant = random.randint(1,10)
  instructionsToDo = random.randint(1, 10)
  env.process(myProcess.processs(env, ("Process No." + str(i)), ram_memory, memoryCant, timeProcess, instructionsToDo, velocityCPU))

env.run()

#avarage
print("Avarage time is: " + str((TotalTime / cantProcess)) + " seconds")