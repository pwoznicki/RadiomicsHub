import logging

import pandas as pd

from radhub import master_config, utils, validate
from radhub.PI_CAI import config, convert, preprocess


log = logging.getLogger(__name__)


def run_pipeline():

    master_config.configure_logging(config.log_dir)

    utils.pretty_log("Preprocessing segmentations (1/3)")

    for roi in config.rois:
        convert.convert_segmentations(
            roi["raw_seg_dir"],
            roi["derived_seg_dir"],
        )

    utils.pretty_log("Creating reference tables (2/3)")
    label_df = pd.read_csv(config.label_table_path)
    label_df.to_csv(config.derived_table_dir / "labels.csv", index=False)

    path_df = preprocess.get_paths(label_df)
    path_df.to_csv(config.derived_table_dir / "paths.csv", index=False)
    path_df = pd.read_csv(config.derived_table_dir / "paths.csv")

    utils.pretty_log("Extracting features (2/2)")
    feature_df = utils.extract_features(
        path_df,
        ID_colname="ROI_ID",
        extraction_params="MR_default.yaml",
    )
    feature_df.to_csv(config.derived_table_dir / f"features.csv", index=False)


if __name__ == "__main__":
    run_pipeline()
