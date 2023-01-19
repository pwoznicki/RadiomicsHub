import logging
import re
from pathlib import Path
from autorad.utils import spatial


import pandas as pd
from tqdm import tqdm
from pqdm.threads import pqdm

log = logging.getLogger(__name__)


def resample_masks_to_match_images(path_df: pd.DataFrame) -> None:
    img_paths = path_df["img_path"].values
    seg_paths = path_df["seg_path"].values
    for seg_path, img_path in tqdm(list(zip(seg_paths, img_paths))[3170:]):
        try:
            spatial.resample_to_img(to_resample=seg_path, reference=img_path)
        except RuntimeError as e:
            log.error(f"Could not resample {seg_path} to {img_path}")
            log.error(f"Orifinal error: {e}")
            continue


def find_lung_nodule_id(fname: str) -> str:
    pattern = re.compile("Nodule_\d+")
    match = pattern.findall(fname)
    if not match:
        raise ValueError("Could not find nodule ID in filename")
    return match[0]


def get_paths(img_dir: Path, seg_dir: Path) -> pd.DataFrame:
    image_paths = list(img_dir.glob("*.nii.gz"))
    seg_paths = list(seg_dir.glob("*.nii.gz"))
    ref = {
        "patient_ID": [],
        "ROI_ID": [],
        "seg_ID": [],
        "img_path": [],
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
        ref["img_path"] += [image_path] * len(matching_seg_paths)
        ref["patient_ID"] += [pat_id] * len(matching_seg_paths)
    df = pd.DataFrame(ref).sort_values(by=["patient_ID", "ROI_ID"])
    return df


def load_metadata(
    raw_metadata_df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    df = raw_metadata_df.copy()
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


def exclude_patients_with_multiple_series(df):
    df = df.copy()
    duplicate_patients = [
        "LIDC-IDRI-0132",
        "LIDC-IDRI-0151",
        "LIDC-IDRI-0315",
        "LIDC-IDRI-0332",
        "LIDC-IDRI-0355",
        "LIDC-IDRI-0365",
        "LIDC-IDRI-0442",
        "LIDC-IDRI-0484",
    ]
    df = df.loc[~df.patient_ID.isin(duplicate_patients)]
    return df


def create_path_df(
    img_dir: Path,
    seg_dir: Path,
    raw_metadata_df: pd.DataFrame,
):
    path_df = get_paths(img_dir, seg_dir)
    img_meta_df, seg_meta_df = load_metadata(raw_metadata_df)
    path_df = merge_metadata(path_df, img_meta_df, seg_meta_df)
    path_df = exclude_patients_with_multiple_series(path_df)

    return path_df
