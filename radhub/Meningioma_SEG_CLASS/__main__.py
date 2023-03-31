import logging

import pandas as pd

from radhub import master_config, utils
from radhub.Meningioma_SEG_CLASS import preprocess
from radhub.Meningioma_SEG_CLASS.config import config

log = logging.getLogger(__name__)


def run_pipeline():

    master_config.configure_logging(config.log_dir)

    utils.pretty_log(
        "Converting DICOM images and segmentations to Nifti (1/3)"
    )
    raw_path_df = preprocess.find_data(config.raw_data_dir)
    conversion_df = preprocess.convert_dataset(
        raw_path_df, config.derived_nifti_dir, n_jobs=6
    )
    conversion_df.to_csv(
        config.derived_table_dir / "conversion.csv", index=False
    )

    utils.pretty_log("Creating tables with paths and labels (2/3)")
    paths_df = preprocess.create_paths_df(
        raw_path_df=raw_path_df,
        conversion_df=conversion_df,
    )
    paths_df.to_csv(config.derived_table_dir / "paths.csv", index=False)

    label_df = pd.read_excel(config.raw_table_dir / "clinical_data.xlsx")
    label_df.to_csv(config.derived_table_dir / "labels.csv", index=False)

    utils.pretty_log("Extracting features (3/3)")

    feature_df = utils.extract_features(
        paths_df=paths_df,
        ID_colname="unique_ID",
        extraction_params="MR_default.yaml",
    )
    feature_df.to_csv(config.derived_table_dir / "features.csv", index=False)


if __name__ == "__main__":
    run_pipeline()
