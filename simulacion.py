import random
import simpy

# Parámetros de la simulación
INTERVAL = 10
RANDSEED = 42
RAMCAP = 100
CPUSPED = 1
PROCESSNUMBER = 25

# Semilla para la generación de números aleatorios
random.seed(RANDSEED)

# Definición de la clase Proceso
class Proceso:
    def __init__(self, env, nombre, ram, cpu):
        self.env = env
        self.nombre = nombre
        self.ram = ram
        self.cpu = cpu
        self.instrucciones = random.randint(1, 10)
        # Inicia el proceso de ejecución
        self.accion = env.process(self.ejecutar())

    def ejecutar(self):
        # Espera un tiempo aleatorio antes de iniciar
        yield self.env.timeout(random.expovariate(1.0 / INTERVAL))
        # Imprime mensaje de nuevo proceso
        print("\033[1;33m" + f">>{self.env.now:.2f}: {self.nombre} - new..." + "\033[0m")

        # Solicita RAM
        yield self.ram.get(random.randint(1, 10))

        # Imprime mensaje de proceso listo
        print("\033[1;32m" + f">>{self.env.now:.2f}: {self.nombre} - ready..." + "\033[0m")
        with self.cpu.request() as req:
            yield req
            while self.instrucciones > 0:
                # Imprime mensaje de proceso corriendo
                print("\033[1;36m" + f">>{self.env.now:.2f}: {self.nombre} - running..." + "\033[0m")
                yield self.env.timeout(1 / CPUSPED)
                self.instrucciones -= 3
                if self.instrucciones <= 0:
                    break
                # Genera una elección aleatoria
                eleccion = random.randint(1, 21)
                if eleccion == 1:
                    # Si la elección es 1, espera un tiempo
                    print("\033[1;31m" + f">>{self.env.now:.2f}: {self.nombre} - waiting..." + "\033[0m")
                    yield self.env.timeout(1)
                    print("\033[1;32m" + f">>{self.env.now:.2f}: {self.nombre} - ready... (waiting...)" + "\033[0m")
                elif eleccion == 2:
                    # Si la elección es 2, continúa corriendo
                    print("\033[1;32m" + f">>{self.env.now:.2f}: {self.nombre} - ready... (running...)" + "\033[0m")
                else:
                    pass
        # Libera el RAM
        yield self.ram.put(random.randint(1, 10))
        # Imprime mensaje de proceso terminado
        print("\033[1;33m" + f">>{self.env.now:.2f}: {self.nombre} - process terminated" + "\033[0m")

# Función para configurar la simulación
def configurar(env, NUMPROCESOS, ram, cpu):
    for num in range(NUMPROCESOS):
        # Crea y activa un nuevo proceso
        p = Proceso(env, f"Proceso {num+1}", ram, cpu)
        yield env.timeout(0.1)

# Configuración de la simulación
env = simpy.Environment()
ram = simpy.Container(env, init=RAMCAP, capacity=RAMCAP)
cpu = simpy.Resource(env, capacity=1)

# Inicia la simulación
env.process(configurar(env, PROCESSNUMBER, ram, cpu))
env.run()
