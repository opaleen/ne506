import sys
sys.path.append("../src/")

from scipy.optimize import differential_evolution
import numpy as np
import geometry as geom
from main_model import *


def simulate_model(drum_rotation_angle_list,):

    arguments = parse_arguments()
    k_eff_target = arguments.k_eff_target

    model = generate_model(drum_rotation_angle_list)
    run = model.run(output = False )

    return np.abs (k_eff_target - openmc.StatePoint(run).keff.nominal_value)
def genetic_optimization():

    initial_rotation_angle_list = np.zeros(geom.number_of_control_drums)
    result = differential_evolution(simulate_model,bounds=[[-9,9]]*geom.number_of_control_drums)
    print (result)

genetic_optimization()
