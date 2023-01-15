import logging
import subprocess

from pqdm.processes import pqdm

log = logging.getLogger(__name__)


def convert_dicom_img_to_nifti(dicom_img_dir, nifti_img_dir):
    if not dicom_img_dir.exists():
        raise FileNotFoundError(f"Directory not found: {dicom_img_dir}")
    nifti_img_dir.mkdir(parents=True, exist_ok=True)

    dicom_img_dirs = (
        child for child in dicom_img_dir.iterdir() if child.is_dir()
    )
    img_cmds = (
        f"dcm2niix -z y -f %i -o {nifti_img_dir.as_posix()} -i y {dicom_dir.as_posix()}"
        for dicom_dir in dicom_img_dirs
    )
    pqdm(img_cmds, convert_series, n_jobs=16)


def convert_dicom_seg_to_nifti(dicom_seg_dir, nifti_seg_dir):
    if not dicom_seg_dir.exists():
        raise FileNotFoundError(f"Directory not found: {dicom_seg_dir}")
    nifti_seg_dir.mkdir(parents=True, exist_ok=True)
    dicom_seg_dirs = (
        child for child in dicom_seg_dir.iterdir() if child.is_dir()
    )
    cmds = (
        f"dcm2niix -z y -f %i_%d -o {nifti_seg_dir.as_posix()} {dicom_dir.as_posix()}"
        for dicom_dir in dicom_seg_dirs
    )
    pqdm(cmds, convert_series, n_jobs=16)
    if not dicom_seg_dir.exists():
        raise FileNotFoundError(f"Directory not found: {dicom_seg_dir}")


def convert_series(cmd):
    try:
        subprocess.check_output(cmd.split())
        log.info(f"Conversion successful! (command: {cmd}")
    except subprocess.CalledProcessError:
        log.error(f"Conversion failed! (command: {cmd}")
