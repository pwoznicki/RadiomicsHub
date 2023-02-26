from pathlib import Path

from radhub import master_config

base_dir = Path("/mnt/hard/radiomics-features/UCSF-PDGM")
raw_data_dir = base_dir / "raw" / "nifti"

config = master_config.Config(
    base_dir=base_dir,
    raw_data_dir=raw_data_dir,
)

rois = [
    "tumor",
    # "brain", - excluded because the extraction takes too long
    # "brain_parenchyma", - excluded because the extraction takes too long
]
tumor_roi_labels = {
    "necrotic_core": 1,
    "peritumoral_edema": 2,
    "enhancing_tumor": 4,
}

sequences = [
    "T2",
    "T2_bias",
    "T1",
    "T1_bias",
    "T1c",
    "T1c_bias",
    "SWI",
    "SWI_bias",
    "FLAIR",
    "FLAIR_bias",
    "DWI",
    "DWI_bias",
    "ADC",
    "ASL",
    "DTI_eddy_FA",
    "DTI_eddy_L1",
    "DTI_eddy_L2",
    "DTI_eddy_L3",
    "DTI_eddy_MD",
]
