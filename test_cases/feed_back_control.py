import sys
sys.path.append("../src/")
from main_model import *
from drum_rotation_algorithm import feed_back_rotation
import numpy as np
import csv
import os


evaluation_count = 0

def log_book(angle,k_eff,norm,filename):

    global evaluation_count
    evaluation_count += 1

    if not os.path.exists("results"):
        os.makedirs("results")

    filename = f"results/{filename}.csv"
    write_header = not os.path.exists(filename)

    with open(filename, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)

        if write_header:
            headers = (
                    ["step"]
                    + ["angle", "norm"]
            )
            writer.writerow(headers)

        row = (
                [evaluation_count, angle,k_eff,norm]
        )
        writer.writerow(row)


if __name__ == "__main__":

    arguments = parse_arguments()
    k_eff_target = arguments.k_eff_target
    number_of_iteration = 20

    k_eff = []
    angle = []

    rotation_angle = 0
    rotation_step = 10

    for i in range (number_of_iteration):

        angle.append(rotation_angle)
        model = generate_model([rotation_angle] * 12)
        run = model.run()

        k_eff_current = openmc.StatePoint(run).keff.nominal_value
        k_eff.append(k_eff_current)
        k_eff_diff = k_eff_current - k_eff_target

        log_book(rotation_angle,k_eff_current,abs(k_eff_diff),filename = "feed_back_iteration") #should track the data now

        rotation_angle = feed_back_rotation(k_eff_diff,
                                            last_rotation_angle = angle [-1],
                                            rotation_step = rotation_step)

        if rotation_angle in angle:

            rotation_angle = ratation_anlge*np.random.rand()


        if np.isclose(k_eff[-1], 1, atol=0.001):
            print("you good a good (!) result. Do the next problem ")
            break

    print (f"k_eff ={k_eff} ")
    print (f"angle ={angle}")