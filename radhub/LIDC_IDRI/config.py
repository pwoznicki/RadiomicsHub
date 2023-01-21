from pathlib import Path

from radhub import master_config

base_dir = Path("/mnt/hard/radiomics-features/LIDC-IDRI")
raw_data_dir = base_dir / "raw"

config = master_config.Config(
    base_dir=base_dir,
    raw_data_dir=raw_data_dir,
)
