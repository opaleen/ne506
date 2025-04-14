import openmc
import numpy as np
import scipy as sp

number_of_control_drums = 12
distance_of_control_drums_from_center = 86
to_radian = np.pi / 180
control_drum_theta = 80

# lower z plane
lower_z_plane = -15.24
upper_z_plane = 15.24
# control rod
control_rod_radius = 1.35
# heat pipe

heat_pipe_inner_radius = 1.18
stainless_steel_thickness = 0.17
heat_pipe_outer_radius = heat_pipe_inner_radius + stainless_steel_thickness

# fuel rod
helium_gas_gap_thickness = 0.04
cladding_thickness = 0.2

fuel_inner_radius = 1.26
fuel_gas_radius = fuel_inner_radius + helium_gas_gap_thickness
fuel_cladding_radius = fuel_gas_radius + cladding_thickness

# assembly
assembly_edge_length = 10.2653
assembly_pitch = (3.33,)

# control drum
inner_radius_control_drum = 5.5
control_drum_absorber_thickness = 2
outer_radius_of_control_drum = (
    inner_radius_control_drum + control_drum_absorber_thickness
)

# whole core
whole_core_diameter = 200
core_pitch = (0.336 * 100 * 0.844 / 1.6,)
core_radius = whole_core_diameter / 2
core_roof = 50.24
core_floor = -50.24


def plane_from_points(point1, point2):

    x1, y1 = point1
    x2, y2 = point2

    dx = x2 - x1
    dy = y2 - y1

    a = -dy / dx  # slope
    b = 1
    c = 0

    d = b * y1 + a * x1

    norm = np.sqrt(a**2 + b**2 + c**2)
    a, b, c, d = a / norm, b / norm, c / norm, d / norm

    return openmc.Plane(a, b, c, d)


def rotate_control_drum_cell(control_drum: openmc.Cell, angle):

    rotation_matrix = sp.spatial.transform.Rotation.from_euler(
        "z", angle, degrees=True
    ).as_matrix()

    control_drum.rotation = rotation_matrix

    return control_drum
