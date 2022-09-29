from pathlib import Path
import pandas as pd
import config

sequences = ["t2w", "adc", "hbv"]
seg_rois = {
        "prostate": config.prostate_mask_dir, 
        "lesion": config.lesion_mask_dir
    }

def get_paths(label_df):
    paths = []
    for patient_ID, study_ID in label_df[["patient_id", "study_id"]].values:
        for seg_roi, seg_dir in seg_rois.items():
            for sequence in sequences:
                img_path = config.img_dir / str(patient_ID) / f"{patient_ID}_{study_ID}_{sequence}.mha"
                seg_path = seg_dir / f"{patient_ID}_{study_ID}.nii.gz"
                if not img_path.exists():
                    print(f"Image file not found: {img_path}")
                    raise FileNotFoundError(f"File not found: {img_path}")
                if not seg_path.exists():
                    print(f"Segmentation file not found: {seg_path}")
                    raise FileNotFoundError(f"File not found: {seg_path}")
                paths.append({
                    "patient_ID": patient_ID,
                    "study_ID": study_ID,
                    "unique_ID": f"{patient_ID}_{study_ID}_{sequence}_{seg_roi}",
                    "ROI": seg_roi,
                    "sequence": sequence,
                    "img_path": str(img_path),
                    "seg_path": str(seg_path),
                })
    path_df = pd.DataFrame(paths)
    return path_df


if __name__ == "__main__":
    label_df = pd.read_csv(config.label_table_path)
    path_df = get_paths(label_df)
    path_df.to_csv(config.table_dir / "paths.csv", index=False)

