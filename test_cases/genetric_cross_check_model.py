import sys

sys.path.append("../src/")
from main_model import *

if __name__ == "__main__":

    angle = [
        -1.371714686,
        64.06917014,
        -17.23011365,
        -14.9609442,
        -69.72462107,
        23.82573943,
        -79.19105094,
        -29.60914295,
        -70.51408575,
        61.87619544,
        -3.805245732,
        -20.70025735,
    ]
    model = generate_model(angle)
    model.run()
