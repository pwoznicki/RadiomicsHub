import logging

import pandas as pd

from radhub import master_config, utils
from radhub.Soft_tissue_Sarcoma import preprocess
from radhub.Soft_tissue_Sarcoma.config import config

log = logging.getLogger(__name__)


def run_pipeline():

    master_config.configure_logging(config.log_dir)

    utils.pretty_log("Converting DICOM and DICOM RT files to Nifti (1/3)")

    preprocess.convert_rtstruct_dataset(
        dicom_dir=config.raw_data_dir,
        output_dir=config.derived_nifti_dir,
    )

    utils.pretty_log("Creating a table with paths (2/3)")

    paths_df = preprocess.create_paths_df(
        config.derived_nifti_dir, config.base_dir
    )
    paths_df.to_csv(config.derived_table_dir / "paths.csv", index=False)

    raw_label_df = pd.read_excel(
        config.raw_table_dir / "INFOclinical_STS.xlsx"
    )
    raw_label_df.loc[:50].to_csv(
        config.derived_table_dir / "labels.csv", index=False
    )

    utils.pretty_log("Extracting features (3/3)")

    feature_df = utils.extract_features(
        paths_df=paths_df,
        ID_colname="unique_ID",
        root_dir=config.base_dir,
    )
    feature_df.to_csv(config.derived_table_dir / "features.csv", index=False)


if __name__ == "__main__":
    run_pipeline()
