import logging

from radfeat import master_config
from radfeat.LIDC_IDRI import convert
from radfeat.LIDC_IDRI.config import config

log = logging.getLogger(__name__)


def run_pipeline():

    master_config.configure_logging(config.log_dir)

    # text = " Converting DICOM images to Nifti (1/4) "
    # log.info(f"{text:#^80}")

    # convert.convert_dicom_img_to_nifti(
    #     config.raw_data_dir / "img",
    #     config.derived_nifti_dir / "img",
    # )

    text = " Converting DICOM segmentations to Nifti (2/4) "
    log.info(f"{text:#^80}")

    convert.convert_dicom_seg_to_nifti(
        config.raw_data_dir / "seg",
        config.derived_nifti_dir / "seg",
    )


if __name__ == "__main__":
    run_pipeline()
