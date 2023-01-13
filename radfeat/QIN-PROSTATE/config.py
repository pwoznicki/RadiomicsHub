from pathlib import Path

base_dir = Path("/mnt/hard/radiomics-features/QIN-PROSTATE")
table_dir = base_dir / "tables"
table_dir.mkdir(exist_ok=True)

raw_dir = base_dir / "raw"
nifti_dir = base_dir / "nifti"
