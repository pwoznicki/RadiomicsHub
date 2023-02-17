from pathlib import Path
import pandas as pd
import config
import pydicom as dcm
import os
import operator
import shutil
import logging
from tqdm import tqdm

log = logging.getLogger(__name__)


def remove_excluded_cases(derived_nifti_dir, excluded_ids):
    all_files = list(derived_nifti_dir.rglob("*"))

    for excluded_id in excluded_ids:
        files_to_exclude = [
            file for file in all_files if excluded_id in str(file)
        ]
        print(files_to_exclude)
        for file in files_to_exclude:
            os.remove(file)
            log.info(f"File removed: {file}")


def rename_images_with_timepoints(nifti_img_dir: Path, dicom_img_dir: Path):
    """I (Piotr) couldn't find the info on whether a CT image belongs to TEST or RETEST,
    so I extract Instance Creation time from DICOM metadata to assign that
    chronologically."""

    json_files = list(nifti_img_dir.rglob("*.json"))
    for json_file in json_files:
        os.remove(json_file)
    dicom_dirs = list(dicom_img_dir.glob("*/*/*/"))
    dates = {}
    for dicom_dir in dicom_dirs:
        patient_ID = dicom_dir.parts[-3]
        dcm_ds = dcm.dcmread(list(dicom_dir.glob("*"))[0])
        series_instance_uid = get_dcm_tag(dcm_ds, 0x0020000E)
        matching_nifti_img_path = (
            nifti_img_dir / f"{patient_ID}_{series_instance_uid}.nii.gz"
        )
        if not matching_nifti_img_path.exists():
            log.warn(
                f"Nifti image doesn't exist! ({str(matching_nifti_img_path)})"
            )
        date = get_dcm_tag(dcm_ds, 0x00080013)
        if not patient_ID in dates:
            dates[patient_ID] = {}
        dates[patient_ID][series_instance_uid] = date

    img_paths = nifti_img_dir.glob("*.nii.gz")
    for img_path in img_paths:
        id_, series_uid = img_path.name.removesuffix(".nii.gz").split("_")
        n_dates = len(dates[id_])
        if not n_dates == 2:
            raise Exception(f"Found {n_dates} dates for {id_}, expected 2!")
        timepoint = get_timepoint(dates[id_], series_uid)

        new_img_path = nifti_img_dir / f"{id_}_{timepoint}.nii.gz"
        os.rename(img_path, new_img_path)


def get_timepoint(time_dict: dict[str], series_uid: int):
    if not len(time_dict) == 2:
        raise Exception("Dictionary should have 2 values!")
    if list(time_dict.values())[0] > list(time_dict.values())[1]:
        if series_uid == list(time_dict.keys())[0]:
            return "RETEST"
        else:
            return "TEST"
    else:
        if series_uid == list(time_dict.keys())[0]:
            return "TEST"
        else:
            return "RETEST"


def get_dcm_tag(ds, tag):
    if not tag in ds:
        raise ValueError(f"Tag not found! ({tag})")
    return ds[tag].value


def create_paths_df(nifti_img_dir, nifti_seg_dir):
    img_paths = list(nifti_img_dir.glob("*.nii.gz"))
    results = []
    for img_path in img_paths:
        patient_ID = img_path.name.split("_")[0]
        timepoint = img_path.name.split("_")[1].removesuffix(".nii.gz")
        human_seg_path = (
            nifti_seg_dir / f"{patient_ID}_{timepoint}" / "1.nii.gz"
        )
        auto_seg_path = (
            nifti_seg_dir / f"{patient_ID}_{timepoint}" / "2.nii.gz"
        )
        if not human_seg_path.exists():
            log.error(f"Segmentation file not found: {str(human_seg_path)}")
        else:
            results.append(
                {
                    "patient_ID": patient_ID,
                    "test/retest": timepoint,
                    "annotator": "human",
                    "unique_ID": f"{patient_ID}_{timepoint}_human",
                    "img_path": str(img_path),
                    "seg_path": str(human_seg_path),
                }
            )
        if not auto_seg_path.exists():
            log.error(f"Segmentation file not found: {str(auto_seg_path)}")
        else:
            results.append(
                {
                    "patient_ID": patient_ID,
                    "test/retest": timepoint,
                    "annotator": "auto",
                    "unique_ID": f"{patient_ID}_{timepoint}_auto",
                    "img_path": str(img_path),
                    "seg_path": str(auto_seg_path),
                },
            )
    return pd.DataFrame(results).sort_values(["patient_ID", "test/retest"])
