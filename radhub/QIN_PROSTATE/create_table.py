import logging
from pathlib import Path

import pandas as pd

log = logging.getLogger(__name__)


def get_paths(patient_dir: Path) -> pd.DataFrame:
    studies = [p for p in patient_dir.iterdir() if p.is_dir()]
    studies = sorted(studies, key=lambda p: p.name)

    assert len(studies) == 2, f"Expected 2 studies, found {len(studies)}"

    test_paths = get_study_paths(studies[0], timepoint="test")
    test_df = pd.DataFrame(test_paths)

    retest_paths = get_study_paths(studies[1], timepoint="retest")
    retest_df = pd.DataFrame(retest_paths)

    patient_df = pd.concat([test_df, retest_df], axis=0)

    return patient_df


def get_study_paths(study_dir: Path, timepoint: str) -> list[dict[str, str]]:
    patient_ID = study_dir.parts[-2]
    sequences = ["T2", "ADC", "DCE_SUB"]
    result = []
    for sequence in sequences:
        sequence_dir = study_dir / sequence
        img_path = sequence_dir / f"{sequence}.nii.gz"
        if not img_path.exists():
            raise FileNotFoundError(f"File not found: {img_path}")
        prostate_rois = [
            "whole_gland",
            "peripheral_zone",
            "tumor_pz",
            "normal_tissue_pz",
        ]
        for roi in prostate_rois:
            seg_path = sequence_dir / "segmentation" / f"{roi}.nii.gz"
            if not seg_path.exists():
                log.warning(f"File not found: {seg_path}")
                continue
            series_ROI_ID = f"{patient_ID}_{sequence}_{roi}_{timepoint}"
            result.append(
                {
                    "patient_ID": patient_ID,
                    "sequence": sequence,
                    "ROI": roi,
                    "test/retest": timepoint,
                    "series_ROI_ID": series_ROI_ID,
                    "img_path": str(img_path),
                    "seg_path": str(seg_path),
                }
            )
    return result


def create_ref_table(derived_nifti_dir: Path) -> pd.DataFrame:
    df = pd.DataFrame()
    for patient_dir in derived_nifti_dir.iterdir():
        if patient_dir.is_dir():
            patient_df = get_paths(patient_dir)
            df = pd.concat([df, patient_df], axis=0)
    df.sort_values(by=["patient_ID", "sequence", "ROI"], inplace=True)
    return df
