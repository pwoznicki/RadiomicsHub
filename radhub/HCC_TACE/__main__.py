import logging

import pandas as pd

from radhub import master_config, utils
from radhub.HCC_TACE import convert, create_paths
from radhub.HCC_TACE.config import config

log = logging.getLogger(__name__)


def run_pipeline():

    master_config.configure_logging(config.log_dir)

    utils.pretty_log(
        "Converting DICOM images and segmentations to Nifti (1/3)"
    )
    conversion_df = convert.convert_dataset(
        raw_data_dir=config.raw_data_dir,
        derived_nifti_dir=config.derived_nifti_dir,
    )
    conversion_df.to_csv(
        config.derived_table_dir / "conversion.csv", index=False
    )

    utils.pretty_log("Creating tables with paths and labels (2/3)")
    paths_df = create_paths.create_paths_df(
        derived_nifti_dir=config.derived_nifti_dir,
    )
    paths_df.to_csv(config.derived_table_dir / "paths.csv", index=False)

    label_df = pd.read_excel(
        config.raw_table_dir / "HCC-TACE-Seg_clinical_data-V2.xlsx"
    )
    label_df.to_csv(config.derived_table_dir / "labels.csv", index=False)

    utils.pretty_log("Extracting features (3/3)")
    feature_df = utils.extract_features(
        paths_df=paths_df,
        ID_colname="unique_ID",
    )
    feature_df.to_csv(config.derived_table_dir / "features.csv", index=False)


if __name__ == "__main__":
    run_pipeline()
