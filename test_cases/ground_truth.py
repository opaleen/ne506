import sys

sys.path.append("../src/")
from main_model import *

if __name__ == "__main__":

    model = generate_model(np.zeros(12))
    model.run()
