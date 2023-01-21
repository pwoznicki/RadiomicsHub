import json
import logging
import subprocess
from pathlib import Path

import nibabel as nib
import numpy as np
from tqdm import tqdm

log = logging.getLogger(__name__)


sequence_map = {
    "Apparent Diffusion Coefficient": "ADC",
    "T2 Weighted Axial": "T2",
    "DCE Subtraction": "DCE_SUB",
    "DCE": "DCE",
    "DWI": "DWI",
}


def convert_dicom_to_nifti(input_dir: Path, output_dir: Path):
    if not input_dir.exists():
        raise FileNotFoundError(f"Directory not found: {input_dir}")
    dicom_files = list(input_dir.rglob("*.dcm"))
    if not dicom_files:
        raise FileNotFoundError(f"No DICOM files found in {input_dir}")
    dicom_dirs = set(
        p.parent
        for p in dicom_files
        if not "Measurement" in p.as_posix()  # ignore volume measurements
    )
    for dicom_dir in tqdm(dicom_dirs):
        patient_ID = dicom_dir.parts[-3]
        date = dicom_dir.parts[-2][:10]
        sequence = dicom_dir.name.split("-")[1].removesuffix(" Segmentations")
        sequence_save_name = sequence_map[sequence]
        save_dir = Path(output_dir) / patient_ID / date / sequence_save_name
        save_dir.mkdir(parents=True, exist_ok=True)
        if "Segmentation" in dicom_dir.as_posix():
            dicom_path = list(dicom_dir.glob("*.dcm"))[0]
            seg_save_dir = save_dir / "segmentation"
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
        else:
            cmd = [
                "dcm2niix",
                "-z",
                "y",
                "-w",
                "0",
                "-f",
                sequence_save_name,
                "-o",
                save_dir.as_posix(),
                dicom_dir.as_posix(),
            ]
        try:
            subprocess.check_output(cmd)
            log.info(f"Conversion successful! (command: {(' ').join(cmd)}")
        except subprocess.CalledProcessError:
            log.error(f"Conversion failed! (command: {(' ').join(cmd)}")


def binarize_segmentation(nifti_path: Path):
    img = nib.load(nifti_path)
    arr = img.get_fdata()
    arr = (arr > 0).astype(np.uint8)
    new_img = nib.Nifti1Image(arr, img.affine, img.header)
    nib.save(new_img, nifti_path)


def postprocess_segmentations(nifti_dir: Path):
    seg_paths = list(Path(nifti_dir).glob("**/segmentation/*.nii.gz"))
    for seg_path in seg_paths:
        binarize_segmentation(seg_path)
        rename_segmentation(seg_path)


def rename_segmentation(seg_path: Path):
    region_map = {
        "PeripheralZone": "peripheral_zone",
        "NormalROI_PZ_1": "normal_tissue_pz",
        "WholeGland": "whole_gland",
        "TumorROI_PZ_1": "tumor_pz",
    }
    log.info(f"Renaming {seg_path}")
    meta_path = seg_path.parent / "meta.json"
    label_ID = seg_path.name.removesuffix(".nii.gz")
    try:
        label_ID = int(label_ID)
    except ValueError:
        log.warning(f"Label ID that is not an int found for {seg_path}")
        return None
    with open(meta_path, "r") as f:
        meta = json.load(f)
    try:
        region = [
            attr[0][0]["SegmentDescription"]
            for attr in meta["segmentAttributes"]
            if attr[0][0]["labelID"] == label_ID
        ]
    except KeyError:
        region = [
            attr[0]["SegmentDescription"]
            for attr in meta["segmentAttributes"]
            if attr[0]["labelID"] == label_ID
        ]
    try:
        region = region[0]
    except IndexError:
        log.error(f"Region not found for {seg_path}")
        return None
    region = region_map[region]
    new_seg_path = seg_path.parent / f"{region}.nii.gz"
    seg_path.rename(new_seg_path)
    log.info(f"Renamed {seg_path} to {new_seg_path}")
