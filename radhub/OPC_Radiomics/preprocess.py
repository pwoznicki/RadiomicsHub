import logging
from pathlib import Path

import pandas as pd
from pqdm.threads import pqdm
from tqdm import tqdm

from radhub import utils

log = logging.getLogger(__name__)


def convert_dataset(dicom_dir, output_dir, n_jobs=1):
    ct_files = (
        path
        for path in dicom_dir.rglob("*.dcm")
        if not path.name.endswith("1-1.dcm")
    )
    raw_ct_dirs = list(set(path.parent for path in ct_files))

    rt_files = []
    cts_without_seg = []
    for raw_ct_dir in raw_ct_dirs:
        study_dir = raw_ct_dir.parent
        study_rt_files = list(study_dir.rglob("*1-1.dcm"))
        if len(study_rt_files) > 1:
            log.warning(
                f"Multiple RTSTRUCT files found for study {str(study_dir)}."
                "I'm assuming the're the same and using the first file: "
                f"{study_rt_files[0]}"
            )
        if len(study_rt_files) == 0:
            log.warning(
                f"No RTSTRUCT files found for study {str(study_dir)}."
                "I'm ignoring this study."
            )
            cts_without_seg.append(raw_ct_dir)
            continue
        rt_files.append(study_rt_files[0])
    raw_ct_dirs = [
        raw_ct_dir
        for raw_ct_dir in raw_ct_dirs
        if raw_ct_dir not in cts_without_seg
    ]
    assert len(rt_files) == 605
    assert len(raw_ct_dirs) == 605

    ids = [raw_ct_dir.parents[1].name for raw_ct_dir in raw_ct_dirs]
    save_dirs = [output_dir / id_ for id_ in ids]
    for save_dir in tqdm(save_dirs):
        save_dir.mkdir(parents=True, exist_ok=True)
    conversion_paths_nested = pqdm(
        (
            {
                "dcm_img": raw_ct_dir,
                "dcm_rt_file": rt_file,
                "output_dir": save_dir,
                "prefix": "seg_",
                "out_img_stem": "CT",
            }
            for raw_ct_dir, rt_file, save_dir in zip(
                raw_ct_dirs,
                rt_files,
                save_dirs,
            )
        ),
        utils.convert_rt,
        n_jobs=n_jobs,
        argument_type="kwargs",
    )

    conversion_paths = [
        path for paths in conversion_paths_nested for path in paths
    ]
    conversion_df = utils.create_conversion_df(
        conversion_paths, dicom_dir, output_dir
    )
    return conversion_df


def create_paths_df(nifti_dir: Path) -> pd.DataFrame:
    results = []
    for study_dir in nifti_dir.iterdir():
        patient_id = study_dir.name
        img_path = study_dir / "CT.nii.gz"
        gtv_seg_path = study_dir / "seg_GTV.nii.gz"
        # if patient_id in ["OPC-00221", "OPC-00367"]:
        #     gtv_seg_path = study_dir / "seg_HTV.nii.gz"
        assert img_path.exists()
        if not gtv_seg_path.exists():
            log.warning(f"Missing GTV segmentation for {patient_id}")
            continue
        results.append(
            {
                "patient_ID": patient_id,
                "ROI": "GTV",
                "img_path": str(img_path),
                "seg_path": str(gtv_seg_path),
            }
        )
    return pd.DataFrame(results).sort_values(by="patient_ID")
