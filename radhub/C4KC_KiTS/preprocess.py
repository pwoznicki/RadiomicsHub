from pathlib import Path

import pandas as pd


def create_path_df(derived_nifti_dir):
    results = []
    for case_dir in derived_nifti_dir.iterdir():
        if not case_dir.is_dir():
            pass
        patient_ID = case_dir.name

        ref_img_path = case_dir / "CT_arterial.nii.gz"
        ref_seg_path = case_dir / "seg_arterial.nii.gz"

        if patient_ID == "KiTS-00145":
            ref_img_path = case_dir / "CT_ARTERIAL_SOFT.nii.gz"

        assert ref_img_path.exists()
        assert ref_seg_path.exists()

        results.append(
            {
                "patient_ID": patient_ID,
                "phase": "arterial",
                "unique_ID": f"{patient_ID}_arterial",
                "img_path": str(ref_img_path),
                "seg_path": str(ref_seg_path),
            }
        )

        for phase in ["noncontrast", "late"]:
            img_path = case_dir / f"CT_{phase}.nii.gz"
            if not img_path.exists():
                continue
            results.append(
                {
                    "patient_ID": patient_ID,
                    "phase": phase,
                    "unique_ID": f"{patient_ID}_{phase}",
                    "img_path": str(img_path),
                    "seg_path": str(ref_seg_path),
                }
            )

    result_df = pd.DataFrame(results).sort_values("unique_ID")
    return result_df
