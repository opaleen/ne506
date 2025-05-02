import numpy as np


def scant_method(theta_current_step, theta_old_step, k_eff_current, k_eff_old):
    theta_new = (theta_current_step * k_eff_current - theta_old_step * k_eff_old) / (
        k_eff_current - k_eff_old
    )
    return theta_new


def oscillatory(arr):
    if len(arr) < 2:
        return False
    a, b = arr[0], arr[1]
    for i in range(len(arr)):
        if arr[i] != (a if i % 2 == 0 else b):
            return False
    return a != b

def feed_back_rotation(k_eff_diff, last_angle, last_direction, rotation_step, history, damping_factor=0.7):
    if oscillatory(history):
        rotation_step = max(0.1, rotation_step - 1/damping_factor)

    if abs(k_eff_diff) < 0.0005:
        return last_angle, last_direction, rotation_step

    if k_eff_diff > 0:
        new_direction = -last_direction
    else:
        new_direction = last_direction

    if k_eff_diff * last_direction > 0:
        new_step = rotation_step * damping_factor
    else:
        new_step = rotation_step / damping_factor

    new_angle = last_angle + (new_direction * new_step)
    return new_angle, new_direction, new_step
