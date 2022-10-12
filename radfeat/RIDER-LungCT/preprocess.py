from pathlib import Path
import pandas as pd
import config
import pydicom as dcm
import os
import operator

timepoints = ["TEST", "RETEST"]

def rename_images_with_timepoints(nifti_img_dir: Path, dicom_img_dir: Path):
    """I couldn't find the info on whether a CT image belongs to TEST or RETEST,
       so I extract Instance Creation time from DICOM metadata to assign that
       chronologically."""
    img_paths = nifti_img_dir.glob("*.nii.gz")
    dates = {}
    for nifti_img_path in img_paths:
        id_, series_n = nifti_img_path.name.removesuffix(".nii.gz").split("_") 
        if not id_ in dates:
            dates[id_] = {}
        interim_dirname = os.listdir(dicom_img_dir / id_)[0]
        matching_dcm_series = [
                dirname 
                for dirname in os.listdir(dicom_img_dir / id_ / interim_dirname) 
                if dirname.startswith(series_n)
        ]
        if not len(matching_dcm_series) == 1:
            raise ValueError(f"Expected 1 matching dicom series, found {len(matching_dcm_series)} for {id_}")
        series_dirname = matching_dcm_series[0]
        dicom_img_path = dicom_img_dir / id_ / interim_dirname / series_dirname
        dcm_ds = dcm.dcmread(list(dicom_img_path.glob("*"))[0])

        date = get_dcm_tag(dcm_ds, 0x00080013)
        dates[id_][series_n] = date
        
    for img_path in img_paths:
        id_, series_n = img_path.name.removesuffix(".nii.gz").split("_") 
        timepoint = get_timepoint(dates[id_], series_n)
        new_img_path = nifti_img_dir / f"{id_}_{timepoint}.nii.gz"
        os.rename(img_path, new_img_path)


def get_timepoint(time_dict: dict[str], series_n: int):
    if not len(time_dict.values()) == 2:
        raise Exception("Dictionary should have 2 values!")
    if time_dict.values()[0] > time_dict.values()[1]:
        if series_n == time_dict.keys()[0]:
            return "RETEST"
        else:
            return "TEST"
    else:
        if series_n == time_dict.keys()[0]:
            return "TEST"
        else:
            return "RETEST"
    

def get_dcm_tag(ds, tag):
    if not tag in ds:
        raise ValueError(f"Tag not found! ({tag})")
    return ds[tag]


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
    rename_images_with_timepoints(config.nifti_img_dir, config.dicom_img_dir)
    rename_masks(config.nifti_seg_dir)
    # path_df.to_csv(config.table_dir / "paths.csv", index=False)

