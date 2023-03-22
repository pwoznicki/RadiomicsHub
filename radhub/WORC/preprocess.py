from pathlib import Path

import config
import pandas as pd


def get_mask_suffix(subject):
    if subject.startswith("CRLM"):
        return "_lesion0_RAD"
    elif (
        subject.startswith("Melanoma")
        or subject in config.subjects_with_two_segmentations
    ):
        return "_lesion0"
    return ""


def create_path_df_for_single_dataset(
    dataset_name: str, raw_label_df: pd.DataFrame, dataset_dir: Path
):
    df_dataset = raw_label_df[raw_label_df["Dataset"] == dataset_name].copy()
    result_dict = {
        "subject_ID": [],
        "img_path": [],
        "seg_path": [],
    }
    for _, row in df_dataset.iterrows():
        subject = row["Subject"]
        modality = get_modality(row)

        dir_path = (
            Path(dataset_dir)
            / "raw"
            / "nifti"
            / (f"{subject}_{modality}")
            / "1"
            / "NIFTI"
        )
        image_path, mask_path = get_image_and_mask_paths(dir_path, subject)

        result_dict["subject_ID"].append(subject)
        result_dict["img_path"].append(image_path.as_posix())
        result_dict["seg_path"].append(mask_path.as_posix())
    path_df = pd.DataFrame(result_dict)

    return path_df, df_dataset


def get_image_and_mask_paths(dir_path, subject):
    image_path = dir_path / "image.nii.gz"
    mask_suffix = get_mask_suffix(subject)
    mask_path = dir_path / f"segmentation{mask_suffix}.nii.gz"
    if not image_path.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")
    if not mask_path.exists():
        raise FileNotFoundError(f"Mask file not found: {mask_path}")

    return image_path, mask_path


def get_modality(row):
    if row["CT Sessions"] == 1:
        return "CT"
    elif row["MR Sessions"] == 1:
        return "MR"
    else:
        raise ValueError(f"No modality found for Subject: {row.Subject}")
