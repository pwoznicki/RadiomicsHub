import logging
import subprocess
from pathlib import Path

import SimpleITK as sitk
from autorad.data.dataset import ImageDataset
from autorad.feature_extraction.extractor import FeatureExtractor
from fire import Fire
from pqdm.threads import pqdm
from tqdm import tqdm

logging.getLogger().setLevel(logging.CRITICAL)

log = logging.getLogger(__name__)


def convert_dicom_img_to_nifti(
    dicom_img_dir, nifti_img_dir, filename_pattern="%i"
):
    if not dicom_img_dir.exists():
        raise FileNotFoundError(f"Directory not found: {dicom_img_dir}")
    nifti_img_dir.mkdir(parents=True, exist_ok=True)

    dicom_img_dirs = (
        child for child in dicom_img_dir.iterdir() if child.is_dir()
    )
    img_cmds = (
        [
            "dcm2niix",
            "-z",
            "y",
            "-f",
            filename_pattern,
            "-o",
            nifti_img_dir.as_posix(),
            "-i",
            "y",
            dicom_dir.as_posix(),
        ]
        for dicom_dir in dicom_img_dirs
    )
    pqdm(img_cmds, convert_series, n_jobs=16)


def convert_series(cmd: list[str]):
    try:
        subprocess.check_output(cmd)
        log.info(f"Conversion successful! (command: {cmd}")
    except subprocess.CalledProcessError:
        log.error(f"Conversion failed! (command: {cmd}")


def convert_dir_sitk(
    input_dir: str,
    output_dir: str,
    ext_from: str = ".mhd",
    ext_to: str = ".nii.gz",
):
    for img_path in tqdm(list(Path(input_dir).glob("*" + ext_from))):
        out_img_path = Path(output_dir) / (
            img_path.name.split(".")[0] + ext_to
        )
        convert_sitk(img_path, out_img_path)


def extract_features(
    paths_df,
    ID_colname,
    extraction_params="CT_default.yaml",
    image_colname="img_path",
    mask_colname="seg_path",
    n_jobs=-1,
):
    image_dset = ImageDataset(
        paths_df,
        ID_colname=ID_colname,
        image_colname=image_colname,
        mask_colname=mask_colname,
    )
    extractor = FeatureExtractor(
        image_dset,
        extraction_params=extraction_params,
        n_jobs=n_jobs,
    )
    feature_df = extractor.run()
    return feature_df


def convert_sitk(in_path, out_path):
    if not Path(in_path).exists():
        raise FileNotFoundError(f"File {in_path} does not exist")
    data = sitk.ReadImage(str(in_path))
    Path(out_path).parent.mkdir(exist_ok=True, parents=True)
    sitk.WriteImage(data, str(out_path))


def sitk_array_to_image(arr, ref_img):
    """
    Convert a NumPy array to a SimpleITK image, using the reference image's
    metadata.
    """
    img = sitk.GetImageFromArray(arr)
    img.CopyInformation(ref_img)
    return img


if __name__ == "__main__":
    Fire()
