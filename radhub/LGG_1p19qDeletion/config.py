from pathlib import Path

from radhub import master_config

base_dir = Path("/Volumes/pw-data/radiomics-features/LGG-1p19qDeletion")
raw_data_dir = base_dir / "raw" / "dicom"

config = master_config.Config(
    base_dir=base_dir,
    raw_data_dir=raw_data_dir,
)
