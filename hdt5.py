import simpy, random

# procesos
class myProcess(object):
    def __init__(self,env):
       self.env = env
       self.instructionsDone = 0
       self.startTime = env.now
    
    def processs(env, name, ram_memory, memoryRequired, time, cantInstructions, cpu_velocity):
    
        #proceso de new
        yield env.timeout(time)
        startTime = env.now #time of start of process
        format_time = "{:.6f}".format(time)
        print("[%s] [RAM] At %s sec \n\tneeds use %d of RAM memory" % (name,format_time, memoryRequired))

        #proceso de ready
        print("[%s] [RAM] \n\t will use %d of RAM memory" % (name,memoryRequired))
        yield ram_memory.get(memoryRequired) #takes ram

        #proceso de running
        instructionsDone = 0
        while instructionsDone < cantInstructions:
            with cpu.request() as req:
                yield req

                if(cantInstructions - instructionsDone) >= cpu_velocity:
                    executed = cpu_velocity
                else:
                    executed = cantInstructions - instructionsDone
                
                print("[%s] [CPU] \n\t CPU runs # instructions:  %d" % (name, executed))
                
                yield env.timeout(executed/cpu_velocity)
                instructionsDone += executed
                
                print("[%s] [CPU]\n\tInstructions done: %d/%d" % (name,instructionsDone,cantInstructions))
            
            decision = random.randint(1,2)

            if(decision == 1) and (instructionsDone < cantInstructions):
                with __wait__.request() as requesWait:
                    yield requesWait
                    yield env.timeout(1)
            #else return to running AKA the while again
            
        yield ram_memory.put(memoryRequired) #returns ram
        format_time2 = "{:.6f}".format(time)
        print("[%s] [RAM] At %s sec \n\tRelease %d of RAM memory" % (name,format_time2, memoryRequired))

        global ListOfTimes 
        global TotalTime 
        ListOfTimes.append((env.now - startTime)) # list of times per process
        TotalTime += (env.now - startTime) # total time minus the starting time


env = simpy.Environment()
ram_memory = simpy.Container(env, init=100, capacity=100) #memoria ram
cpu = simpy.Resource(env, capacity=4)
__wait__ = simpy.Resource(env, capacity=2)


velocityCPU = 1
cantProcess = 25
TotalTime = 0
ListOfTimes = []

#intervals
intevalo = 1

#calling and running process
for i in range(cantProcess):
  memoryCant = random.randint(1,10)
  instructionsToDo = random.randint(1, 10)
  time = random.expovariate(1 / intevalo)
  env.process(myProcess.processs(env, ("Program No." + str(i)), ram_memory, memoryCant, time, instructionsToDo, velocityCPU))

env.run()

#avarage
print()
print("Avarage time is: " + str((TotalTime / cantProcess)) + " seconds")