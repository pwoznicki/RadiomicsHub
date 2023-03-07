import logging
from pathlib import Path

import pandas as pd
import pydicom
import pydicom_seg
import SimpleITK as sitk
from tqdm import tqdm

from radhub import utils

log = logging.getLogger(__name__)


def convert_dataset(dicom_dir, output_dir):
    raw_seg_paths = [
        path
        for path in dicom_dir.rglob("*.dcm")
        if "tumor segmentation" in str(path)
    ]
    paths = []
    for raw_seg_path in tqdm(raw_seg_paths):
        seg_paths = convert_seg(
            raw_seg_path, output_dir / raw_seg_path.parents[2].name
        )
        paths.extend(seg_paths)
        derived_seg_dir = seg_paths[0][1].parent
        if not (derived_seg_dir / "CT.nii.gz").exists():
            ct_paths = convert_ct(raw_seg_path, derived_seg_dir)
            paths.extend(ct_paths)
        if not (derived_seg_dir / "PET.nii.gz").exists():
            pet_paths = convert_pet(raw_seg_path, derived_seg_dir)
            paths.extend(pet_paths)

    conversion_df = pd.DataFrame(paths, columns=["raw_path", "derived_path"])
    conversion_df["raw_path"] = conversion_df["raw_path"].apply(
        lambda x: x.relative_to(dicom_dir)
    )
    conversion_df["derived_path"] = conversion_df["derived_path"].apply(
        lambda x: x.relative_to(output_dir)
    )
    return conversion_df


def convert_seg(
    raw_seg_path: Path, output_dir: Path
) -> list[tuple[Path, Path]]:
    dcm = pydicom.dcmread(raw_seg_path)

    reader = pydicom_seg.SegmentReader()
    result = reader.read(dcm)
    meta = result.dataset
    timepoint = meta.ClinicalTrialTimePointID
    raw_name = raw_seg_path.parent.name
    name = raw_name.split("-")[2].strip().replace(" ", "_").lower()
    paths = []
    for segment_ID in result.available_segments:
        segment_meta = result.segment_infos[segment_ID]
        roi = segment_meta.SegmentLabel.replace(", ", "_").lower()
        # seg_method = segment_meta.SegmentAlgorithmType
        # region = segment_meta.AnatomicRegion
        image = result.segment_image(segment_ID)
        output_path = (
            output_dir / timepoint / f"{roi}_{segment_ID}-{name}.nii.gz"
        )
        if output_path.exists():
            log.warn("Output path already exists: %s", output_path)
        output_path.parent.mkdir(exist_ok=True, parents=True)
        print(output_path)
        sitk.WriteImage(image, str(output_path))

        paths.append((raw_seg_path, output_path))
    return paths


def create_path_df(derived_nifti_dir):
    results = []
    for case_dir in derived_nifti_dir.iterdir():
        if not case_dir.is_dir():
            log.warn(f"Skipping non-directory: {case_dir}")
            continue
        for study_dir in case_dir.iterdir():
            if not study_dir.is_dir():
                log.warn(f"Skipping non-directory: {study_dir}")
                continue
            ct_path = study_dir / "CT.nii.gz"
            if not ct_path.exists():
                raise FileNotFoundError("CT image does not exist")
            pet_path = study_dir / "PET.nii.gz"
            if not pet_path.exists():
                raise FileNotFoundError("PET image does not exist")
            seg_paths = [
                path
                for path in study_dir.glob("*.nii.gz")
                if "neoplasm" in path.name
            ]
            for seg_path in seg_paths:
                seg_name = seg_path.name.removesuffix(".nii.gz")
                parts = seg_name.split("-")
                reader, method, _, trial_num = parts[1].split("_")
                roi = parts[0]
                timepoint = study_dir.name
                patient_ID = case_dir.name
                results.append(
                    {
                        "patient_ID": patient_ID,
                        "timepoint": timepoint,
                        "roi": roi,
                        "reader": reader,
                        "trial_num": trial_num,
                        "segmentation_method": method,
                        "unique_ID": f"{patient_ID}_{timepoint}_{roi}_{reader}_{trial_num}_{method}",
                        "CT_path": ct_path,
                        "PET_path": pet_path,
                        "seg_path": seg_path,
                    }
                )
    return pd.DataFrame(results).sort_values(by=["unique_ID"])


def convert_pet(seg_path: Path, output_dir: Path):
    if (output_dir / "PET.nii.gz").exists():
        log.error("CT image already exists")
    raw_pet_paths = [
        path
        for path in seg_path.parents[1].iterdir()
        if "PET" in path.name
        and "SUV" not in path.name
        and "NAC" not in path.name
    ]
    if len(raw_pet_paths) != 1:
        raise ValueError("Could not find PET image")
    raw_pet_path = raw_pet_paths[0]
    pet_image = utils.read_dicom_sitk(raw_pet_path)
    output_path = output_dir / "PET.nii.gz"
    sitk.WriteImage(pet_image, str(output_path))

    return [(raw_pet_path, output_path)]


def convert_ct(seg_path: Path, output_dir: Path):
    if (output_dir / "CT.nii.gz").exists():
        log.error("CT image already exists")
    raw_ct_paths = [
        path for path in seg_path.parents[1].iterdir() if "CT" in path.name
    ]
    if len(raw_ct_paths) != 1:
        raise ValueError("Could not find CT image")
    raw_ct_path = raw_ct_paths[0]
    ct_image = utils.read_dicom_sitk(raw_ct_path)
    output_path = output_dir / "CT.nii.gz"
    sitk.WriteImage(ct_image, str(output_path))

    return [(raw_ct_path, output_path)]


#  utils.convert_dicom_to_nifti(
#      raw_ct_paths, output_dir, filename_pattern="CT"
#  )
#  utils.convert_dicom_to_nifti(
#      raw_pet_paths, output_dir, filename_pattern="PET"
#  )
