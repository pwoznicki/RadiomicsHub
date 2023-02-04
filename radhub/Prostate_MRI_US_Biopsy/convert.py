from pathlib import Path
import os
import slicer
import logging
from tqdm import tqdm
from pqdm.threads import pqdm

from radhub import utils

log = logging.getLogger(__name__)


def find_relevant_MRI_series(dicom_img_dir):
    result_list = []
    for patient_dir in dicom_img_dir.iterdir():
        if not patient_dir.is_dir():
            continue
        for series_dir in patient_dir.iterdir():
            if not "Rendering" in series_dir.name:
                result_list.append(series_dir)
    return result_list


def convert_dicom_img_to_nifti(
    dicom_img_dirs, nifti_img_dir, filename_pattern="%i"
):
    nifti_img_dir.mkdir(parents=True, exist_ok=True)

    img_cmds = (
        [
            "dcm2niix",
            "-z",
            "y",
            "-f",
            filename_pattern,
            "-o",
            nifti_img_dir.as_posix(),
            "-i",
            "y",
            dicom_dir.as_posix(),
        ]
        for dicom_dir in dicom_img_dirs
    )
    pqdm(img_cmds, utils.convert_series, n_jobs=16)