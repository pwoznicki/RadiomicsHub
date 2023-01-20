import logging

import pandas as pd

from radfeat import master_config
from radfeat.PI_CAI.config import config
from radfeat.PI_CAI import convert

log = logging.getLogger(__name__)


def run_pipeline():

    master_config.configure_logging(config.log_dir)

    text = " Converting .mha images to .nii.gz (1/4) "
    log.info(f"{text:#^80}")

    raw_img_dir = config.raw_data_dir / "img"
    out_img_dir = config.derived_nifti_dir / "img"
    convert.convert_images(raw_img_dir, out_img_dir)

    text = " Extracting features (4/4)"
    log.info(f"{text:#^80}")


if __name__ == "__main__":
    run_pipeline()
