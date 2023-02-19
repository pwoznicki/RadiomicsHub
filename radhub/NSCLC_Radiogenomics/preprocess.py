from pathlib import Path
import pandas as pd
import logging

log = logging.getLogger(__name__)


def find_studies(raw_dicom_dir: Path):
    seg_dirs = list(raw_dicom_dir.rglob("*/*ePAD*")) + list(
        raw_dicom_dir.rglob("*/*segmentation*")
    )
    log.info(f"Found {len(seg_dirs)} segmentation directories")
    study_dirs = set(path.parent for path in seg_dirs)
    ct_dirs = []
    for study_dir in study_dirs:
        candidate_ct_dirs = [
            path
            for path in study_dir.iterdir()
            if ("ePAD" not in path.name)
            and ("segmentation" not in path.name)
            and ("Eq_1" not in path.name)
        ]
        if len(candidate_ct_dirs) == 0:
            log.warning(f"No CT directory found for {study_dir}")
        elif len(candidate_ct_dirs) > 1:
            log.warning(
                f"Found multiple series for {study_dir}" "Choosing lung series"
            )
            candidate_ct_dirs = [
                path
                for path in candidate_ct_dirs
                if "lung" in path.name.lower()
            ]
            if len(candidate_ct_dirs) == 0:
                log.warning("Could not find lung series")
                continue
            elif len(candidate_ct_dirs) > 1:
                log.warning("Found multiple lung series")
        ct_dirs.extend(candidate_ct_dirs)

    return ct_dirs, seg_dirs


def create_paths_df(derived_nifti_dir: Path):
    img_paths = [
        path
        for path in derived_nifti_dir.rglob("img_*.nii.gz")
        if not "Eq_1" in path.name
    ]
    paths = []
    for img_path in img_paths:
        seg_path = img_path.parent / "seg.nii.gz"
        if not seg_path.exists():
            raise FileNotFoundError(f"Segmentation not found: {seg_path}")
        id_ = img_path.parent.name
        paths.append(
            {
                "case_ID": id_,
                "img_path": str(img_path),
                "seg_path": str(seg_path),
            }
        )
    result_df = pd.DataFrame(paths).sort_values("case_ID")

    return result_df


def create_label_df(raw_label_df):
    label_df = raw_label_df.copy().rename(columns={"Case ID": "case_ID"})

    return label_df
