import logging

from radfeat import master_config
from radfeat.QIN_PROSTATE import convert, create_table, extract
from radfeat.QIN_PROSTATE.config import config

log = logging.getLogger(__name__)


def run_pipeline():

    master_config.configure_logging(config.log_dir)

    text = "Converting DICOM to NIfTI (1/3)"
    log.info(f"{text:#^80}")
    convert.convert_dicom_to_nifti(
        config.raw_data_dir, config.derived_nifti_dir
    )
    convert.postprocess_segmentations(config.derived_nifti_dir)

    text = "Creating reference table (2/3)"
    log.info(f"{text:#^80}")
    ref_table = create_table.create_ref_table(config.derived_nifti_dir)
    ref_table.to_csv(config.derived_table_dir / "paths.csv", index=False)

    text = "Extracting features (3/3)"
    log.info(f"{text:#^80}")
    feature_df = extract.extract_features(ref_table)
    feature_df.to_csv(config.derived_table_dir / f"features.csv", index=False)


if __name__ == "__main__":
    run_pipeline()
