from tqdm import tqdm

from radhub import utils


def convert_images(input_dir, output_dir):
    for raw_img_path in tqdm(list(input_dir.rglob("*.mha"))):
        out_img_path = (
            output_dir
            / raw_img_path.parent.stem
            / (raw_img_path.stem + ".nii.gz")
        )

        utils.convert_sitk(raw_img_path, out_img_path)
