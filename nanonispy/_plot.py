import matplotlib as mpl
import matplotlib.pyplot as plt

class Plotter:
    def __init__(self, data):
        self.data = data
        self.fig, self.ax = plt.subplots()
        self.handles = [self.fig, self.ax]

    def _plot():
        pass