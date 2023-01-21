from tqdm import tqdm
import re
from pathlib import Path
import SimpleITK as sitk

from radhub import utils
import numpy as np


def convert_images(input_dir, output_dir):
    for img_path in tqdm(list(input_dir.glob("*.mhd"))):
        out_img_path = output_dir / (img_path.name.split(".")[0] + ".nii.gz")
        utils.convert_sitk(img_path, out_img_path)


def convert_and_separate_masks_all(
    raw_seg_dir, derived_seg_dir, expanded_ref_df
):
    for finding_mask_path in tqdm(list(raw_seg_dir.glob("*.mhd"))):
        convert_and_separate_mask(
            finding_mask_path, derived_seg_dir, expanded_ref_df
        )


def convert_and_separate_mask(finding_mask_path, out_dir, ref_df):
    if not finding_mask_path.exists():
        raise FileNotFoundError(f"{finding_mask_path} does not exist.")
    Path(out_dir).mkdir(exist_ok=True)

    full_lndb_id, lndb_id, rad_id = re.findall(
        r"^(LNDb-0*(\d*))_rad(\d).*", finding_mask_path.name
    )[0]
    lndb_id = int(lndb_id)
    rad_id = int(rad_id)

    finding_mask = sitk.ReadImage(str(finding_mask_path))
    finding_mask_arr = sitk.GetArrayFromImage(finding_mask)
    n_findings = int(finding_mask_arr.max())

    for rad_finding_id in range(1, n_findings + 1):
        single_finding_arr = (finding_mask_arr == rad_finding_id).astype(
            np.uint8
        )
        single_finding_mask = utils.sitk_array_to_image(
            single_finding_arr, finding_mask
        )
        finding_id = get_finding_id(lndb_id, rad_id, rad_finding_id, ref_df)
        save_path = (
            out_dir / f"{full_lndb_id}_rad{rad_id}_finding{finding_id}.nii.gz"
        )
        sitk.WriteImage(
            single_finding_mask,
            str(save_path),
        )


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
