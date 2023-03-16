import logging

import pandas as pd

from radhub import master_config, utils
from radhub.HCC_TACE import preprocess
from radhub.HCC_TACE.config import config

log = logging.getLogger(__name__)


def run_pipeline():

    master_config.configure_logging(config.log_dir)

    utils.pretty_log(
        "Converting DICOM images and segmentations to Nifti (1/4)"
    )
    conversion_paths = preprocess.convert_dataset(
        raw_data_dir=config.raw_data_dir,
        derived_nifti_dir=config.derived_nifti_dir,
    )

    utils.pretty_log("Extracting features (4/4)")


if __name__ == "__main__":
    run_pipeline()
