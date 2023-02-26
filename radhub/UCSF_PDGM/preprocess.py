import logging
from pathlib import Path

import pandas as pd
from radhub.UCSF_PDGM import config

log = logging.getLogger(__name__)


def get_paths(
    case_dir: Path,
    sequence_name: str,
    roi: str,
) -> dict[str, str]:
    case_ID = case_dir.name.removesuffix("_nifti")
    img_path = case_dir / f"{case_ID}_{sequence_name}.nii.gz"
    seg_path = case_dir / f"{case_ID}_{roi}_segmentation.nii.gz"
    if not img_path.exists():
        log.info(f"Image file not found: {img_path}")
        raise FileNotFoundError(f"File not found: {img_path}")
    if not seg_path.exists():
        log.info(f"Segmentation file not found: {seg_path}")
        raise FileNotFoundError(f"File not found: {seg_path}")
    return {
        "patient_ID": case_ID,
        "sequence": sequence_name,
        "unique_ID": f"{case_ID}_{sequence_name}",
        "img_path": str(img_path),
        "seg_path": str(seg_path),
    }


def create_path_df(raw_nifti_dir: Path, roi: str) -> pd.DataFrame:
    ref_data = []
    for case_dir in raw_nifti_dir.iterdir():
        if not case_dir.is_dir():
            continue
        for sequence_name in config.sequences:
            try:
                ref_data.append(get_paths(case_dir, sequence_name, roi))
            except FileNotFoundError:
                pass
    ref_table = pd.DataFrame(ref_data).sort_values(
        by=["patient_ID", "sequence"]
    )
    return ref_table
