import logging

import pandas as pd

from radhub import master_config, utils
from radhub.NSCLC_Radiogenomics.config import config
from radhub.NSCLC_Radiogenomics import preprocess

log = logging.getLogger(__name__)


def run_pipeline():

    master_config.configure_logging(config.log_dir)

    utils.pretty_log(
        "Converting DICOM images and segmentations to Nifti (1/3)"
    )
    ct_dirs, seg_dirs = preprocess.find_studies(config.raw_data_dir)
    utils.convert_dicom_to_nifti(
        dicom_data=ct_dirs,
        nifti_img_dir=config.derived_nifti_dir,
        filename_pattern="%i/img_%d",
        ignore_derived=False,
        n_jobs=8,
    )
    utils.convert_dicom_to_nifti(
        dicom_data=seg_dirs,
        nifti_img_dir=config.derived_nifti_dir,
        filename_pattern="%i/seg",
        ignore_derived=False,
    )

    utils.pretty_log("Compiling a table with paths and labels (2/3)")
    paths_df = preprocess.create_paths_df(config.derived_nifti_dir)
    paths_df.to_csv(config.derived_table_dir / "paths.csv", index=False)

    raw_label_df = pd.read_csv(config.raw_table_dir / "clinical_data.csv")
    label_df = preprocess.create_label_df(raw_label_df)
    label_df.to_csv(config.derived_table_dir / "labels.csv", index=False)

    utils.pretty_log("Extracting features (3/3)")
    feature_df = utils.extract_features(
        paths_df=paths_df,
        ID_colname="case_ID",
    )
    feature_df.to_csv(config.derived_table_dir / "features.csv", index=False)


if __name__ == "__main__":
    run_pipeline()
