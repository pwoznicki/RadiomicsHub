import logging

import pandas as pd

from radhub import master_config

log = logging.getLogger(__name__)


def run_pipeline():

    master_config.configure_logging(config.log_dir)

    text = " Converting DICOM images and segmentations to Nifti (1/4) "
    log.info(f"{text:#^80}")

    text = " Extracting features (4/4)"
    log.info(f"{text:#^80}")


if __name__ == "__main__":
    run_pipeline()
