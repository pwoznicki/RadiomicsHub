import logging

import pandas as pd

from radhub import master_config, utils
from radhub.RIDER_LungCT.config import config, excluded_ids
from radhub.RIDER_LungCT import preprocess, convert


log = logging.getLogger(__name__)


def run_pipeline():

    master_config.configure_logging(config.log_dir)

    utils.pretty_log("Converting and renaming DICOM images to Nifti (1/4)")

    convert.convert_img_to_nifti(
        config.raw_data_dir / "img",
        config.derived_nifti_dir / "img",
        excluded_ids=excluded_ids,
    )
    preprocess.rename_images_with_timepoints(
        nifti_img_dir=config.derived_nifti_dir / "img",
        dicom_img_dir=config.raw_data_dir / "img",
    )

    utils.pretty_log(
        "Converting and postprocessing DICOM segmentations to Nifti (2/4)"
    )

    convert.convert_seg_to_nifti(
        config.raw_data_dir / "seg",
        config.derived_nifti_dir / "seg",
        excluded_ids=excluded_ids,
    )
    utils.binarize_segmentations(config.derived_nifti_dir / "seg")

    utils.pretty_log("Creating a table with paths (3/4)")

    paths_df = preprocess.create_paths_df(
        config.derived_nifti_dir / "img", config.derived_nifti_dir / "seg"
    )
    paths_df.to_csv(config.derived_table_dir / "paths.csv", index=False)

    utils.pretty_log("Extracting features (4/4)")

    feature_df = utils.extract_features(
        paths_df=paths_df,
        ID_colname="unique_ID",
    )
    feature_df.to_csv(config.derived_table_dir / "features.csv", index=False)


if __name__ == "__main__":
    run_pipeline()
