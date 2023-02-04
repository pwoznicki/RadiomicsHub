import logging

import pandas as pd

from radhub import master_config, utils

from radhub.Prostate_MRI_US_Biopsy.config import config
from radhub.Prostate_MRI_US_Biopsy import convert, preprocess

log = logging.getLogger(__name__)


def run_pipeline():

    master_config.configure_logging(config.log_dir)

    # text = " Converting DICOM images and segmentations to Nifti (1/4) "
    # log.info(f"{text:#^80}")

    # dicom_paths = convert.find_relevant_MRI_series(
    #     config.raw_data_dir / "dicom"
    # )
    # convert.convert_dicom_img_to_nifti(
    #     dicom_paths,
    #     config.derived_nifti_dir / "img",
    #     filename_pattern="%i\/%j",
    # )

    # text = " Converting STL segmentations to Nifti (2/4) "
    # log.info(f"{text:#^80}")

    # convert.convert_segmentations(
    #     stl_dir=config.raw_data_dir / "stl",
    #     img_dir=config.derived_nifti_dir / "img",
    #     out_dir=config.derived_nifti_dir / "seg",
    # )

    text = " Creating table with paths (3/4) "
    log.info(f"{text:#^80}")

    biopsy_df = pd.read_excel(str(config.raw_table_dir / "biopsy.xlsx"))
    path_df, label_df = preprocess.create_path_df(
        biopsy_df,
        config.derived_nifti_dir / "img",
        config.derived_nifti_dir / "seg",
    )
    path_df.to_csv(config.derived_table_dir / "paths.csv", index=False)
    label_df.to_csv(config.derived_table_dir / "labels.csv", index=False)

    text = " Extracting features (4/4) "
    log.info(f"{text:#^80}")

    for ROI in ["lesion", "prostate"]:
        feature_df = utils.extract_features(
            path_df,
            ID_colname="img_series_instance_UID",
            extraction_params="MR_default.yaml",
            mask_colname=f"{ROI}_mask_path",
        )
        feature_df.to_csv(
            config.derived_table_dir / f"features_{ROI}.csv", index=False
        )


if __name__ == "__main__":
    run_pipeline()
