import pandas as pd

import config


def get_pyradiomics_param_file(dataset):
    modality = config.modality_map[dataset]
    if modality == "CT":
        return "CT_Baessler.yaml"
    elif modality == "MR":
        return "MR_default.yaml"
    else:
        raise ValueError(f"Modality {modality} not recognized.")
