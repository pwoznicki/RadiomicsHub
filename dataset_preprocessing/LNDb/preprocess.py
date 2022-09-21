import re
from pathlib import Path

import nibabel as nib
import numpy as np
from tqdm import tqdm

import config


def separate_nodules(nodule_mask_path, out_dir):
    if not nodule_mask_path.exists():
        raise FileNotFoundError(f"{nodule_mask_path} does not exist.")
    Path(out_dir).mkdir(exist_ok=True)
    lndb_id, rad_id = re.findall(r"(.*)_rad(\d).*", nodule_mask_path.name)[0]
    nodule_mask = nib.load(nodule_mask_path)
    nodule_mask_arr = nodule_mask.get_fdata()
    n_nodules = int(nodule_mask_arr.max())
    for nodule_id in range(1, n_nodules + 1):
        single_nodule_arr = (nodule_mask_arr == nodule_id).astype(np.uint8)
        single_nodule_mask = nib.Nifti1Image(
            single_nodule_arr, nodule_mask.affine
        )
        nib.save(
            single_nodule_mask,
            out_dir / f"{lndb_id}_rad{rad_id}_nodule{nodule_id}.nii.gz",
        )


if __name__ == "__main__":
    nifti_seg_dir = config.base_dir / "nifti_seg"
    out_dir = config.base_dir / "nifti_seg_separated"
    for mask_path in tqdm(nifti_seg_dir.glob("*.nii.gz")):
        separate_nodules(mask_path, out_dir)
