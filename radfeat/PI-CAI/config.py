from pathlib import Path

base_dir = Path("/mnt/hard/radiomics-features/PI-CAI")
img_dir = base_dir / "images"
lesion_mask_dir = base_dir / "picai_labels" / "csPCa_lesion_delineations" / "AI" / "Bosma22a"
prostate_mask_dir = base_dir / "picai_labels" / "anatomical_delineations" / "whole_gland" / "AI" / "Bosma22b"
table_dir = base_dir / "tables"
label_table_path = base_dir / "picai_labels" / "clinical_information" / "marksheet.csv"

table_dir.mkdir(exist_ok=True)
