import logging
from pathlib import Path

import pandas as pd

log = logging.getLogger(__name__)


def get_paths(
    ID: str, raw_data_dir: Path, sequence_name: str
) -> dict[str, str]:
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
        "sequence": sequence_name,
        "series_ID": series_ID,
        "img_path": str(img_path),
        "seg_path": str(seg_path),
    }


def process_label_df(raw_label_df: pd.DataFrame):
    df = raw_label_df.copy()
    df["patient_ID"] = df["BraTS21ID"].apply(lambda x: f"BraTS2021_{x:05d}")
    df["MGMT_value"] = df["MGMT_value"].astype(int)
    df.drop(columns=["BraTS21ID"], inplace=True)
    return df


def get_IDs(derived_label_df: pd.DataFrame) -> list[str]:
    IDs = derived_label_df["patient_ID"].values
    return list(IDs)


def create_path_df(data_dir: Path, label_df: pd.DataFrame) -> pd.DataFrame:
    ref_data = []
    IDs = get_IDs(label_df)
    sequences = ["t1", "t1ce", "t2", "flair"]
    for id_ in IDs:
        for sequence_name in sequences:
            try:
                ref_data.append(get_paths(id_, data_dir, sequence_name))
            except FileNotFoundError:
                pass
    ref_table = pd.DataFrame(ref_data)
    return ref_table
