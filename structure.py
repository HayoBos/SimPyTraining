from simpy import *
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
pd.options.mode.chained_assignment = None

class Queue:

    def __init__(self):
       self.df = pd.DataFrame()
       self.memory = []

    def fifo_sort(self):
        self.df = self.df.sort_values(
            by="start", ascending=True).reset_index(drop=True)

    def insert(self, task, time):
        self.df = self.df.append(task, ignore_index=True)
        self.memory += [[time, len(self.df.index)]]

    def get(self, time):
        data = self.df.to_dict('records')[0]
        self.df.drop(
            index=self.df.index[0],
            axis=0,
            inplace=True)
        self.memory += [[time, len(self.df.index)]]
        return data
