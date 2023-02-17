import logging

import pandas as pd

from radhub import master_config
from radhub.NSCLC_Radiomics.config import config
from radhub.NSCLC_Radiomics import preprocess
from radhub import utils

log = logging.getLogger(__name__)


def run_pipeline():

    master_config.configure_logging(config.log_dir)

    utils.pretty_log("Converting DICOM images to Nifti (1/5)")
    utils.convert_dicom_to_nifti(
        config.raw_data_dir,
        config.derived_nifti_dir,
        filename_pattern="%i/ct",
        ignore_derived=True,
    )

    utils.pretty_log("Converting DICOM segmentations to Nifti (2/5)")
    preprocess.convert_seg_to_nifti(
        raw_dicom_dir=config.raw_data_dir,
        derived_nifti_dir=config.derived_nifti_dir,
    )

    utils.pretty_log("Renaming and relabeling Nifti segmentations (3/5)")
    preprocess.rename_dcmqi_nifti_seg(config.derived_nifti_dir)
    all_seg_paths = list(config.derived_nifti_dir.rglob("*seg*.nii.gz"))
    utils.binarize_segmentations(nifti_data=all_seg_paths)

    utils.pretty_log("Creating a table with paths (4/5)")
    paths_df = preprocess.create_paths_df(
        derived_nifti_dir=config.derived_nifti_dir
    )
    paths_df.to_csv(config.derived_table_dir / "paths.csv", index=False)

    label_df = pd.read_csv(config.raw_table_dir / "clinical_info.csv")
    label_df.to_csv(config.derived_table_dir / "labels.csv", index=False)

    utils.pretty_log("Extracting features (5/5)")
    feature_df = utils.extract_features(
        paths_df=paths_df,
        ID_colname="patient_ID",
    )
    feature_df.to_csv(config.derived_table_dir / "features.csv", index=False)


if __name__ == "__main__":
    run_pipeline()
