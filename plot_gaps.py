#!/opt/homebrew/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt
import csv
import sys
import scipy.stats
import matplotlib

from scipy.interpolate import interp1d

def linfun(x, a):
    return a*x

if __name__ == "__main__":
    filenames = ["8cm_1", "8cm_2", "11cm_1", "14cm_1", "37cm", "47cm", "56cm"]
    d = [8, 8, 11, 14, 37, 47, 56]
    dt = []

    for filename in filenames:
        data = np.genfromtxt(f"output/{filename}_fit.csv", delimiter=",", usecols=range(3), skip_header=1)
        means = data.T[0,:]
        dt.append(np.median(np.diff(means)))
    
    with open(f'output/gaps.csv', 'w') as f:
        print("d,dt", file=f)
        for i in range(0, len(d)):
            print(f"{d[i]},{dt[i]}", file=f)
            print(f"{filenames[i]}:\n\td={d[i]}\n\tdt={dt[i]}\n")
    
    fitted_params,_ = scipy.optimize.curve_fit(linfun, dt, d, p0=[1])
    a = fitted_params[0]

    plt.plot(dt, d, 'o', label="Median Interpeak Distance")
    xx = np.linspace(np.min(dt), np.max(dt), 2)
    plt.plot(xx, a*xx, label="Best Fit Line (y=mx)")

    plt.xlabel('Interpeak Distance (s)')
    plt.ylabel('Distance Between Mirrors (cm)')

    plt.title('Interpeak Distance vs Distance Between Mirrors')

    plt.legend(loc="upper left")

    matplotlib.pyplot.gcf().set_size_inches(18.5, 10.5)

    plt.savefig("output/gaps.png")

    plt.show()