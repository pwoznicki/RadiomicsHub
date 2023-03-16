import logging
from pathlib import Path

import pandas as pd
from tqdm import tqdm

from radhub import utils

log = logging.getLogger(__name__)


def create_paths_df(derived_nifti_dir: Path):
    paths = []
    for patient_dir in tqdm(derived_nifti_dir.iterdir()):
        patient_id = patient_dir.name
        for roi in ["Liver", "Mass", "Portal_vein", "Abdominal_aorta"]:
            img_path = patient_dir / "img_phase2.nii.gz"
            if not img_path.exists():
                log.warning(f"Image not found for {img_path}. Skipping.")
            seg_path = patient_dir / f"seg_{roi}.nii.gz"
            paths.append(
                {
                    "patient_ID": patient_id,
                    "ROI": roi,
                    "unique_ID": f"{patient_id}_{roi}",
                    "img_path": str(img_path),
                    "seg_path": str(seg_path),
                }
            )
    paths_df = pd.DataFrame(paths).sort_values(by="patient_ID")
    return paths_df
