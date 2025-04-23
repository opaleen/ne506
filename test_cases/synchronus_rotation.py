import sys
sys.path.append("../src/")

from main_model import *

def synchronus_rotation():

    arguments = parse_arguments()
    k_eff_target = arguments.k_eff_target


    k_eff = []
    angle = []

    for i in np.linspace(0, 20, 20):

        angle.append(i)
        model = generate_model([i]*12)
        run = model.run()

        k_eff.append(openmc.StatePoint(run).keff.nominal_value)
        print(f" keff = {k_eff[-1]:.6f}")
        if np.isclose(k_eff[-1], 1, atol=.001):
            break


    plt.plot(angle, k_eff)
    plt.show()


synchronus_rotation()
