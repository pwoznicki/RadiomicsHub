from pathlib import Path

from radhub import master_config

base_dir = Path("/Volumes/pw-data/radiomics-features/Meningioma-SEG-CLASS")
raw_data_dir = base_dir / "raw" / "dicom"

config = master_config.Config(
    base_dir=base_dir,
    raw_data_dir=raw_data_dir,
)

EXCLUDED_ID = "Meningioma-SEG-CLASS-094"
