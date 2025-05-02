import sys
import numpy as np
import csv
import os
import openmc
sys.path.append("../src/")

from main_model import generate_model, parse_arguments
from drum_rotation_algorithm import feed_back_rotation

evaluation_count = 0

def log_book(angle, k_eff, norm, filename):
    global evaluation_count
    evaluation_count += 1

    os.makedirs("results", exist_ok=True)
    filepath = f"results/{filename}.csv"
    write_header = not os.path.exists(filepath)

    with open(filepath, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if write_header:
            writer.writerow(["step", "angle", "k_eff", "norm"])
        writer.writerow([evaluation_count, angle, k_eff, norm])

def main():
    args = parse_arguments()
    k_eff_target = args.k_eff_target
    max_iterations = 20
    rotation_step = 5.0
    last_direction = -1
    rotation_angle = 0 #initial
    angles = []
    k_effs = []

    for i in range(max_iterations):

        model = generate_model(rotation_angle)
        run = model.run(output=False)

        current_k_eff = openmc.StatePoint(run).keff.nominal_value
        k_eff_diff =   k_eff_target -current_k_eff
        k_effs.append(current_k_eff)
        angles.append(rotation_angle)
        log_book(rotation_angle, current_k_eff, abs(k_eff_diff), "feed_back_iteration")

        rotation_angle, last_direction , rotation_step = feed_back_rotation(
            k_eff_diff,
            rotation_angle,
            last_direction,
            rotation_step,
            history = angles
        )

        if np.isclose(current_k_eff, k_eff_target, atol=0.0009):
            print(f"Converged at iteration {i+1}")
            print(f"Iteration {i+1}: k_eff={current_k_eff:.6f}, angle={angles[-1]:.6f}")
            break

        print(f"Iteration {i+1}: k_eff={current_k_eff:.6f}, angle={angles[-1]:.6f}")

if __name__ == "__main__":
    main()