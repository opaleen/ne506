import sys

sys.path.append("../src/")

from scipy.optimize import differential_evolution
import numpy as np
import geometry as geom
import csv
import os

from main_model import *


if __name__ == "__main__":

    k_eff = []
    angle = []
    k_eff_std = []
    for i in np.linspace(-90, 90, 20):
        # i am just gonna rotate the first control drum

        rotation_list = np.zeros(geom.number_of_control_drums)
        rotation_list[1] = i
        angle.append(i)
        model = generate_model(rotation_list)
        run = model.run()
        with openmc.StatePoint(run) as state_point:
            k_eff.append(state_point.keff)

    print(angle)
    print(k_eff)
