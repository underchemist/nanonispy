def show_grid(arr, sweep_signal):
    """
    Plot 2 out of 3 dimensions of a Grid as an image with a slider to move along third dimension.
    Should be used with an interactive backend, only tested with qt5 backend so mileage my vary.

    *warning*
    Depending on the OS, because we are manipulating and handling large numpy arrays in memory 
    python doesn't always properly free the memory, even if if you shut down your ipython kernel/script.
    Hence you may need to keep an eye on your memory consumption and force quit the process if it
    isn't freed after your analysis.
    
    Parameters
    ----------
    arr : array_like
        A 3d array consisting of (Ix, Iy, E) or (qx, qy, E) data.
    sweep_signal : array_like
        A 1d array consiting of the bias values or other relevant spectroscopic sweep parameter.
        For example can be passed from Grid.signals['sweep_signal'].


    Returns
    -------
    fig : matplotlib.figure.Figure
        Figure handle.
    ax : matplotlib.axes._subplots.AxesSubplot
        Axes handle for image.
    s_ax : matplotlib.axes._axes.Axes
        Axes handle for slider widget.
    im : matplotlib.image.AxesImage
        Image handle.
    s_energy_ind : matplotlib.widgets.Slider
        Slider handle for slider widget
    """
    import matplotlib.pyplot as plt
    from matplotlib.widgets import Slider
    import numpy as np
    
    # starting + min/max values for slider
    default_energy_index = arr.shape[-1] // 2
    energy_min = 0
    energy_max = arr.shape[-1] -1 

    fig, ax = plt.subplots()
    ax.set_position([0.125, 0.175, 0.80, 0.80])
    s_ax = fig.add_axes([0.2, 0.10, 0.65, 0.03]) # axis for slider
    s_energy_ind = Slider(s_ax, 'Energy', energy_min, energy_max, valinit=default_energy_index)

    im = ax.imshow(arr[:, :, int(s_energy_ind.val)])
    s_energy_ind.valtext.set_text('{:.2f} mV\n{}/{} index'.format(
        sweep_signal[int(s_energy_ind.val)] * 1000, 
        int(s_energy_ind.val), 
        arr.shape[-1]-1))

    def update(val):
        im.set_data(arr[:, :, int(s_energy_ind.val)])
        im.autoscale()

        s_energy_ind.valtext.set_text('{:.2f} mV\n{}/{} index'.format(
            sweep_signal[int(s_energy_ind.val)] * 1000, 
            int(s_energy_ind.val), 
            arr.shape[-1]-1))

    s_energy_ind.on_changed(update)
    plt.show()

    return fig, ax, s_ax, im, s_energy_ind

def fft(arr, axes=[0, 1]):
    """
    Compute the 2d fft of an array. The fft is calculated across the first two (spatial)
    dimensions, for each slice of energy. Applies a frequency shift to center low q vector
    values in middle of array.

    Parameters
    ----------
    arr : array_like
        A 3d array consisting of (Ix, Iy, E) data. 
    """
    import numpy as np

    # complex valued array of same shape as arr
    fft_arr = np.fft.fft2(arr, axes=axes)

    fft_shifted_arr = np.fft.fftshift(fft_arr, axes=axes)

    return fft_shifted_arr
