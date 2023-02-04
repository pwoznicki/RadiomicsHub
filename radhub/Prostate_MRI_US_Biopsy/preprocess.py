import pandas as pd

import config
import logging

log = logging.getLogger(__name__)


def get_image_path(image_dir, patient_ID, series_UID):
    result = image_dir / patient_ID / (series_UID + ".nii.gz")
    if not result.exists():
        print(f"Image path does not exist: {result}")
        return None
    return str(result)


def get_mask_path(mask_dir, patient_ID, series_UID, roi):
    # mask_dir = config.DATA_DIR / "prostate-ucla" / "masks" / "nifti"
    if roi == "prostate":
        result = mask_dir / patient_ID / f"ProstateSurface_{series_UID}.nii.gz"
    elif roi == "lesion":
        result = mask_dir / patient_ID / f"Target1_{series_UID}.nii.gz"
    else:
        raise ValueError("Unknown ROI:", roi)
    if not result.exists():
        log.warning(f"Mask path does not exist: {result}")
        return None
    return str(result)


def create_path_df(biopsy_df, image_dir, mask_dir):
    biopsy_df["gleason"] = (
        biopsy_df["Primary Gleason"] + biopsy_df["Secondary Gleason"]
    )
    biopsy_df.dropna(subset=["Series Instance UID (MRI)"], inplace=True)
    biopsy_df["gleason"].fillna(value=0, inplace=True)
    patient_df = (
        biopsy_df.groupby(by="Series Instance UID (MRI)").max().reset_index()
    )

    patient_df["img_path"] = patient_df.apply(
        lambda x: get_image_path(
            image_dir, x["Patient Number"], x["Series Instance UID (MRI)"]
        ),
        axis=1,
    )
    patient_df["prostate_mask_path"] = patient_df.apply(
        lambda x: get_mask_path(
            mask_dir,
            x["Patient Number"],
            x["Series Instance UID (MRI)"],
            roi="prostate",
        ),
        axis=1,
    )
    patient_df["lesion_mask_path"] = patient_df.apply(
        lambda x: get_mask_path(
            mask_dir,
            x["Patient Number"],
            x["Series Instance UID (MRI)"],
            roi="lesion",
        ),
        axis=1,
    )
    meta_df = (
        patient_df[
            [
                "Patient Number",
                "Series Instance UID (MRI)",
                "gleason",
                "img_path",
                "prostate_mask_path",
                "lesion_mask_path",
            ]
        ]
        .rename(
            {
                "Patient Number": "patient_ID",
                "Series Instance UID (MRI)": "img_series_instance_UID",
                "gleason": "max_gleason",
            },
            axis="columns",
        )
        .sort_values(by="patient_ID")
        .dropna()
    )
    label_df = meta_df[
        ["patient_ID", "img_series_instance_UID", "max_gleason"]
    ]
    path_df = meta_df.drop(columns=["max_gleason"])
    # path_df = pd.melt(
    #     meta_df,
    #     id_vars=["patient_ID", "img_series_instance_UID", "img_path"],
    #     value_vars=["prostate", "lesion"],
    #     var_name="ROI",
    #     value_name="seg_path",
    # )
    # path_df["unique_ID"] = path_df.apply(
    #     lambda x: f"{x['ROI']}_{x['img_series_instance_UID']}",
    #     axis=1,
    # )
    # path_df.sort_values(by=["patient_ID", "ROI"], inplace=True)
    # path_df = path_df[
    #     [
    #         "patient_ID",
    #         "ROI",
    #         "img_series_instance_UID",
    #         "unique_ID",
    #         "img_path",
    #         "seg_path",
    #     ]
    # ]

    return path_df, label_df


if __name__ == "__main__":
    main()
