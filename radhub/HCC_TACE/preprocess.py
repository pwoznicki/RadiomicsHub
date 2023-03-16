import logging
import shutil
from pathlib import Path
from typing import Sequence

import pydicom
from tqdm import tqdm

from radhub import utils

log = logging.getLogger(__name__)


def find_image_matching_to_seg(
    dcm_seg_path: Path,
    dcm_img_data: Path | Sequence[Path],
):
    dicom_dirs = utils.get_dicom_dirs(dcm_img_data)
    for dicom_dir in dicom_dirs:
        dcm_img_path = next(dicom_dir.glob("*.dcm"))
        dcm_img = pydicom.dcmread(dcm_img_path)
        dcm_seg = pydicom.dcmread(dcm_seg_path)
        if not dcm_img.Modality in ("CT", "MR", "PT"):
            pass
        assert dcm_seg.Modality == "SEG"
        if is_a_match(dcm_img, dcm_seg):
            return dcm_img_path.parent
    log.error(f"No matching image found for {dcm_seg_path}")


def is_a_match(dcm_img: pydicom.Dataset, dcm_seg: pydicom.Dataset):
    try:
        match = (
            dcm_img.SeriesInstanceUID
            == dcm_seg.ReferencedSeriesSequence[0].SeriesInstanceUID
        )
    except AttributeError:
        log.warning(
            f"Could not find ReferencedSeriesSequence for {dcm_seg.PatientID}"
        )
        match = False
    return match


def convert_dataset(raw_data_dir, derived_nifti_dir):
    raw_seg_paths = list(raw_data_dir.rglob("*1-1.dcm"))
    conversion_paths = []
    raw_img_paths = []
    for raw_seg_path in tqdm(raw_seg_paths):
        id_ = raw_seg_path.parents[2].name
        raw_patient_dir = raw_data_dir / id_
        raw_img_path = find_image_matching_to_seg(
            raw_seg_path, raw_patient_dir
        )
        if raw_img_path is None:
            log.error(f"Image not found for {raw_seg_path}")
            continue
        raw_img_paths.append(raw_img_path)
        out_patient_dir = derived_nifti_dir / id_
        out_patient_dir.mkdir(parents=True, exist_ok=True)

        derived_dicom_dir = derived_nifti_dir.parent / "dicom"
        corrected_dicom_dirs = separate_by_acquisition_number(
            raw_series_dir=raw_img_path,
            derived_dicom_dir=derived_dicom_dir,
        )
        img_conversion_paths = []
        for dcm_dir in corrected_dicom_dirs:
            derived_img_path = out_patient_dir / f"img_{dcm_dir.name}.nii.gz"
            img_conversion_paths.append(
                utils.convert_sitk(dcm_dir, derived_img_path)
            )
        seg_conversion_paths = utils.convert_seg(
            raw_seg_path=raw_seg_path,
            output_dir=out_patient_dir,
        )
        conversion_paths.extend(img_conversion_paths)
        conversion_paths.extend(seg_conversion_paths)

    return conversion_paths


def get_acquisition_number(dcm_path: Path):
    dcm = pydicom.dcmread(dcm_path)
    return dcm.AcquisitionNumber


def separate_by_acquisition_number(
    raw_series_dir: Path, derived_dicom_dir: Path
):
    dcm_paths = list(raw_series_dir.rglob("*.dcm"))
    acq_dirs = []
    for dcm_path in dcm_paths:
        acq_n = get_acquisition_number(dcm_path)
        acq_dir = (
            derived_dicom_dir
            / raw_series_dir.parents[1].name
            / raw_series_dir.parent.name
            / raw_series_dir.name
            / f"phase{acq_n}"
        )
        acq_dir.mkdir(parents=True, exist_ok=True)
        acq_dirs.append(acq_dir)
        shutil.copy(dcm_path, acq_dir / dcm_path.name)
    return set(acq_dirs)
