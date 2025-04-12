"""
This model of Heat Pipe Mirco Reactor is developed by
Ebny Walid Ahammed and Oliver Paleen.
©  All rights reserved
"""
import openmc
import matplotlib.pyplot as plt
import numpy as np
import warnings

warnings.filterwarnings("ignore")


from materials import *
import geometry as geom
from settings import *


sodium = make_material(material_dict["sodium"], percent_type="ao")
uranium_15 = make_material(material_dict["uranium_15_percent"], percent_type="ao")
uranium_19 = make_material(material_dict["uranium_19_percent"], percent_type="ao")
uranium_12 = make_material(material_dict["uranium_12_percent"], percent_type="ao")
graphite = make_material(material_dict["graphite"], percent_type="ao")
stainless_steel = make_material(material_dict["stainless_steel"], percent_type="ao")
zircalloy = make_material(material_dict["zircalloy"], percent_type="ao")
helium = make_material(material_dict["helium"], percent_type="ao")
beryllium = make_material(material_dict["beryllium"], percent_type="ao")
boron_carbide = make_material(material_dict["boron_carbide"], percent_type="ao")


materials = openmc.Materials(
    [
        sodium,
        uranium_12,
        uranium_15,
        uranium_19,
        graphite,
        stainless_steel,
        zircalloy,
        helium,
        beryllium,
        boron_carbide,
    ]
)

floor_z_plane = openmc.ZPlane(z0=geom.lower_z_plane)
roof_z_plane = openmc.ZPlane(z0=geom.upper_z_plane)


fuel_or = openmc.ZCylinder(r=geom.fuel_inner_radius)
clad_ir = openmc.ZCylinder(r=geom.fuel_gas_radius)
clad_or = openmc.ZCylinder(r=geom.fuel_cladding_radius)


heat_pipe_ir = openmc.ZCylinder(r=geom.heat_pipe_inner_radius)
heat_pipe_or = openmc.ZCylinder(r=geom.heat_pipe_outer_radius)


control_drum_outer_cylinder = openmc.ZCylinder(r=geom.outer_radius_of_control_drum)
control_drum_inner_cylinder = openmc.ZCylinder(r=geom.inner_radius_control_drum)

first_plane = openmc.Plane(
    a=np.cos(geom.control_drum_theta), b=np.sin(geom.control_drum_theta)
)
second_plane = openmc.Plane(
    a=np.cos(geom.control_drum_theta), b=-np.sin(geom.control_drum_theta)
)
thrid_plane = openmc.YPlane(0)


heat_pipe_graphite_cell = openmc.Cell(fill=graphite, region=+heat_pipe_or)
heat_pipe_steel_cell = openmc.Cell(
    region=-heat_pipe_or & +heat_pipe_ir,
    fill=stainless_steel,
)

heat_pipe_fluid_cell = openmc.Cell(region=-heat_pipe_ir, fill=sodium)


fuel_12 = openmc.Cell(fill=uranium_12, region=-fuel_or)
fuel_15 = openmc.Cell(fill=uranium_15, region=-fuel_or)
fuel_19 = openmc.Cell(fill=uranium_19, region=-fuel_or)


core_cylinder = openmc.ZCylinder(r=geom.core_radius, boundary_type="vacuum")
core_roof = openmc.ZPlane(z0=geom.core_roof, boundary_type="vacuum")
core_floor = openmc.ZPlane(z0=geom.core_floor, boundary_type="vacuum")

control_rod_cylinder = openmc.ZCylinder(r=geom.control_rod_radius)


control_rod_graphite_cell = openmc.Cell(fill=graphite, region=+control_rod_cylinder)

control_rod_cell = openmc.Cell(region=-control_rod_cylinder, fill=boron_carbide)


graphite_cell = openmc.Cell(fill=graphite)
beryllium_cell = openmc.Cell(fill=beryllium)

control_rod = openmc.Universe(cells=[control_rod_cell, control_rod_graphite_cell])

heat_pipe = openmc.Universe(
    cells=[heat_pipe_fluid_cell, heat_pipe_steel_cell, heat_pipe_graphite_cell]
)


control_drum_inner_reflector_cell = openmc.Cell(
    region=-control_drum_inner_cylinder
    | (
        +control_drum_inner_cylinder
        & -control_drum_outer_cylinder
        & -first_plane
        & +second_plane
        & +thrid_plane
    ),
    fill=beryllium,
)
control_drum_absorber_cell = openmc.Cell(
    region=(
        (+control_drum_inner_cylinder & -control_drum_outer_cylinder)
        & ~(
            +control_drum_inner_cylinder
            & -control_drum_outer_cylinder
            & -first_plane
            & +second_plane
            & +thrid_plane
        )
    ),
    fill=boron_carbide,
)

control_drum__outer_reflector_cell = openmc.Cell(
    region=+control_drum_outer_cylinder, fill=beryllium
)

control_drum_universe = openmc.Universe(
    cells=[
        control_drum_absorber_cell,
        control_drum_inner_reflector_cell,
        control_drum__outer_reflector_cell,
    ]
)

graphite_universe = openmc.Universe(cells=[graphite_cell])
beryllium_universe = openmc.Universe(cells=[beryllium_cell])
fuel_12_rod = openmc.Universe(
    cells=(
        fuel_12,
        openmc.Cell(fill=helium, region=+fuel_or & -clad_ir),
        openmc.Cell(fill=zircalloy, region=-clad_or & +clad_ir),
        openmc.Cell(fill=graphite, region=+clad_or),
    )
)
fuel_15_rod = openmc.Universe(
    cells=(
        fuel_15,
        openmc.Cell(fill=helium, region=+fuel_or & -clad_ir),
        openmc.Cell(fill=zircalloy, region=-clad_or & +clad_ir),
        openmc.Cell(fill=graphite, region=+clad_or),
    )
)
fuel_19_rod = openmc.Universe(
    cells=(
        fuel_19,
        openmc.Cell(fill=helium, region=+fuel_or & -clad_ir),
        openmc.Cell(fill=zircalloy, region=-clad_or & +clad_ir),
        openmc.Cell(fill=graphite, region=+clad_or),
    )
)


assembly_1 = openmc.HexLattice()
assembly_1.pitch = geom.assembly_pitch
assembly_1.outer = graphite_universe
assembly_1.orientation = "x"
assembly_1.universes = [[fuel_12_rod, heat_pipe] * 6, [fuel_12_rod] * 6, [control_rod]]
assembly_1.center = (0.0, 0.0)


assembly_2 = openmc.HexLattice()
assembly_2.pitch = geom.assembly_pitch
assembly_2.outer = graphite_universe
assembly_2.orientation = "x"
assembly_2.universes = [[fuel_15_rod, heat_pipe] * 6, [fuel_15_rod] * 6, [heat_pipe]]
assembly_2.center = (0.0, 0.0)

assembly_3 = openmc.HexLattice()

assembly_3.pitch = geom.assembly_pitch
assembly_3.outer = graphite_universe
assembly_3.orientation = "x"
assembly_3.universes = [[fuel_19_rod, heat_pipe] * 6, [fuel_19_rod] * 6, [heat_pipe]]
assembly_3.center = (0.0, 0.0)

outer_in_surface = openmc.model.HexagonalPrism(
    edge_length=geom.assembly_edge_length, orientation="y"
)

assembly_1_cell = openmc.Cell(fill=assembly_1, region=-outer_in_surface)
out_in_assembly = openmc.Cell(fill=graphite_universe, region=~(-outer_in_surface))
assembly_1_universe = openmc.Universe(cells=[assembly_1_cell, out_in_assembly])


assembly_2_cell = openmc.Cell(fill=assembly_2, region=-outer_in_surface)
out_in_assembly = openmc.Cell(fill=graphite_universe, region=~(-outer_in_surface))
assembly_2_universe = openmc.Universe(cells=[assembly_2_cell, out_in_assembly])

assembly_3_cell = openmc.Cell(fill=assembly_3, region=-outer_in_surface)
out_in_assembly = openmc.Cell(fill=graphite_universe, region=~(-outer_in_surface))
assembly_3_universe = openmc.Universe(cells=[assembly_3_cell, out_in_assembly])


core = openmc.HexLattice()
core.center = (0, 0)
core.pitch = geom.core_pitch
core.outer = beryllium_universe
core.orientation = "x"
core.universes = [
    [assembly_3_universe] * 18,
    [assembly_2_universe] * 12,
    [assembly_1_universe] * 6,
    [assembly_1_universe],
]


core_outer_in_surface = openmc.model.HexagonalPrism(
    edge_length=geom.assembly_edge_length * 7.5, orientation="y"
)
core_cell = openmc.Cell(
    fill=core, region=-core_outer_in_surface & +core_floor & -core_roof
)
out_in_core = openmc.Cell(
    fill=beryllium_universe,
    region=~(+core_outer_in_surface) & (+core_floor & -core_roof),
)


outer_berilyium_region = (
    -core_cylinder & +core_outer_in_surface & +core_floor & -core_roof
)
beryllium_cell = openmc.Cell(region=outer_berilyium_region, fill=beryllium)

cells = [core_cell, out_in_core, beryllium_cell]

angle_offset_deg = 90.0
angles_deg = np.linspace(0, 360, geom.number_of_control_drums, endpoint=False)

for i, angle_deg in enumerate(angles_deg):

    effective_angle_deg = angle_deg + angle_offset_deg
    effective_angle_rad = effective_angle_deg * geom.to_radian

    x = geom.distance_of_control_drums_from_center * np.cos(effective_angle_rad)
    y = geom.distance_of_control_drums_from_center * np.sin(effective_angle_rad)

    cylinder = openmc.ZCylinder(x0=x, y0=y, r=geom.outer_radius_of_control_drum)

    outer_berilyium_region &= +cylinder

    drum_cell = openmc.Cell(region=-cylinder, fill=control_drum_universe)
    drum_cell.translation = (x, y, 0)
    rotated_drum_cell = geom.rotate_control_drum_cell(
        drum_cell, -i * (360 / geom.number_of_control_drums)
    )

    cells.append(rotated_drum_cell)

core_universe = openmc.Universe(cells=cells)


geometry = openmc.Geometry(root=core_universe)

settings_file = openmc.Settings()
settings_file.batches = batches
settings_file.inactive = inactive
settings_file.particles = particles


settings_file.export_to_xml()
geometry.export_to_xml()
materials.export_to_xml()

openmc.run()
