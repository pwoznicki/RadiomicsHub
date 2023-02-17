import logging
import shutil

import pandas as pd

from radhub import master_config, utils
from radhub.LNDb.config import config
from radhub.LNDb import convert, preprocess

log = logging.getLogger(__name__)


def run_pipeline():

    master_config.configure_logging(config.log_dir)

    utils.pretty_log("Gathering metadata... (1/5)")

    ref_df = pd.read_csv(config.raw_table_dir / "trainNodules_gt.csv")
    ref_df_expanded = preprocess.expand_ref_df(ref_df)
    ref_df_expanded.to_csv(
        config.derived_table_dir / "trainNodules_gt_expanded.csv", index=False
    )

    utils.pretty_log("Converting .mhd/.raw images to .nii.gz (2/5)")

    raw_img_dir = config.raw_data_dir / "img"
    raw_seg_dir = config.raw_data_dir / "seg"
    derived_img_dir = config.derived_nifti_dir / "img"
    derived_seg_dir = config.derived_nifti_dir / "seg"
    convert.convert_images(
        raw_img_dir,
        derived_img_dir,
    )

    utils.pretty_log("Converting .mhd/.raw segmentations to .nii.gz (3/5)")

    convert.convert_and_separate_masks_all(
        raw_seg_dir=raw_seg_dir,
        derived_seg_dir=derived_seg_dir,
        expanded_ref_df=ref_df_expanded,
    )

    utils.pretty_log("Creating reference tables (4/5)")

    paths_df = preprocess.create_path_df(derived_img_dir, derived_seg_dir)
    paths_df.to_csv(config.derived_table_dir / "paths.csv", index=False)
    paths_df = pd.read_csv(config.derived_table_dir / "paths.csv")

    shutil.copy(
        config.raw_table_dir / "trainFleischner.csv",
        config.derived_table_dir / "labels.csv",
    )

    utils.pretty_log("Extracting features (5/5)")

    feature_df = utils.extract_features(paths_df=paths_df, ID_colname="seg_ID")
    feature_df.to_csv(config.derived_table_dir / "features.csv", index=False)


if __name__ == "__main__":
    run_pipeline()
