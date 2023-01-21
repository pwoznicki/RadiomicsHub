import logging
import pandas as pd

from radhub.PI_CAI import config

log = logging.getLogger(__name__)

sequences = ["t2w", "adc", "hbv"]
rois = [
    {
        "name": "prostate",
        "seg_dir": config.prostate_seg_dir,
        "annotator": "AI",
    },
    {
        "name": "lesion",
        "seg_dir": config.lesion_AI_seg_dir,
        "annotator": "AI",
    },
    {
        "name": "lesion",
        "seg_dir": config.lesion_human_seg_dir,
        "annotator": "human",
    },
]


def get_paths(label_df):
    paths = []
    for patient_ID, study_ID in label_df[["patient_id", "study_id"]].values:
        for roi in rois:
            for sequence in sequences:
                img_path = (
                    config.raw_data_dir
                    / "img"
                    / str(patient_ID)
                    / f"{patient_ID}_{study_ID}_{sequence}.mha"
                )
                seg_path = roi["seg_dir"] / f"{patient_ID}_{study_ID}.nii.gz"
                if not img_path.exists():
                    log.error(f"Image file not found: {img_path}")
                if not seg_path.exists():
                    log.error(f"Segmentation file not found: {seg_path}")
                    continue
                paths.append(
                    {
                        "patient_ID": patient_ID,
                        "study_ID": study_ID,
                        "ROI_ID": f"{patient_ID}_{study_ID}_{sequence}_{roi['name']}_{roi['annotator']}",
                        "ROI": roi["name"],
                        "sequence": sequence,
                        "annotator": roi["annotator"],
                        "img_path": str(img_path),
                        "seg_path": str(seg_path),
                    }
                )
    path_df = pd.DataFrame(paths)
    return path_df
