import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np

def show_grid(arr, sweep_signal):
    """
    Plot 2 out of 3 dimensions of a Grid as an image with a slider to move along third dimension
    
    Parameters
    ----------
    arr : array_like
        A 3d array consisting of (Ix, Iy, E) or (qx, qy, E) data.

    Returns
    -------
    ?
    """
    default_energy_index = arr.shape[-1] // 2
    emin = 0
    emax = arr.shape[-1] -1 

    fig, ax = plt.subplots()
    ax_energy_ind = fig.add_axes([0.25, 0.10, 0.65, 0.03])
    s_energy_ind = Slider(ax_energy_ind, 'Energy index', emin, emax, valinit=default_energy_index)

    im = ax.imshow(arr[:, :, s_energy_ind.val])

    def update(val):
        im.set_data(arr[:, :, int(s_energy_ind.val)])
        im.autoscale()

        s_energy_ind.valtext.set_text('{:.2f}'.format(sweep_signal[int(s_energy_ind.val)] * 1000))

    s_energy_ind.on_changed(update)
    plt.show()

    return fig, ax, im , s_energy_ind