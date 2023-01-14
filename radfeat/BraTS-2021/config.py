from pathlib import Path

from radfeat.master_config import configure_logging


base_dir = Path("/mnt/hard/radiomics-features/BraTS-2021")
table_dir = base_dir / "tables"
data_dir = base_dir / "raw" / "training_data"

log_dir = base_dir / "logs"
log_dir.mkdir()
