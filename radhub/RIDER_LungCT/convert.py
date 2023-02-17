from radhub import utils
import subprocess
import logging

from tqdm import tqdm

from radhub import utils

log = logging.getLogger(__name__)


def convert_img_to_nifti(dicom_img_dir, save_dir, excluded_ids):
    dicom_dirs = [
        dicom_dir
        for dicom_dir in dicom_img_dir.iterdir()
        if not any(
            excluded_id in str(dicom_dir) for excluded_id in excluded_ids
        )
    ]
    utils.convert_dicom_to_nifti(
        dicom_dirs,
        save_dir,
        filename_pattern="%i_%j",
        ignore_derived=False,
    )


def convert_seg_to_nifti(dicom_seg_dir, save_dir, excluded_ids):
    """
    It is expected that this will fail for the RTStruct files
    (half of all seg files).
    """

    dicom_paths = [
        path
        for path in dicom_seg_dir.rglob("*.dcm")
        if not any(excluded_id in str(path) for excluded_id in excluded_ids)
    ]
    for dicom_path in tqdm(dicom_paths):
        id_ = dicom_path.parents[2].name
        print(dicom_path.parent.name)
        if "RETEST" in dicom_path.parent.name:
            timepoint = "RETEST"
        else:
            timepoint = "TEST"
        seg_save_dir = save_dir / f"{id_}_{timepoint}"
        seg_save_dir.mkdir(parents=True, exist_ok=True)
        cmd = [
            "segimage2itkimage",
            "--inputDICOM",
            dicom_path.as_posix(),
            "--outputDirectory",
            seg_save_dir.as_posix(),
            "-t",
            "nifti",
        ]
        try:
            subprocess.check_output(cmd)
            log.info(f"Conversion successful! (command: {(' ').join(cmd)}")
        except subprocess.CalledProcessError:
            log.error(f"Conversion failed! (command: {(' ').join(cmd)}")


def postprocess_segmentations(nifti_seg_dir):
    seg_paths = list(nifti_seg_dir.rglob("*.nii.gz"))
    for seg_path in tqdm(seg_paths):
        utils.binarize_segmentation(seg_path)
