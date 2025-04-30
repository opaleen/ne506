import sys

import numpy as np

sys.path.append("../src/")
from main_model import *
import openmc
import geometry as geom

if __name__ == "__main__":

    openmc.search_for_keff(
        generate_model,
        bracket=[-60, 60],
        print_iterations=True,
        tol=0.001,
        run_args={"output": False},
    )
