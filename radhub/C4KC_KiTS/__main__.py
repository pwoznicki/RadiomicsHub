import logging

import pandas as pd

from radhub import master_config, utils
from radhub.C4KC_KiTS.config import config

log = logging.getLogger(__name__)


def run_pipeline():

    master_config.configure_logging(config.log_dir)

    utils.pretty_log("Converting DICOM images to Nifti (1/4)")
    dicom_segs = [
        path
        for path in config.raw_data_dir.rglob("*.dcm")
        if "Segmentation" in path.parent.name
    ]
    dicom_img_dirs = set(
        path.parent
        for path in config.raw_data_dir.rglob("*.dcm")
        if not "Segmentation" in path.parent.name
    )

    print(dicom_img_dirs)
    utils.convert_dicom_to_nifti(
        dicom_data=dicom_img_dirs,
        nifti_img_dir=config.derived_nifti_dir,
        filename_pattern="%i/CT_%d",
        ignore_derived=False,
        n_jobs=8,
    )

    utils.pretty_log("Converting DICOM segmentations to Nifti (2/4)")
    utils.convert_dicom_seg_dataset(
        dicom_data=dicom_segs,
        nifti_seg_dir=config.derived_nifti_dir,
        suffix="arterial",
    )

    utils.pretty_log("Extracting features (4/4)")


if __name__ == "__main__":
    run_pipeline()
