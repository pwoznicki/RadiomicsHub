from pathlib import Path

from radhub import master_config

base_dir = Path("/Users/pwoznicki/git/RadiomicsHub/data/LUAD-CT-Survival")
raw_data_dir = base_dir / "raw"
raw_img_dir = raw_data_dir / "img"
raw_seg_dir = raw_data_dir / "seg"

config = master_config.Config(
    base_dir=base_dir,
    raw_data_dir=raw_data_dir,
    raw_img_dir=raw_img_dir,
    raw_seg_dir=raw_seg_dir,
)
