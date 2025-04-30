import openmc


material_dict = {
    "sodium": {"density": 0.927, "composition": {"Na23": 1.0}},  # g/cm3 at 400°C
    "stainless_steel": {
        "density": 7.9,
        "composition": {
            "Fe54": 0.035405,
            "Fe56": 0.555685,
            "Fe57": 0.01283,
            "Fe58": 0.001708,
            "Cr50": 0.007675,
            "Cr52": 0.147965,
            "Cr53": 0.016775,
            "Cr54": 0.004175,
            "Ni58": 0.06019,
            "Ni60": 0.02318,
            "Ni61": 0.001007,
            "Ni62": 0.003211,
            "Ni64": 0.000817,
            "Mn55": 0.02,
            "Si28": 0.01,
            "Si29": 0.0005,
            "Si30": 0.00033,
            "C12": 0.001,
        },
    },
    "zircalloy": {
        "density": 6.56,
        "composition": {
            "Zr90": 0.5145,
            "Zr91": 0.1122,
            "Zr92": 0.1715,
            "Zr94": 0.1738,
            "Zr96": 0.028,
            "Sn112": 0.005,
            "Sn114": 0.0034,
            "Sn115": 0.0017,
            "Sn116": 0.0073,
            "Sn117": 0.0039,
            "Sn118": 0.0123,
            "Sn119": 0.0043,
            "Sn120": 0.0164,
            "Sn122": 0.0023,
            "Sn124": 0.0029,
            "Fe54": 0.0009,
            "Fe56": 0.0141,
            "Fe57": 0.0003,
            "Fe58": 0.00004,
            "Cr50": 0.0002,
            "Cr52": 0.0039,
            "Cr53": 0.0004,
            "Cr54": 0.0001,
        },
    },
    "helium": {"density": 0.0001785, "composition": {"He4": 1.0}},  # g/cm3 at STP
    "uranium_12_percent": {
        "density": 10.5,
        "composition": {"U235": 0.12, "U238": 0.88},
    },
    "uranium_15_percent": {
        "density": 10.5,
        "composition": {"U235": 0.15, "U238": 0.85},
    },
    "uranium_19_percent": {
        "density": 10.5,
        "composition": {"U235": 0.1975, "U238": 0.8025},
    },
    "graphite": {"density": 1.7, "composition": {"C12": 1.0}},  # Natural carbon
    "beryllium": {"density": 1.85, "composition": {"Be9": 1.0}},
    "boron_carbide": {
        "density": 4.52,
        "composition": {"B10": 0.199, "B11": 0.801, "C12": 1.0},  # Natural carbon
    },
}


def make_material(material_dict, percent_type: str):
    material = openmc.Material()
    material.set_density("g/cm3", material_dict["density"])

    for nuclide, percent in material_dict["composition"].items():
        material.add_nuclide(nuclide, percent=percent, percent_type=percent_type)

    return material
