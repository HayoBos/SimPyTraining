import pandas as pd
import numpy as np
import model


class Experiment:
    def __init__(self, lanes, price_per_program):
        self.carwash = model.CarWash(lanes=lanes, price_per_program=price_per_program)

    def run_experiment(self):
        self.carwash.run()
        mean = np.mean([self.carwash.queue.memory[i][1] for i in range(len(self.carwash.queue.memory))])
        stdev = np.std([self.carwash.queue.memory[i][1] for i in range(len(self.carwash.queue.memory))])
        print("The mean queue length is " + str(mean) + " stdev is " + str(stdev))
        print("Simulated days: " + str(self.carwash.day_counter))

