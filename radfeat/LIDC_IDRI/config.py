from pathlib import Path

from radfeat import master_config

base_dir = Path("/mnt/hard/radiomics-features/LIDC-IDRI")
raw_data_dir = base_dir / "raw" / "dicom"

config = master_config.Config(
    base_dir=base_dir,
    raw_data_dir=raw_data_dir,
)

metadata_path = config.raw_table_dir / "metadata.csv"
