## Explanation of how to use this code

* Raw data are stored in the data/ folder
* First, peaks are visually estimated by running `plot.py`, i.e. `./plot.py 8cm_1`. These were manually entered into a corresponding `txt` file in the estimates/ folder
* Then, `fit_curve.py` computes the optimal sum-of-Gaussians fit starting at the visual estimate. The plots and graphs are stored in the output/ folder
* Finally, we compute the median of the interpeak distances for each reading and plot these as a function of the distance between mirrors. This final result is stored in `gaps.csv` and graphed in `gaps.png`.