import logging
import re
from pathlib import Path

import pandas as pd
from tqdm import tqdm

import config

log = logging.getLogger(__name__)


def find_lung_nodule_id(fname):
    pattern = re.compile("Nodule_\d+")
    match = pattern.findall(fname)
    if not match:
        raise ValueError("Could not find nodule ID in filename")
    return match[0]


def get_paths(data_dir) -> pd.DataFrame:
    img_dir = data_dir / "nifti_img"
    seg_dir = data_dir / "nifti_seg"
    image_paths = list(img_dir.glob("*.nii.gz"))
    seg_paths = list(seg_dir.glob("*.nii.gz"))
    ref = {
        "patient_ID": [],
        "ROI_ID": [],
        "seg_ID": [],
        "image_path": [],
        "seg_path": [],
    }
    for image_path in tqdm(image_paths):
        pat_id = image_path.name.split(".")[0]
        matching_seg_paths = [p for p in seg_paths if pat_id in p.name]
        matching_roi_names = [
            find_lung_nodule_id(p.name) for p in matching_seg_paths
        ]
        if not matching_seg_paths:
            log.warning(f"Missing segmentation for ID={pat_id}")
        ref["seg_path"] += matching_seg_paths
        ref["ROI_ID"] += matching_roi_names
        ref["seg_ID"] += [p.name.split(".")[0] for p in matching_seg_paths]
        ref["image_path"] += [image_path] * len(matching_seg_paths)
        ref["patient_ID"] += [pat_id] * len(matching_seg_paths)
    df = pd.DataFrame(ref).sort_values(by=["patient_ID", "ROI_ID"])
    return df


def load_metadata(data_dir):
    metadata_path = data_dir / "metadata.csv"
    df = pd.read_csv(metadata_path)
    df.rename(columns={"Subject ID": "patient_ID"}, inplace=True)
    img_df = df[df.Modality == "CT"][["Series UID", "Study UID", "patient_ID"]]
    img_df.rename({"Series UID": "Image Series UID"}, axis=1, inplace=True)
    seg_df = df[df.Modality == "SEG"][
        ["Series UID", "Series Description", "patient_ID"]
    ]
    seg_df["seg_ID"] = seg_df.apply(
        lambda x: x["patient_ID"]
        + "_"
        + x["Series Description"].replace(" ", "_"),
        axis=1,
    )
    seg_df.rename(
        {"Series UID": "Segmentation Series UID"}, axis=1, inplace=True
    )
    seg_df.drop("Series Description", axis=1, inplace=True)
    return img_df, seg_df


def merge_metadata(path_df, img_meta_df, seg_meta_df):
    df = path_df.copy()
    df = df.merge(img_meta_df, on="patient_ID")
    df = df.merge(
        seg_meta_df,
        on=["patient_ID", "seg_ID"],
    )
    return df


if __name__ == "__main__":
    img_meta_df, seg_meta_df = load_metadata(config.base_dir)
    path_df = get_paths(config.base_dir)
    img_meta_df.to_csv(config.base_dir / "image_df.csv", index=False)
    path_df.to_csv(config.base_dir / "paths_raw_debug.csv", index=False)
    df = merge_metadata(path_df, img_meta_df, seg_meta_df)
    df.to_csv(config.base_dir / "paths.csv", index=False)
