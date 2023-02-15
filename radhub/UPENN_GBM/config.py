from pathlib import Path

base_dir = Path("/mnt/hard/radiomics-features/UPENN-GBM")
derived_table_dir = base_dir / "derived" / "tables"

raw_data_dir = base_dir / "raw"
raw_table_dir = raw_data_dir / "tables"
raw_seg_dir = raw_data_dir / "automated_segm"

log_dir = base_dir / "logs"
