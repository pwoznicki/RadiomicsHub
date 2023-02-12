import re
from pathlib import Path

import pandas as pd
import pydicom as dcm
from platipy.dicom.io.rtstruct_to_nifti import convert_rtstruct
from tqdm import tqdm


def get_dicom_modality(series_dir):
    """Get the modality of a dicom series"""
    file = next(series_dir.glob("*.dcm"))
    return dcm.read_file(file).Modality


def is_candidate(series_dir, modality):
    if "RTstruct" in series_dir.name:
        return False
    if modality in ["CT", "PET"]:
        ref_modality = get_dicom_modality(series_dir).replace("PT", "PET")
        if ref_modality == modality:
            return True
    else:
        ref_img_pattern = series_dir.name
        if modality.upper() in ref_img_pattern.upper():
            return True
        if modality == "T2FS" and re.search(
            "T2 F.*S.*", ref_img_pattern.upper()
        ):
            return True
        if modality == "T2FS" and "FAT T2" in ref_img_pattern:
            return True
        if modality == "T2FS" and "T2SP" in ref_img_pattern:
            return True
        if modality == "T2FS" and "FSE T2" in ref_img_pattern:
            return True
        if modality == "STIR" and "T2ST" in ref_img_pattern:
            return True
        if modality == "STIR" and "AX IR" in ref_img_pattern:
            return True
        if (
            modality == "AlignedT1toPET"
            and "AllignedT1toPET" in ref_img_pattern
        ):
            return True
        if modality == "AlignedTtoPET" and "AlignedT1toPET" in ref_img_pattern:
            return True
    return False


def convert_rtstruct_dataset(
    dicom_dir,
    output_dir,
):
    """Convert a dataset of RTSTRUCT files into Nifti files"""
    rtstruct_files = list(dicom_dir.rglob("*RTstruct*/*.dcm"))
    assert len(rtstruct_files) > 0, "No RTSTRUCT files found"
    modalities = [
        file.parent.name.split("-")[1].removeprefix("RTstruct")
        for file in rtstruct_files
    ]
    reference_images = []
    for rtstruct_file, modality in tqdm(list(zip(rtstruct_files, modalities))):
        candidate_images = [
            folder
            for folder in rtstruct_file.parents[1].iterdir()
            if is_candidate(folder, modality)
        ]
        if len(candidate_images) == 0:
            raise FileNotFoundError(
                f"Could not find reference image for {rtstruct_file}"
            )
        elif len(candidate_images) > 1:
            raise FileNotFoundError(
                f"Multiple reference images found for {rtstruct_file}:"
                f"{candidate_images}"
            )
        reference_images.append(candidate_images[0])

    for (rtstruct_file, reference_image, modality) in tqdm(
        list(zip(rtstruct_files, reference_images, modalities))
    ):
        id_ = rtstruct_file.parents[2].name
        save_dir = Path(output_dir) / id_
        save_dir.mkdir(parents=True, exist_ok=True)
        convert_rtstruct(
            reference_image,
            rtstruct_file,
            prefix=f"seg_{modality}_",
            output_dir=save_dir,
            output_img=modality,
        )


def create_paths_df(nifti_dir, base_dir):
    info = []
    for patient_dir in nifti_dir.iterdir():
        for nifti_file in patient_dir.glob("*.nii.gz"):
            if "seg" in nifti_file.stem:
                continue
            for roi in ["Edema", "Mass"]:
                patient_id = patient_dir.name
                modality = nifti_file.stem.split(".")[0]
                seg_path = (
                    nifti_file.parent / f"seg_{modality}_GTV_{roi}.nii.gz"
                )
                info.append(
                    {
                        "patient_id": patient_id,
                        "unique_ID": f"{patient_id}_{modality}_{roi}",
                        "modality": modality,
                        "ROI": roi,
                        "img_path": str(nifti_file.relative_to(base_dir)),
                        "seg_path": str(seg_path.relative_to(base_dir)),
                    }
                )
    return pd.DataFrame(info).sort_values("unique_ID")
