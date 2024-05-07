#!/opt/homebrew/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt
import csv
import sys
import scipy.stats
import matplotlib

from scipy.interpolate import interp1d

if __name__ == "__main__":
    filenames = ["8cm_1", "8cm_2", "11cm_1", "14cm_1", "37cm", "47cm", "56cm"]
    com_filenames = ["com_laser1", "com_laser2", "com_laser3"]
    colors = ["g", "r", "b"]
    linestyles = ["-", "-", "--"]

    d = [32, 32, 35, 38, 37, 47, 56]
    dt = []

    com_dt = []

    for filename in filenames:
        data = np.genfromtxt(f"output/{filename}_fit.csv", delimiter=",", usecols=range(3), skip_header=1)
        means = data.T[0,:]
        dt.append(np.median(np.diff(means)))
    
    for filename in com_filenames:
        data = np.genfromtxt(f"output/{filename}_fit.csv", delimiter=",", usecols=range(3), skip_header=1)
        means = data.T[0,:]
        com_dt.append(np.median(np.diff(means)))
    
    with open(f'output/gaps.csv', 'w') as f:
        print("d,dt", file=f)
        for i in range(0, len(d)):
            print(f"{d[i]},{dt[i]}", file=f)
            print(f"{filenames[i]}:\n\td={d[i]}\n\tdt={dt[i]}\n")



    plt.plot(d, dt, 'o', label="Interpeak Distance")

    for i in range(0, len(com_dt)):
        plt.axhline(y=com_dt[i], linestyle=linestyles[i], color=colors[i], label=f"Commercial Laser Interpeak Distance ({com_filenames[i]})")

    plt.ylabel('Median Interpeak Distance (s)')
    plt.xlabel('Distance Between Mirrors (cm)')

    plt.title('Distance Between Mirrors vs Median Interpeak Distance')

    plt.legend(loc="upper right")

    matplotlib.pyplot.gcf().set_size_inches(18.5, 10.5)

    plt.savefig("output/gaps.png")

    plt.show()