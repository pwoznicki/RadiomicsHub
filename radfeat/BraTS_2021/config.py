from pathlib import Path

from radfeat import master_config

base_dir = Path("/mnt/hard/radiomics-features/BraTS-2021")
raw_data_dir = base_dir / "raw" / "training_data"
# label_df_path = base_dir / "raw" / "tables" / "train_labels.csv"

config = master_config.Config(
    base_dir=base_dir,
    raw_data_dir=raw_data_dir,
)
