from radhub import master_config
from pathlib import Path


base_dir = Path("/mnt/hard/radiomics-features/RIDER-LungCT")

raw_data_dir = base_dir / "raw" / "dicom"

config = master_config.Config(
    base_dir=base_dir,
    raw_data_dir=raw_data_dir,
)

excluded_ids = [
    "RIDER-2283289298",  # only 1 timepoint
    "RIDER-5195703382",  # only 1 timepoint
    "RIDER-8509201188",  # only 1 timepoint
]
