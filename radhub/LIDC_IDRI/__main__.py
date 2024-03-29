import logging

import pandas as pd

from radhub import master_config, utils
from radhub.LIDC_IDRI import convert, preprocess
from radhub.LIDC_IDRI.config import config

log = logging.getLogger(__name__)


def run_pipeline():

    master_config.configure_logging(config.log_dir)

    utils.pretty_log(
        "Converting DICOM images and segmentations to Nifti (1/4)"
    )

    convert.convert_dicom_img_to_nifti(
        config.raw_data_dir / "img",
        config.derived_nifti_dir / "img",
    )
    convert.convert_dicom_seg_to_nifti(
        config.raw_data_dir / "seg",
        config.derived_nifti_dir / "seg",
    )

    utils.pretty_log("Creating reference tables (2/4)")

    raw_metadata_df = pd.read_csv(config.raw_table_dir / "metadata.csv")
    path_df = preprocess.create_path_df(
        img_dir=config.derived_nifti_dir / "img",
        seg_dir=config.derived_nifti_dir / "seg",
        raw_metadata_df=raw_metadata_df,
    )
    path_df.to_csv(config.derived_table_dir / "paths.csv", index=False)

    label_df = pd.read_excel(
        config.raw_table_dir / "tcia-diagnosis-data-2012-04-20.xls"
    )
    label_df[label_df.columns[:8]].to_csv(
        config.derived_table_dir / "labels.csv", index=False
    )

    utils.pretty_log("Resampling masks to match images (3/4)")
    preprocess.resample_masks_to_match_images(path_df)

    utils.pretty_log("Extracting features (4/4)")

    path_df = pd.read_csv(config.derived_table_dir / "paths.csv")
    feature_df = utils.extract_features(path_df, ID_colname="seg_ID")
    feature_df.to_csv(config.derived_table_dir / "features.csv", index=False)


if __name__ == "__main__":
    run_pipeline()
