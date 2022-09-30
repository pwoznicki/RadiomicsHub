import config
from tqdm import tqdm

from radfeat import utils


def convert_dir(input_dir, output_dir):
    for raw_img_path in tqdm(input_dir.rglob("*.mha")):
        out_img_path = (
            output_dir
            / raw_img_path.parent.stem
            / (raw_img_path.stem + ".nii.gz")
        )
        utils.convert_sitk(raw_img_path, out_img_path)


if __name__ == "__main__":
    raw_img_dir = config.base_dir / "raw_img"
    out_img_dir = config.base_dir / "nifti_img"
    out_img_dir.mkdir(exist_ok=True, parents=True)
    convert_dir(raw_img_dir, out_img_dir)
