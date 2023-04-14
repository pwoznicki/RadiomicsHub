import logging

import pandas as pd

from radhub import master_config, utils
from radhub.HNSCC.config import config
from radhub.HNSCC import preprocess

log = logging.getLogger(__name__)


def run_pipeline():
    master_config.configure_logging(config.log_dir)

    utils.pretty_log(
        "Converting DICOM images and segmentations to Nifti (1/3)"
    )
    conversion_df = preprocess.convert_dataset(
        raw_dicom_dir=config.raw_data_dir,
        derived_nifti_dir=config.derived_nifti_dir,
        n_jobs=16,
    )
    conversion_df.to_csv(
        config.derived_table_dir / "conversion.csv", index=False
    )

    utils.pretty_log("Creating tables with paths and labels (2/3)")

    paths_df = preprocess.create_paths_df(config.derived_nifti_dir)
    paths_df.to_csv(config.derived_table_dir / "paths.csv", index=False)

    atlas_label_df = pd.read_excel(
        config.raw_table_dir / "Patient and Treatment Characteristics.xls"
    )
    atlas_label_df.to_csv(
        config.derived_table_dir / "labels_HN_Cancer_Atlas.csv", index=False
    )

    opc_label_df = pd.read_csv(
        config.raw_table_dir
        / "Radiomics_Outcome_Prediction_in_OPC_ASRM_corrected.csv"
    )
    opc_label_df.to_csv(
        config.derived_table_dir / "labels_OPC.csv", index=False
    )

    utils.pretty_log("Extracting features (3/3)")
    feature_df = utils.extract_features(
        paths_df=paths_df,
        ID_colname="unique_ID",
        n_jobs=16,
    )
    feature_df.to_csv(config.derived_table_dir / "features.csv", index=False)


if __name__ == "__main__":
    run_pipeline()
