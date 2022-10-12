import logging
from pathlib import Path

import config
import pandas as pd

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def get_paths(ID, raw_data_dir, sequence_name):
    series_ID = f"{ID}_{sequence_name}"
    img_path = raw_data_dir / str(ID) / f"{ID}_{sequence_name}.nii.gz"
    seg_path = raw_data_dir / str(ID) / f"{ID}_seg.nii.gz"
    if not img_path.exists():
        log.info(f"Image file not found: {img_path}")
        raise FileNotFoundError(f"File not found: {img_path}")
    if not seg_path.exists():
        log.info(f"Segmentation file not found: {seg_path}")
        raise FileNotFoundError(f"File not found: {seg_path}")
    return {
        "patient_ID": ID,
        "series_ID": series_ID,
        "sequence": sequence_name,
        "img_path": str(img_path),
        "seg_path": str(seg_path),
    }


def get_IDs(table_dir):
    df = pd.read_csv(table_dir / "train_labels.csv")
    IDs = df["BraTS21ID"].values
    IDs_str = [f"BraTS2021_{ID:05d}" for ID in IDs]
    return IDs_str


def create_ref_table():
    ref_data = []
    IDs = get_IDs(config.table_dir)
    data_dir = config.base_dir / "training_data"
    sequences = ["t1", "t1ce", "t2", "flair"]
    for ID in IDs:
        for sequence_name in sequences:
            try:
                ref_data.append(get_paths(ID, data_dir, sequence_name))
            except FileNotFoundError:
                pass
    ref_table = pd.DataFrame(ref_data)
    return ref_table


if __name__ == "__main__":
    ref_table = create_ref_table()
    ref_table.to_csv(config.table_dir / "paths.csv", index=False)
