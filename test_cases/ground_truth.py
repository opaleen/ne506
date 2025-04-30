import sys

sys.path.append("../src/")

from scipy.optimize import differential_evolution
import numpy as np
import geometry as geom
import csv
import os

from main_model import *


model = generate_model(np.zeros(12))
model.run()
