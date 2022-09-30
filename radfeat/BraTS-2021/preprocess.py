import logging
from pathlib import Path

import config
import pandas as pd

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def get_paths(ID, raw_data_dirpath, sequence_name):
    series_ID = f"{ID}_{sequence_name}"
    img_path = raw_data_dirpath / ID / f"{ID}_{sequence_name}.nii.gz"
    seg_path = raw_data_dirpath / f"{ID}_seg.nii.gz"
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


def get_IDs(seg_dir):
    return [
        f.name.removesuffix("_automated_approx_segm.nii.gz")
        for f in seg_dir.glob("*_segm.nii.gz")
    ]


def create_ref_table():
    ref_data = []
    seg_dirpath = config.base_dir / "automated_segm"
    IDs = get_IDs(seg_dirpath)
    for ID in IDs:
        for sequence_name, dirname in sequence_map.items():
            img_dirpath = config.base_dir / dirname
            try:
                ref_data.append(
                    get_paths(ID, img_dirpath, seg_dirpath, sequence_name)
                )
            except FileNotFoundError:
                pass
    ref_table = pd.DataFrame(ref_data)
    return ref_table


if __name__ == "__main__":
    ref_table = create_ref_table()
    ref_table.to_csv(config.table_dir / "paths.csv", index=False)
