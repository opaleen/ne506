import numpy as np


def scant_method(theta_current_step, theta_old_step, k_eff_current, k_eff_old):
    theta_new = (theta_current_step * k_eff_current - theta_old_step * k_eff_old) / (
        k_eff_current - k_eff_old
    )
    return theta_new


def feed_back_rotation(
        k_eff_diff,
        last_rotation_angle,
        last_rotation_direction,
        rotation_step,
        min_step=0.1,
        max_step=5.0,
        sensitivity=1.0,
        damping_factor=0.9
):
    adjusted_step = rotation_step * (1 + sensitivity * abs(k_eff_diff))
    adjusted_step = max(min_step, min(max_step, adjusted_step))
    adjusted_step *= damping_factor

    if k_eff_diff * last_rotation_direction < 0:
        new_direction = last_rotation_direction
    else:
        new_direction = -last_rotation_direction

    new_rotation_angle = last_rotation_angle + (adjusted_step * new_direction)

    return new_rotation_angle, new_direction
