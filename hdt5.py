import simpy, random

# proceso

def myProcess(env, name, ram_memory, memoryRequired, time, cantInstructions, cpu_velocity):
    
    #NEW
    yield env.timeout(time)

    print("%s necesita %d de memoria RAM" % (name, memoryRequired))

    #READY
    yield ram_memory.get(memoryRequired)
    print("%s usara %d de memoria RAM" % (name,memoryRequired))

    instructions_ToDoReady = 0

    #RUNNING
    while instructions_ToDoReady < cantInstructions:
        with cpu.request() as req:
            yield req

            if(cantInstructions - instructions_ToDoReady) >= cpu_velocity:
                executed = cpu_velocity
            else:
                executed = cpu_velocity - instructions_ToDoReady
            print("%s - el cpu acaba de ejecutar %d instrucciones" % (name, executed))
            yield env.timeout(executed)
            instructions_ToDoReady += executed
            print("%s ejecuto %d instrucciones de %d" % (name,instructions_ToDoReady,cantInstructions))
        
        decision = random.randint(1,2)

        if(decision == 1) and (instructions_ToDoReady < cantInstructions):
            with __wait__.request() as req_1:
                yield req_1
                yield env.timeout(1)
        
    yield ram_memory.put(memoryRequired)
    print("Tiempo [%s] - %s - libero %d de ram" % (time, name, memoryRequired))

#proceso
velocityCPU = 1
process_c = 25
time_T = 0
time_list = []
#capacidad
env = simpy.Environment()
ram_memory = simpy.Container(env, init=100, capacity=100)
cpu = simpy.Resource(env, capacity=4)
__wait__ = simpy.Resource(env, capacity=2)

#INTERVALOS
intevalo = 1
#intervalo
for i in range(process_c):
  memory_size = random.randint(1,10)
  instructionsToDo = random.randint(1, 10)
  time = random.expovariate(1 / intevalo)
  
  env.process(myProcess(env, ("Program No." + str(i)), ram_memory, memory_size, time, instructionsToDo, velocityCPU))
  
env.run()