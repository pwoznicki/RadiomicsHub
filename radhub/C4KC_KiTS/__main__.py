import logging
import shutil

from radhub import master_config, utils
from radhub.C4KC_KiTS import preprocess
from radhub.C4KC_KiTS.config import config

log = logging.getLogger(__name__)


def run_pipeline():

    master_config.configure_logging(config.log_dir)

    utils.pretty_log("Converting DICOM images to Nifti (1/4)")
    dicom_segs = [
        path
        for path in config.raw_data_dir.rglob("*.dcm")
        if "Segmentation" in path.parent.name
    ]
    dicom_img_dirs = set(
        path.parent
        for path in config.raw_data_dir.rglob("*.dcm")
        if not "Segmentation" in path.parent.name
    )

    conversion_paths = utils.convert_dicom_sitk(
        dicom_data=dicom_img_dirs,
        output_dir=config.base_dir / "derived" / "nifti-test",
        prefix="CT_",
        n_jobs=8,
    )
    conversion_df = utils.create_conversion_df(conversion_paths)
    conversion_df.to_csv(
        config.derived_table_dir / "conversion.csv", index=False
    )

    utils.pretty_log("Converting DICOM segmentations to Nifti (2/4)")
    utils.convert_dicom_seg_dataset(
        dicom_data=dicom_segs,
        nifti_seg_dir=config.derived_nifti_dir,
        suffix="arterial",
    )

    utils.pretty_log("Creating tables with paths and labels (3/4)")
    paths_df = preprocess.create_path_df(
        derived_nifti_dir=config.derived_nifti_dir
    )
    paths_df.to_csv(config.derived_table_dir / "paths.csv", index=False)

    shutil.copy(
        config.raw_table_dir / "clinical_data.csv",
        config.derived_table_dir / "labels.csv",
    )

    utils.pretty_log("Extracting features (4/4)")
    feature_df = utils.extract_features(
        paths_df=paths_df,
        ID_colname="unique_ID",
        extraction_params="CT_default.yaml",
    )
    feature_df.to_csv(config.derived_table_dir / "features.csv", index=False)


if __name__ == "__main__":
    run_pipeline()
