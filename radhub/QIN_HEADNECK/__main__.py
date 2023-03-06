import logging

import pandas as pd

from radhub import master_config, utils
from radhub.QIN_HEADNECK import preprocess
from radhub.QIN_HEADNECK.config import config

log = logging.getLogger(__name__)


def run_pipeline():

    master_config.configure_logging(config.log_dir)

    # utils.pretty_log(
    #     "Converting DICOM images and segmentations to Nifti (1/3)"
    # )
    # conversion_df = preprocess.convert_dataset(
    #     config.raw_data_dir, config.derived_nifti_dir
    # )
    # conversion_df.to_csv(
    #     config.derived_table_dir / "conversion.csv", index=False
    # )

    utils.pretty_log("Creating tables with paths and labels (2/3)")

    paths_df = preprocess.create_path_df(config.derived_nifti_dir)
    paths_df.to_csv(config.derived_table_dir / "paths.csv", index=False)

    raw_label_df = pd.read_excel(config.raw_table_dir / "clinical_data.xlsx")
    raw_label_df.to_csv(config.derived_table_dir / "labels.csv", index=False)

    utils.pretty_log("Extracting features (3/3)")
    for modality in ["CT"]:
        feature_df = utils.extract_features(
            paths_df=paths_df,
            ID_colname="unique_ID",
            image_colname=f"{modality}_path",
        )
        feature_df.to_csv(
            config.derived_table_dir / f"features_{modality}.csv", index=False
        )


if __name__ == "__main__":
    run_pipeline()
