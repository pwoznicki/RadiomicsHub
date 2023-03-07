import logging

import pandas as pd

from radhub import master_config, utils
from radhub.OPC_Radiomics import preprocess
from radhub.OPC_Radiomics.config import config

log = logging.getLogger(__name__)


def run_pipeline():

    master_config.configure_logging(config.log_dir)

    utils.pretty_log(
        "Converting DICOM images and segmentations to Nifti (1/4)"
    )
    conversion_df = preprocess.convert_dataset(
        dicom_dir=config.raw_data_dir,
        output_dir=config.derived_nifti_dir,
        n_jobs=7,
    )
    conversion_df.to_csv(
        config.derived_table_dir / "conversion.csv", index=False
    )

    utils.pretty_log("Extracting features (4/4)")


if __name__ == "__main__":
    run_pipeline()
