import re
import pandas as pd
from tqdm import tqdm


def expand_ref_df(df):
    df["RadID"] = df["RadID"].str.split(",")
    df["RadFindingID"] = df["RadFindingID"].str.split(",")
    df_expanded = df.explode(["RadID", "RadFindingID"])
    df_expanded["RadID"] = df_expanded["RadID"].astype(int)
    df_expanded["RadFindingID"] = df_expanded["RadFindingID"].astype(int)
    return df_expanded


def create_path_df(img_dir, seg_dir):
    seg_paths = list(seg_dir.glob("*.nii.gz"))
    seg_IDs, patient_IDs, reader_IDs = zip(
        *[
            re.findall(r"^((LNDb-\d{4})_rad(\d).*).nii.gz$", path.name)[0]
            for path in seg_paths
        ]
    )
    img_paths = [
        img_dir / f"{patient_ID}.nii.gz" for patient_ID in patient_IDs
    ]
    for path in img_paths:
        if not path.exists():
            raise FileNotFoundError(f"{path} does not exist.")

    path_df = pd.DataFrame(
        {
            "patient_ID": patient_IDs,
            "seg_ID": seg_IDs,
            "reader_ID": reader_IDs,
            "img_path": img_paths,
            "seg_path": seg_paths,
        }
    )
    path_df.sort_values(by=["patient_ID", "seg_ID"], inplace=True)
    return path_df
