import logging

import pandas as pd

from radhub import master_config, utils
from radhub.RIDER_LungCT.config import config, excluded_ids
from radhub.RIDER_LungCT import preprocess, convert


log = logging.getLogger(__name__)


def run_pipeline():

    master_config.configure_logging(config.log_dir)

    text = " Converting and renaming DICOM images to Nifti (1/4) "
    log.info(f"{text:#^80}")

    convert.convert_img_to_nifti(
        config.raw_data_dir / "img",
        config.derived_nifti_dir / "img",
        excluded_ids=excluded_ids,
    )
    preprocess.rename_images_with_timepoints(
        nifti_img_dir=config.derived_nifti_dir / "img",
        dicom_img_dir=config.raw_data_dir / "img",
    )

    text = " Converting and postprocessing DICOM segmentations to Nifti (2/4) "
    log.info(f"{text:#^80}")

    convert.convert_seg_to_nifti(
        config.raw_data_dir / "seg",
        config.derived_nifti_dir / "seg",
        excluded_ids=excluded_ids,
    )
    convert.postprocess_segmentations(config.derived_nifti_dir / "seg")

    text = " Creating a table with paths (3/4)"
    log.info(f"{text:#^80}")

    paths_df = preprocess.create_paths_df(
        config.derived_nifti_dir / "img", config.derived_nifti_dir / "seg"
    )
    paths_df.to_csv(config.derived_table_dir / "paths.csv", index=False)

    text = " Extracting features (4/4)"
    log.info(f"{text:#^80}")

    feature_df = utils.extract_features(
        paths_df=paths_df,
        ID_colname="unique_ID",
    )
    feature_df.to_csv(config.derived_table_dir / "features.csv", index=False)


if __name__ == "__main__":
    run_pipeline()
