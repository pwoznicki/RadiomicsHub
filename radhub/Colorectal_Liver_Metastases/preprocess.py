from pathlib import Path
from radhub import utils
import pandas as pd


def convert_dataset(raw_dicom_dir, derived_nifti_dir, n_jobs=8):
    seg_dirs = list(raw_dicom_dir.glob("**/*Segmentation*"))
    img_paths = [d for d in raw_dicom_dir.glob("*/*/*") if d not in seg_dirs]
    seg_paths = [d / "1-1.dcm" for d in seg_dirs]
    seg_conversion_df = utils.convert_seg_dataset(
        raw_seg_paths=seg_paths,
        output_dir=derived_nifti_dir,
        n_jobs=n_jobs,
    )
    img_conversion_df = utils.convert_dataset_sitk(
        dicom_data=img_paths,
        output_dir=derived_nifti_dir,
        out_fname="CT",
        n_jobs=n_jobs,
    )

    conversion_df = pd.concat([img_conversion_df, seg_conversion_df])

    return conversion_df


def create_paths_df(derived_nifti_dir):
    paths = []
    for case_dir in derived_nifti_dir.iterdir():
        patient_ID = case_dir.name
        seg_paths = list(case_dir.glob("seg_*.nii.gz"))
        for seg_path in seg_paths:
            roi = seg_path.name.removeprefix("seg_").removesuffix(".nii.gz")
            img_path = case_dir / "CT.nii.gz"
            paths.append(
                {
                    "patient_ID": patient_ID,
                    "ROI": roi,
                    "unique_ID": f"{patient_ID}_{roi}",
                    "img_path": str(img_path),
                    "seg_path": str(seg_path),
                }
            )
    paths_df = pd.DataFrame(paths).sort_values("unique_ID")
    return paths_df
