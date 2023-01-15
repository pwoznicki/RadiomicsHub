from pathlib import Path

from radfeat import master_config

base_dir = Path("/mnt/hard/radiomics-features/QIN-PROSTATE")
raw_data_dir = base_dir / "raw" / "dicom"

config = master_config.Config(
    base_dir=base_dir,
    raw_data_dir=raw_data_dir,
)
