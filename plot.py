#!/opt/homebrew/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt
import csv
import sys
import scipy.stats

from scipy.interpolate import interp1d

if __name__ == "__main__":
    filename = str(sys.argv[1])

    data = np.genfromtxt(f"data/{filename}.CSV", delimiter=",", usecols=range(2), skip_header=16)

    x = data.T[0,:]
    y = data.T[1,:]

    plt.plot(x, y)
    xx = np.linspace(np.min(x), np.max(x), 1000)
    plt.show()