from pathlib import Path

base_dir = Path("/mnt/hard/radiomics-features/PI-CAI")
raw_data_dir = base_dir / "raw"

derived_table_dir = base_dir / "derived" / "tables"
derived_table_dir.mkdir(parents=True, exist_ok=True)

log_dir = base_dir / "logs"


lesion_AI_seg_dir = (
    raw_data_dir
    / "picai_labels"
    / "csPCa_lesion_delineations"
    / "AI"
    / "Bosma22a"
)

lesion_human_seg_dir = (
    raw_data_dir
    / "picai_labels"
    / "csPCa_lesion_delineations"
    / "human_expert"
    / "resampled"
)

prostate_seg_dir = (
    raw_data_dir
    / "picai_labels"
    / "anatomical_delineations"
    / "whole_gland"
    / "AI"
    / "Bosma22b"
)

label_table_path = (
    raw_data_dir / "picai_labels" / "clinical_information" / "marksheet.csv"
)
