#!/opt/homebrew/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import scipy.optimize as opt
import csv
import sys
import scipy.stats

from scipy.interpolate import interp1d


labels = {"8cm_1": "d=32cm (1)", "8cm_2": "d=32cm (2)", "11cm_1": "d=35cm", "14cm_1": "d=38cm", "37cm": "d=37cm", "47cm": "d=47cm", "56cm": "d=56cm", "com_laser1": "Commercial Laser (1)", "com_laser2": "Commercial Laser (2)", "com_laser3": "Commercial Laser (3)"}

def k_norm(num_peaks: int, x, *args):
    assert len(args) == 3*num_peaks+1

    m = args[0:num_peaks]
    s = args[num_peaks:2*num_peaks]
    k = args[2*num_peaks:3*num_peaks]

    ret = k[0]*scipy.stats.norm.pdf(x, loc=m[0] ,scale=s[0])

    for i in range(1, num_peaks):
        ret += k[i]*scipy.stats.norm.pdf(x, loc=m[i] ,scale=s[i])

    return ret + args[-1]

if __name__ == "__main__":
    filename = str(sys.argv[1])
    
    data = np.genfromtxt(f"data/{filename}.CSV", delimiter=",", usecols=range(2), skip_header=16)

    num_peaks = 0
    est = []
    with open(f"estimates/{filename}.txt", 'r') as f:
        line = f.readline().split(" ")
        num_peaks = int(line[0])
        est = [float(x) for x in line[1:]]
    

    x = data.T[0,:]
    y = data.T[1,:]

    # Initial guess for the parameters

    t0 = x[0]
    tf = x[-1]

    Dt = tf - t0

    step = Dt/(num_peaks+1)

    scale = max(y)

    leeway = 0.0005

    params = []
    bnds = ([],[])
    for i in range(num_peaks):
        params.append(est[i])
        bnds[0].append(est[i]-leeway)
        bnds[1].append(est[i]+leeway)
    for i in range(num_peaks):
        params.append(step/8)
        bnds[0].append(0)
        bnds[1].append(Dt/num_peaks/4)

    for i in range(num_peaks):
        params.append(scale)
        bnds[0].append(0)
        bnds[1].append(2*scale)

    params.append(scale/20)
    bnds[0].append(0)
    bnds[1].append(scale/10)

    # Optimizing curve fit
        
    func = lambda x, *args: k_norm(num_peaks, x, *args)

    fitted_params,_ = scipy.optimize.curve_fit(func, x, y, p0=params, maxfev=1000000, bounds=bnds)

    m = fitted_params[0:num_peaks]

    with open(f'output/{filename}_fit.csv', 'w') as f:
        print("mean,sigma,scale", file=f)
        for i in range(0, num_peaks):
            print(f"{fitted_params[i]},{fitted_params[num_peaks+i]},{fitted_params[2*num_peaks+i]}", file=f)
            print(f"Peak {i}:\n\tmean={fitted_params[i]}\n\tsigma={fitted_params[num_peaks+i]}\n\tscale={fitted_params[2*num_peaks+i]}\n")

        print(f"Constant offset: {fitted_params[-1]}")

    plt.plot(x, y, 'o', label="Data")
    xx = np.linspace(np.min(x), np.max(x), 1000)
    plt.plot(xx, func(xx, *fitted_params), label="Best Fit Sum of Gaussians")

    plt.xlabel('Time (s)')
    plt.ylabel('Reading (Volts)')

    plt.title(f'Fabry-Perot Interferometer Data and Fit: {labels[filename]}')

    plt.legend(loc="upper left")

    matplotlib.pyplot.gcf().set_size_inches(18.5, 10.5)

    plt.savefig(f"output/{filename}_fit.png")
    plt.show()