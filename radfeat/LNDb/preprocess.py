import re
from pathlib import Path

import nibabel as nib
import numpy as np
import pandas as pd
from tqdm import tqdm

import config


def expand_ref_df(df):
    df["RadID"] = df["RadID"].str.split(",")
    df["RadFindingID"] = df["RadFindingID"].str.split(",")
    df_expanded = df.explode(["RadID", "RadFindingID"])
    df_expanded["RadID"] = df_expanded["RadID"].astype(int)
    df_expanded["RadFindingID"] = df_expanded["RadFindingID"].astype(int)
    return df_expanded


def get_finding_id(lndb_id, rad_id, rad_finding_id, ref_df):
    matches = ref_df.loc[
        (ref_df["LNDbID"] == lndb_id)
        & (ref_df["RadID"] == rad_id)
        & (ref_df["RadFindingID"] == rad_finding_id),
        "FindingID",
    ]
    if len(matches) == 0:
        raise ValueError(
            f"No match found for LNDbID {lndb_id}, RadID {rad_id}, RadFindingID {rad_finding_id}"
        )
    elif len(matches) > 1:
        raise ValueError(
            f"Multiple matches found for LNDbID {lndb_id}, RadID {rad_id}, RadFindingID {rad_finding_id}"
        )
    return matches.iloc[0]


def separate_findings(finding_mask_path, out_dir, ref_df):
    if not finding_mask_path.exists():
        raise FileNotFoundError(f"{finding_mask_path} does not exist.")
    Path(out_dir).mkdir(exist_ok=True)
    full_lndb_id, lndb_id, rad_id = re.findall(
        r"^(LNDb-0*(\d*))_rad(\d).*", finding_mask_path.name
    )[0]
    lndb_id = int(lndb_id)
    rad_id = int(rad_id)
    finding_mask = nib.load(finding_mask_path)
    finding_mask_arr = finding_mask.get_fdata()
    n_findings = int(finding_mask_arr.max())
    for rad_finding_id in range(1, n_findings + 1):
        single_finding_arr = (finding_mask_arr == rad_finding_id).astype(
            np.uint8
        )
        single_finding_mask = nib.Nifti1Image(
            single_finding_arr, finding_mask.affine
        )
        finding_id = get_finding_id(lndb_id, rad_id, rad_finding_id, ref_df)
        nib.save(
            single_finding_mask,
            out_dir / f"{full_lndb_id}_rad{rad_id}_finding{finding_id}.nii.gz",
        )


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


if __name__ == "__main__":
    img_dir = config.base_dir / "nifti_img"
    seg_dir = config.base_dir / "nifti_seg"
    seg_separated_dir = config.base_dir / "nifti_seg_separated"
    ref_df = pd.read_csv(config.table_dir / "trainNodules_gt.csv")
    ref_df_expanded = expand_ref_df(ref_df)
    ref_df_expanded.to_csv(
        config.table_dir / "trainNodules_gt_expanded.csv", index=False
    )
    # for mask_path in tqdm(seg_dir.glob("*.nii.gz")):
    #    separate_findings(mask_path, seg_separated_dir, ref_df_expanded)
    path_df = create_path_df(img_dir, seg_separated_dir)
    path_df.to_csv(config.table_dir / "paths.csv", index=False)
