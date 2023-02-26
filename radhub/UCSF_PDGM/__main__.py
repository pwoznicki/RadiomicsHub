import logging

import pandas as pd

from radhub import master_config, utils
from radhub.UCSF_PDGM.config import config, rois, tumor_roi_labels
from radhub.UCSF_PDGM import preprocess

log = logging.getLogger(__name__)


def run_pipeline():

    master_config.configure_logging(config.log_dir)

    utils.pretty_log("Creating reference table (1/2)")
    # for roi in rois:
    #     paths_df = preprocess.create_path_df(config.raw_data_dir, roi=roi)
    #     paths_df.to_csv(
    #         config.derived_table_dir / f"paths_{roi}.csv", index=False
    #     )
    raw_label_df = pd.read_csv(
        config.raw_table_dir / "UCSF-PDGM-metadata_v2.csv"
    )
    raw_label_df.to_csv(config.derived_table_dir / "labels.csv", index=False)

    utils.pretty_log("Extracting features (2/2)")
    for roi in rois:
        paths_df = pd.read_csv(config.derived_table_dir / f"paths_{roi}.csv")
        if roi == "tumor":
            for tumor_roi, label in tumor_roi_labels.items():
                log.info(f"Extracting features for tumor ROI: {tumor_roi}")
                feature_df = utils.extract_features(
                    paths_df=paths_df,
                    ID_colname="unique_ID",
                    extraction_params="MR_default.yaml",
                    mask_label=label,
                )
                feature_df.to_csv(
                    config.derived_table_dir / f"features_{tumor_roi}.csv",
                    index=False,
                )
        else:
            log.info(f"Extracting features for ROI: {roi}")
            feature_df = utils.extract_features(
                paths_df=paths_df,
                ID_colname="unique_ID",
                extraction_params="MR_default.yaml",
            )
            feature_df.to_csv(
                config.derived_table_dir / f"features_{roi}.csv",
                index=False,
            )


if __name__ == "__main__":
    run_pipeline()
