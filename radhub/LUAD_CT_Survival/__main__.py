import logging

import pandas as pd

from radhub import master_config, utils
from radhub.LUAD_CT_Survival import preprocess
from radhub.LUAD_CT_Survival.config import config

log = logging.getLogger(__name__)


def run_pipeline():

    master_config.configure_logging(config.log_dir)

    utils.pretty_log("Converting DICOM images to Nifti (1/4)")
    utils.convert_dicom_img_to_nifti(
        dicom_img_dir=config.raw_img_dir,
        nifti_img_dir=config.derived_nifti_dir / "img",
    )

    utils.pretty_log("Cleaning Nifti segmentations (2/4)")
    preprocess.cleanse_segmentations(
        config.raw_seg_dir, config.derived_nifti_dir / "seg"
    )

    utils.pretty_log("Creating a table with paths (3/4)")
    paths_df = preprocess.create_path_df(
        nifti_img_dir=config.derived_nifti_dir / "img",
        nifti_seg_dir=config.derived_nifti_dir / "seg",
    )
    paths_df.to_csv(config.derived_table_dir / "paths.csv", index=False)

    raw_label_df = pd.read_csv(config.raw_table_dir / "FeaturesWithLabels.csv")
    label_df = preprocess.extract_labels(raw_label_df)
    label_df.to_csv(config.derived_table_dir / "labels.csv", index=False)

    utils.pretty_log("Extracting features (4/4)")

    feature_df = utils.extract_features(
        paths_df=paths_df,
        ID_colname="patient_ID",
        extraction_params="CT_default.yaml",
        n_jobs=-1,
    )
    feature_df.to_csv(config.derived_table_dir / "features.csv", index=False)


if __name__ == "__main__":
    run_pipeline()
