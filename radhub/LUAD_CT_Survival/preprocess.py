import logging
from pathlib import Path

import numpy as np
import pandas as pd
import SimpleITK as sitk
from tqdm import tqdm

log = logging.getLogger(__name__)


def cleanse_segmentations(input_seg_dir: Path, output_seg_dir: Path):
    output_seg_dir.mkdir(parents=True, exist_ok=True)
    for seg_path in tqdm(list(input_seg_dir.glob("*.nii"))):
        seg = sitk.ReadImage(str(seg_path))
        seg_arr = sitk.GetArrayFromImage(seg)
        new_seg_arr = np.zeros(seg_arr.shape)
        new_seg_arr[seg_arr > 1] = 1
        new_seg = sitk.GetImageFromArray(new_seg_arr)
        new_seg.CopyInformation(seg)

        new_stem = seg_path.stem.replace("_", "0")
        sitk.WriteImage(
            new_seg, str(Path(output_seg_dir) / (new_stem + ".nii.gz"))
        )


def create_path_df(nifti_img_dir, nifti_seg_dir):
    meta_list = []
    for seg_path in Path(nifti_seg_dir).glob("*.nii.gz"):
        img_path = Path(nifti_img_dir) / seg_path.name
        if not seg_path.exists():
            log.error(f"Segmentation not found: {seg_path}")
            raise FileNotFoundError(f"Segmentation not found: {seg_path}")
        id_ = seg_path.name.split(".")[0]
        meta_list.append(
            {
                "patient_ID": id_,
                "img_path": str(img_path),
                "seg_path": str(seg_path),
            }
        )
    return (
        pd.DataFrame(meta_list)
        .sort_values("patient_ID")
        .reset_index(drop=True)
    )


def extract_labels(raw_label_df):
    label_df = raw_label_df[["RID", "survival_label"]]
    label_df.columns = ["patient_ID", "survival_label"]
    return label_df
