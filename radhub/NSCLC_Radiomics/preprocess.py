import subprocess
import pandas as pd
import logging
from tqdm import tqdm
import json

log = logging.getLogger(__name__)


def convert_seg_to_nifti(raw_dicom_dir, derived_nifti_dir):
    seg_paths = [
        path
        for path in raw_dicom_dir.rglob("*.dcm")
        if "Segmentation" in str(path)
    ]
    for seg_path in tqdm(seg_paths):
        id_ = seg_path.parents[2].name
        seg_save_dir = derived_nifti_dir / id_
        seg_save_dir.mkdir(parents=True, exist_ok=True)
        cmd = [
            "segimage2itkimage",
            "--inputDICOM",
            seg_path.as_posix(),
            "--outputDirectory",
            seg_save_dir.as_posix(),
            "-p",
            "seg",
            "-t",
            "nifti",
        ]
        try:
            subprocess.check_output(cmd)
            log.info(f"Conversion successful! (command: {(' ').join(cmd)}")
        except subprocess.CalledProcessError:
            log.error(f"Conversion failed! (command: {(' ').join(cmd)}")


def rename_dcmqi_nifti_seg(derived_nifti_dir):
    for id_dir in tqdm(list(derived_nifti_dir.iterdir())):
        meta_path = id_dir / "seg-meta.json"
        if not meta_path.exists():
            log.error(f"Meta file does not exist for {id_dir.name}")
            continue
        meta = json.load(meta_path.open())
        for segment in meta["segmentAttributes"]:
            label = segment[0]["labelID"]
            name = segment[0]["SegmentDescription"]
            new_seg_path = id_dir / f"seg_{name}.nii.gz"
            old_seg_path = id_dir / f"seg-{label}.nii.gz"
            if not old_seg_path.exists():
                log.error(
                    f"Segmentation file does not exist for {id_dir.name}"
                )
                continue
            old_seg_path.rename(new_seg_path)
            log.info(f"Renamed {old_seg_path} to {new_seg_path}")


def create_paths_df(derived_nifti_dir):
    paths = []
    for case_dir in tqdm(derived_nifti_dir.iterdir()):
        id_ = case_dir.name
        img_path = case_dir / "ct.nii.gz"
        seg_path = case_dir / "seg_GTV-1.nii.gz"
        if not img_path.exists():
            log.error(f"Image file does not exist for {id_}")
            continue
        if not seg_path.exists():
            log.error(f"Segmentation file does not exist for {id_}")
            continue
        paths.append(
            {
                "patient_ID": id_,
                "ROI": "primary tumor",
                "img_path": img_path,
                "seg_path": seg_path,
            }
        )
    return pd.DataFrame(paths).sort_values("patient_ID")
