import simpy
import model
import statistics

exp = statistics.Experiment(2, {1: 15, 2: 12, 3: 7.5})
exp.run_experiment()