import matplotlib as mpl
import matplotlib.pyplot as plt

class NanonisPlotter:
    def __init__(self, NanonisFileHandle):
        self._ncls = NanonisFileHandle

    def __call__(self, signal, ):
        return self.plot(signal)

    def plot(self, signal, **kwargs):
        """
        Return appropriate plotting method.
        """
        ndim = len(self._ncls.signals[signal].shape)
        if ndim == 3:  # grid?
            
    def plot_scan(self):
        pass

    def plot_grid_slice(self):
        pass

    def plot_grid_interactice(self):
        pass

    def plot_dat(self):
        pass

    # def plot_grid(self, energy_index=None, **kwargs):
    #     """
    #     Plot slice of grid at specified index.

    #     Parameters
    #     ----------
    #     energy_index : int
    #     """
    #     fig, ax =plt.subplots()

    #     # generate real space values
    #     size_x, size_y = self._ncls.header['size_xy'] # units of m
    #     # convert to nm
    #     size_x *= 10e9
    #     size_y *= 10e9
    #     extent = [0, size_x, 0, size_y]

    #     if not energy_index:
    #         # if no index specified select index value that is half of sweep_signal length
    #         energy_index = len(self._ncls.signals['sweep_signal']) // 2

    #     signal = self._
    #     im = ax.imshow()

