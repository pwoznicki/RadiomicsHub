from pathlib import Path

from radfeat import master_config

base_dir = Path("/mnt/hard/radiomics-features/PI-CAI")

config = master_config.Config(
    base_dir=base_dir,
    raw_data_dir=base_dir / "raw",
)

raw_lesion_seg_dir = (
    config.raw_data_dir
    / "picai_labels"
    / "csPCa_lesion_delineations"
    / "AI"
    / "Bosma22a"
)
prostate_mask_dir = (
    config.raw_data_dir
    / "picai_labels"
    / "anatomical_delineations"
    / "whole_gland"
    / "AI"
    / "Bosma22b"
)

label_table_path = (
    base_dir / "picai_labels" / "clinical_information" / "marksheet.csv"
)
