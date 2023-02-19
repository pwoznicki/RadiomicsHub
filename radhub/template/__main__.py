import logging

import pandas as pd

from radhub import master_config, utils

log = logging.getLogger(__name__)


def run_pipeline():

    master_config.configure_logging(config.log_dir)

    utils.pretty_log(
        "Converting DICOM images and segmentations to Nifti (1/4)"
    )

    utils.pretty_log("Extracting features (4/4)")


if __name__ == "__main__":
    run_pipeline()
