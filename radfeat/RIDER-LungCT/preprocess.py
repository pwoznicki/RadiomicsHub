from pathlib import Path
import pandas as pd
import config
import pydicom as dcm
import os
import operator
import shutil
import logging

log = logging.getLogger(__name__)

timepoints = ["TEST", "RETEST"]


def remove_excluded_cases(base_dir, excluded_ids):
    all_files = base_dir.rglob("*")
    for id_ in excluded_ids:
        id_files = [file for file in all_files if id_ in str(file)]
        breakpoint()
        for file in id_files:
            os.remove(file)
            log.warn(f"File removed ({file})")

def rename_images_with_timepoints(nifti_img_dir: Path, dicom_img_dir: Path):
    """I (Piotr) couldn't find the info on whether a CT image belongs to TEST or RETEST,
       so I extract Instance Creation time from DICOM metadata to assign that
       chronologically."""
    dicom_dirs = list(dicom_img_dir.glob("*/*/*/"))
    dates = {}
    for dicom_dir in dicom_dirs:
        patient_ID = dicom_dir.parts[-3]
        dcm_ds = dcm.dcmread(list(dicom_dir.glob("*"))[0])
        series_instance_uid = get_dcm_tag(dcm_ds, 0x0020000E)
        matching_nifti_img_path = nifti_img_dir / f"{patient_ID}_{series_instance_uid}.nii.gz"
        if not matching_nifti_img_path.exists():
            breakpoint()
            raise ValueError(f"Nifti image doesn't exist! ({str(matching_nifti_img_path)})")
        date = get_dcm_tag(dcm_ds, 0x00080013)
        if not patient_ID in dates:
            dates[patient_ID] = {}
        dates[patient_ID][series_instance_uid] = date
        
    img_paths = nifti_img_dir.glob("*.nii.gz")
    for img_path in img_paths:
        id_, series_uid = img_path.name.removesuffix(".nii.gz").split("_") 
        if not len(dates[id_]) == 2:
            breakpoint()
        timepoint = get_timepoint(dates[id_], series_uid)
        new_nifti_dir = nifti_img_dir.parent / "nifti_renamed"
        new_nifti_dir.mkdir(exist_ok=True)
        new_img_path = new_nifti_dir / f"{id_}_{timepoint}_{series_uid}.nii.gz"
        shutil.copyfile(img_path, new_img_path)

def get_timepoint(time_dict: dict[str], series_uid: int):
    if not len(time_dict) == 2:
        raise Exception("Dictionary should have 2 values!")
    if list(time_dict.values())[0] > list(time_dict.values())[1]:
        if series_uid == list(time_dict.keys())[0]:
            return "RETEST"
        else:
            return "TEST"
    else:
        if series_uid == list(time_dict.keys())[0]:
            return "TEST"
        else:
            return "RETEST"
    

def get_dcm_tag(ds, tag):
    if not tag in ds:
        raise ValueError(f"Tag not found! ({tag})")
    return ds[tag].value


def rename_masks(nifti_seg_dir: Path):
    for fname in os.listdir(nifti_seg_dir):
        fpath = nifti_seg_dir / fname
        new_fname = fname.split("_")[0] + "_" + fname.split("_")[3]
        new_fpath = nifti_seg_dir / new_fname
        os.rename(fpath, new_fpath)


def get_paths():
    paths = []
    for patient_ID, study_ID in label_df[["patient_id", "study_id"]].values:
        for seg_roi, seg_dir in seg_rois.items():
            for sequence in sequences:
                img_path = config.img_dir / str(patient_ID) / f"{patient_ID}_{study_ID}_{sequence}.mha"
                seg_path = seg_dir / f"{patient_ID}_{study_ID}.nii.gz"
                if not img_path.exists():
                    print(f"Image file not found: {img_path}")
                    raise FileNotFoundError(f"File not found: {img_path}")
                if not seg_path.exists():
                    print(f"Segmentation file not found: {seg_path}")
                    raise FileNotFoundError(f"File not found: {seg_path}")
                paths.append({
                    "patient_ID": patient_ID,
                    "study_ID": study_ID,
                    "unique_ID": f"{patient_ID}_{study_ID}_{sequence}_{seg_roi}",
                    "ROI": seg_roi,
                    "sequence": sequence,
                    "img_path": str(img_path),
                    "seg_path": str(seg_path),
                })
    path_df = pd.DataFrame(paths)

    return path_df


if __name__ == "__main__":
    remove_excluded_cases(config.base_dir, config.excluded)
    rename_images_with_timepoints(config.nifti_img_dir, config.dicom_img_dir)
    rename_masks(config.nifti_seg_dir)
    # path_df.to_csv(config.table_dir / "paths.csv", index=False)

