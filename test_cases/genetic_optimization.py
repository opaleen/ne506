import sys
sys.path.append("../src/")

from scipy.optimize import differential_evolution
import numpy as np
import geometry as geom
import csv
import os

from main_model import *

evaluation_count = 0

def log_book(angles, k_eff,k_eff_target):

    global evaluation_count
    evaluation_count += 1

    if not os.path.exists('results'):
        os.makedirs('results')

    filename = f'results/drum_optimization.csv'

    write_header = not os.path.exists(filename)

    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)

        if write_header:
            headers = ['evaluation'] + [f'drum_{i+1}_angle' for i in range(geom.number_of_control_drums)] + ['k_eff', 'abs_diff']
            writer.writerow(headers)

        row = [evaluation_count] + list(angles) + [k_eff.nominal_value, abs(k_eff.nominal_value - k_eff_target)]
        writer.writerow(row)

def simulate_model(drum_rotation_angle_list,):
    arguments = parse_arguments()
    k_eff_target = arguments.k_eff_target

    model = generate_model(drum_rotation_angle_list)
    run = model.run(output=False)
    state_point = openmc.StatePoint(run)
    current_k_eff = state_point.keff
    state_point.close()

    log_book(drum_rotation_angle_list, current_k_eff,k_eff_target)

    print(f"Norm = {np.abs(k_eff_target - current_k_eff.nominal_value):.6f}")
    if np.abs(k_eff_target - current_k_eff.nominal_value)<0.01:
        return
    return np.abs(k_eff_target - current_k_eff.nominal_value)

def genetic_optimization():
    initial_rotation_angle_list = np.zeros(geom.number_of_control_drums)
    result = differential_evolution(
        simulate_model,
        bounds=[[-90, 90]] * geom.number_of_control_drums,
        workers=1
    )
    print(result)

    if result.success:

        print("\nOptimization successful!")
        print(f"Optimal angles: {result.x}")
        print(f"Final k_eff difference: {result.fun}")

        model = generate_model(result.x)
        run = model.run(output=False)
        final_k_eff = openmc.StatePoint(run).keff
        openmc.StatePoint(run).close()
        log_parameters(result.x, final_k_eff)

if __name__ == "__main__":
    genetic_optimization()
