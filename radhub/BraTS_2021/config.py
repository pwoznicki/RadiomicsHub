from pathlib import Path

from radhub import master_config

base_dir = Path("/mnt/hard/radiomics-features/BraTS-2021")
raw_data_dir = base_dir / "raw" / "training_data"

config = master_config.Config(
    base_dir=base_dir,
    raw_data_dir=raw_data_dir,
)
