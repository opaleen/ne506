import numpy as np


def scant_method(theta_current_step, theta_old_step, k_eff_current, k_eff_old):
    theta_new = (theta_current_step * k_eff_current - theta_old_step * k_eff_old) / (
        k_eff_current - k_eff_old
    )
    return theta_new


def  feed_back_rotation(k_eff_diff,
                        last_rotation_angle,
                        rotation_step ):
    if k_eff_diff > 0:
        last_rotation_angle -= rotation_step
    else:
        last_rotation_angle += rotation_step

    return last_rotation_angle
