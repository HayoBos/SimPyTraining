import random

import numpy as np
import simpy

from structure import Queue
from simpy import *
import statistics

class CarWash:
    def __init__(self, lanes, price_per_program):
        self.env = Environment()
        self.lanes = lanes
        self.price_per_program = price_per_program
        self.washtimes_per_program = {1: 15, 2: 12, 3: 10}
        self.queue = Queue()
        self.lanes = simpy.Resource(self.env, lanes)
        self.state = 0
        self.day_counter = 0

    def clean_car(self):
        req_machine = self.lanes.request()
        yield req_machine
        car_to_clean = self.queue.get(self.env.now)
        yield self.env.timeout(self.washtimes_per_program[car_to_clean["program"]])
        self.lanes.release(req_machine)
        # print(str("Cleaned a " + car_to_clean["color"] + " " + car_to_clean["brand"] + " with program " + str(car_to_clean["program"])))

    def car(self):
        brand = random.choice(["Peugeot", "Audi", "Volvo", "Mercedes"])
        color = random.choice(["Blue", "Green", "Black", "White"])
        state = random.choice([1, 2, 3])
        state_program_map = {1: 3, 2: 2, 3: 1}
        program = state_program_map[state]
        # print(str("A " + color + " " + brand + " entered the queue at time " + str(self.env.now) + " and requested program " + str(state_program_map[state])))
        self.queue.insert({
            "brand": brand,
            "color": color,
            "state": state,
            "program": program
        }, self.env.now)
        yield self.env.process(self.clean_car())

    def source_cars(self):
        while True:
            yield self.env.timeout(random.expovariate(1/9))
            if self.state:
                print("A car arrives")
                self.env.process(self.car())

    def open_close(self):
        while True:
            yield self.env.timeout(60 * 8.5 + 1440 * self.day_counter - self.env.now)
            self.state = 1
            print("The Carwash has opened")
            opening_time = self.env.now
            yield self.env.timeout(60 * 9 + opening_time - self.env.now)
            print("The Carwash has closed")
            # self.queue.df.drop(self.queue.df.index, inplace=True)
            self.state = 0
            closing_time = self.env.now
            yield self.env.timeout(60 * 6.5 + closing_time - self.env.now)
            self.day_counter += 1
            print("A new day has started")

    def run(self):
        self.env.process(self.open_close())
        self.env.process(self.source_cars())
        self.env.run(1440 * 28)