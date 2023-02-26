import logging
from typing import Sequence
import subprocess
from pathlib import Path

import SimpleITK as sitk
from autorad.data.dataset import ImageDataset
from autorad.feature_extraction.extractor import FeatureExtractor
from autorad.utils import io
from pqdm.threads import pqdm
from tqdm import tqdm
import nibabel as nib
import numpy as np

logging.getLogger().setLevel(logging.CRITICAL)

log = logging.getLogger(__name__)


def pretty_log(text):
    text = f" {text} "
    log.info(f"{text:#^80}")


def binarize_segmentations(nifti_data: Path | Sequence[Path], n_jobs=4):
    if isinstance(nifti_data, Path):
        seg_paths = list(nifti_data.rglob("*.nii.gz"))
    else:
        seg_paths = nifti_data
    for seg_path in tqdm(seg_paths):
        binarize_segmentation(seg_path)


def binarize_segmentation(nifti_path: Path):
    img = nib.load(nifti_path)
    arr = img.get_fdata()
    arr = (arr > 0).astype(np.uint8)
    new_img = nib.Nifti1Image(arr, img.affine, img.header)
    nib.save(new_img, nifti_path)


def read_dicom_sitk(input_dir: Path) -> sitk.Image:
    reader = sitk.ImageSeriesReader()

    dicom_names = reader.GetGDCMSeriesFileNames(str(input_dir))
    reader.SetFileNames(dicom_names)

    image = reader.Execute()

    return image


def convert_dicom_seg_dataset(
    dicom_data: Path | Sequence[Path],
    nifti_seg_dir: Path,
    suffix="",
):
    dicom_dirs = get_dicom_dirs(dicom_data)
    for dicom_dir in dicom_dirs:
        seg_sitk = io.read_dicom_seg_sitk(dicom_dir)
        id_ = dicom_dir.parents[2].name
        output_dir = nifti_seg_dir / id_
        output_dir.mkdir(parents=True, exist_ok=True)
        sitk.WriteImage(seg_sitk, str(output_dir / f"seg_{suffix}.nii.gz"))


def get_dicom_dirs(dicom_data: Path | Sequence[Path]):
    if isinstance(dicom_data, Path):
        if not dicom_data.exists():
            raise FileNotFoundError(f"Directory not found: {dicom_data}")
        dicom_dirs = (
            child for child in dicom_data.iterdir() if child.is_dir()
        )
    else:
        dicom_dirs = dicom_data
    return dicom_dirs


def convert_dicom_to_nifti(
    dicom_data: Path | Sequence[Path],
    nifti_img_dir,
    filename_pattern="%i",
    *dcm2niix_args,
    ignore_derived=True,
    n_jobs=4,
):
    dicom_dirs = get_dicom_dirs(dicom_data)
    nifti_img_dir.mkdir(parents=True, exist_ok=True)
    if ignore_derived:
        dcm2niix_args = list(dcm2niix_args) + ["-i", "y"]
    img_cmds = (
        [
            "dcm2niix",
            "-z",
            "y",
            "-f",
            filename_pattern,
            "-o",
            nifti_img_dir.as_posix(),
            *dcm2niix_args,
            dicom_dir.as_posix(),
        ]
        for dicom_dir in dicom_dirs
    )
    pqdm(img_cmds, convert_series, n_jobs=n_jobs)


def convert_dicom_to_nifti_imported(
    dicom_dir: Path, output_path: Path, converter: str = "dcm2niix"
):
    """
    Convert directory containing one dicom series into compressed nifti
    Args:
        dicom_dir (Path): Path to the dicom directory
        output_path (Path): Path to the output nifti file
        converter (str): Converter to use. Either "plastimatch" or "dcm2niix"
    """
    dicom_dir = Path(dicom_dir)
    output_path = Path(output_path)
    if converter == "plastimatch":
        cmd = (
            f"plastimatch convert --input {dicom_dir.absolute()} "
            f"--output-img {output_path.absolute()}"
        )
    elif converter == "dcm2niix":
        do_compression = "y" if output_path.name.endswith(".nii.gz") else "n"
        cmd = (
            f"dcm2niix -z {do_compression} -f {output_path.name.split('.')[0]} -o"
            f" {output_path.parent.absolute()} -i y {dicom_dir.absolute()}"
        )
    else:
        raise ValueError(f"Converter {converter} not found!")

    log.info(f"Converting {dicom_dir} to {output_path} with {converter}")
    log.info(f"Command: {cmd}")

    try:
        output = subprocess.check_output(cmd.split())
    except RuntimeError:
        log.error(f"Conversion to nifti with dcm2niix failed for {dicom_dir}")


def convert_series(cmd: list[str]):
    try:
        subprocess.check_output(cmd)
        log.info(f"Conversion successful! (command: {cmd}")
    except subprocess.CalledProcessError as e:
        log.error(f"Conversion failed! (command: {cmd}")
        log.error(f"Error: {e.output}")


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
    root_dir=None,
    n_jobs=-1,
    mask_label=None,
):
    image_dset = ImageDataset(
        paths_df,
        ID_colname=ID_colname,
        image_colname=image_colname,
        mask_colname=mask_colname,
        root_dir=root_dir,
    )
    extractor = FeatureExtractor(
        image_dset,
        extraction_params=extraction_params,
        n_jobs=n_jobs,
    )
    feature_df = extractor.run(mask_label=mask_label)
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
