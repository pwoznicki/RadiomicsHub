from pathlib import Path

import pandas as pd
from pqdm.threads import pqdm
from tqdm import tqdm

from radhub import utils


def find_data(raw_dicom_dir):
    raw_rt_paths = [
        fpath
        for fpath in raw_dicom_dir.glob("**/1-1.dcm")
        if "Segmentation" not in fpath.parent.name
    ]
    raw_img_paths = [
        utils.find_matching_img(
            rtstruct_path=rt_path,
            dcm_img_data=rt_path.parents[1],
        )
        for rt_path in tqdm(raw_rt_paths)
    ]
    return raw_img_paths, raw_rt_paths


def convert_dataset(raw_dicom_dir, derived_nifti_dir, n_jobs=8):
    raw_img_paths, raw_rt_paths = find_data(raw_dicom_dir)
    out_fnames = ["CT" for _ in raw_img_paths]
    return utils.convert_rt_dataset(
        raw_img_paths=raw_img_paths,
        raw_rt_paths=raw_rt_paths,
        derived_nifti_dir=derived_nifti_dir,
        out_fnames=out_fnames,
        n_jobs=n_jobs,
    )


def create_paths_df(derived_nifti_dir):
    seg_paths = list(derived_nifti_dir.rglob("seg*.nii.gz"))
    img_paths = [seg_path.parent / "CT.nii.gz" for seg_path in seg_paths]
    patient_ids = [seg_path.parent.name for seg_path in seg_paths]
    rois = [
        seg_path.name.split("_")[2].removesuffix(".nii.gz")
        for seg_path in seg_paths
    ]
    unique_ids = [f"{pid}_{roi}" for pid, roi in zip(patient_ids, rois)]
    df = pd.DataFrame(
        {
            "patient_ID": patient_ids,
            "ROI": rois,
            "unique_ID": unique_ids,
            "img_path": img_paths,
            "seg_path": seg_paths,
        }
    ).sort_values(["patient_ID", "ROI"])

    return df
