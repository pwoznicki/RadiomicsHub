from tqdm import tqdm
import numpy as np
import SimpleITK as sitk

import logging
from radhub import utils

log = logging.getLogger(__name__)


def convert_segmentations(input_dir, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    log.info(f"Converting segmentations from {input_dir} to {output_dir}...")
    for raw_seg_path in tqdm(list(input_dir.glob("*.nii.gz"))):
        img = sitk.ReadImage(str(raw_seg_path))
        arr = sitk.GetArrayFromImage(img)

        new_arr = (arr > 0).astype(np.uint8)
        new_img = utils.sitk_array_to_image(new_arr, img)

        out_img_path = output_dir / (raw_seg_path.stem + ".nii.gz")
        sitk.WriteImage(new_img, str(out_img_path))
