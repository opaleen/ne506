import numpy as np


def scant_method(theta_current_step, theta_old_step, k_eff_current, k_eff_old):
    theta_new = (theta_current_step * k_eff_current - theta_old_step * k_eff_old) / (k_eff_current - k_eff_old)
    return theta_new


def iterative_method(k_eff_current, k_eff_old, rotation_angle, rotation_step):
    if np.isclose(k_eff_current, 1, atol=0.01):
        rotation_angle = 0
    elif k_eff_current - k_eff_old > 0:
        rotation_angle -= rotation_step

    else:
        rotation_angle += rotation_step

    return rotation_angle
