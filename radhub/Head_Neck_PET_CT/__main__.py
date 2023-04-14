import logging

import pandas as pd

from radhub import master_config, utils
from radhub.Head_Neck_PET_CT.config import config
from radhub.Head_Neck_PET_CT import preprocess

log = logging.getLogger(__name__)


def run_pipeline():
    master_config.configure_logging(config.log_dir)

    utils.pretty_log("Matching images and segmentations (1/4)")

    raw_path_df = preprocess.find_data(
        raw_dicom_dir=config.raw_data_dir,
    )
    raw_path_df.to_csv(config.derived_table_dir / "raw_paths.csv", index=False)

    utils.pretty_log(
        "Converting DICOM images and DICOM RT segmentations to Nifti (2/4)"
    )

    conversion_df = preprocess.convert_dataset(
        raw_path_df=raw_path_df,
        output_dir=config.derived_nifti_dir,
    )
    conversion_df.to_csv(
        config.derived_table_dir / "conversion.csv", index=False
    )

    utils.pretty_log("Creating tables with paths and labels (3/4)")

    contours_df = preprocess.load_contours_df(
        path=config.raw_table_dir / "INFO_GTVcontours_HN.xlsx",
    )
    path_df = preprocess.create_path_df(
        conversion_df=conversion_df,
        contours_df=contours_df,
    )
    path_df.to_csv(config.derived_table_dir / "paths.csv", index=False)

    label_df = pd.read_excel(
        config.raw_table_dir / "INFOclinical_HN_Version2_30may2018.xlsx"
    )
    label_df.to_csv(config.derived_table_dir / "labels.csv", index=False)

    utils.pretty_log("Extracting features (4/4)")

    feature_df = utils.extract_features(
        paths_df=path_df,
        ID_colname="unique_ID",
    )
    feature_df.to_csv(config.derived_table_dir / "features.csv", index=False)


if __name__ == "__main__":
    run_pipeline()
