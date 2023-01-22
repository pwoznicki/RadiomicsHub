import logging

import pandas as pd

from radhub import master_config, utils, validate
from radhub.PI_CAI import config, convert, preprocess


log = logging.getLogger(__name__)


def run_pipeline():

    master_config.configure_logging(config.log_dir)

    # text = " Preprocessing segmentations (1/3) "
    # log.info(f"{text:#^80}")

    # for roi in config.rois:
    #     convert.convert_segmentations(
    #         roi["raw_seg_dir"],
    #         roi["derived_seg_dir"],
    #     )

    # text = " Creating reference tables (2/3) "
    # log.info(f"{text:#^80}")

    # label_df = pd.read_csv(config.label_table_path)
    # label_df.to_csv(config.derived_table_dir / "labels.csv", index=False)

    # path_df = preprocess.get_paths(label_df)
    # path_df.to_csv(config.derived_table_dir / "paths.csv", index=False)
    path_df = pd.read_csv(config.derived_table_dir / "paths.csv")

    text = " Extracting features (2/2) "
    log.info(f"{text:#^80}")

    feature_df = utils.extract_features(
        path_df,
        ID_colname="ROI_ID",
        extraction_params="MR_default.yaml",
    )
    feature_df.to_csv(config.derived_table_dir / f"features.csv", index=False)


if __name__ == "__main__":
    run_pipeline()
