from pathlib import Path

base_dir = Path("/mnt/hard/radiomics-features/PI-CAI")
raw_data_dir = base_dir / "raw"

# It you follow README, there's no need to change paths below
derived_seg_dir = base_dir / "derived" / "segmentations"
derived_table_dir = base_dir / "derived" / "tables"
derived_table_dir.mkdir(parents=True, exist_ok=True)

log_dir = base_dir / "logs"


lesion_AI_seg_dir = ()

lesion_human_seg_dir = ()

prostate_seg_dir = ()

label_table_path = (
    raw_data_dir / "picai_labels" / "clinical_information" / "marksheet.csv"
)

rois = [
    {
        "name": "prostate",
        "raw_seg_dir": raw_data_dir
        / "picai_labels"
        / "anatomical_delineations"
        / "whole_gland"
        / "AI"
        / "Bosma22b",
        "derived_seg_dir": derived_seg_dir / "prostate",
        "annotator": "AI",
    },
    {
        "name": "lesion",
        "raw_seg_dir": raw_data_dir
        / "picai_labels"
        / "csPCa_lesion_delineations"
        / "AI"
        / "Bosma22a",
        "derived_seg_dir": derived_seg_dir / "lesion_AI",
        "annotator": "AI",
    },
    {
        "name": "lesion",
        "raw_seg_dir": raw_data_dir
        / "picai_labels"
        / "csPCa_lesion_delineations"
        / "human_expert"
        / "resampled",
        "derived_seg_dir": derived_seg_dir / "lesion_human",
        "annotator": "human",
    },
]
