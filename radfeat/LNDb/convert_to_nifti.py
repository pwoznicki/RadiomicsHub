import config
from tqdm import tqdm

from radfeat import utils


def convert_dir(input_dir, output_dir):
    for img_path in tqdm(input_dir.glob("*.mhd")):
        out_img_path = output_dir / (img_path.name.split(".")[0] + ".nii.gz")
        utils.convert_sitk(img_path, out_img_path)


def convert_mhd_to_nifti(data_dir):
    img_dir = data_dir / "raw_img"
    out_img_dir = data_dir / "nifti_img"
    convert_dir(img_dir, out_img_dir)

    seg_dir = data_dir / "raw_seg"
    out_seg_dir = data_dir / "nifti_seg"
    convert_dir(seg_dir, out_seg_dir)


if __name__ == "__main__":
    convert_mhd_to_nifti(config.base_dir)
