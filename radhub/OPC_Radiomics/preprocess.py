import logging

import pandas as pd
from platipy.dicom.io.rtstruct_to_nifti import convert_rtstruct
from pqdm.threads import pqdm

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
    for save_dir in save_dirs:
        save_dir.mkdir(parents=True, exist_ok=True)
    conversion_paths_nested = pqdm(
        (
            {
                "dcm_img": raw_ct_dir,
                "dcm_rt_file": rt_file,
                "output_dir": save_dir,
                "prefix": "seg_",
                "output_img": "CT",
            }
            for raw_ct_dir, rt_file, save_dir in zip(
                raw_ct_dirs,
                rt_files,
                save_dirs,
            )
        ),
        convert_rt,
        n_jobs=n_jobs,
        argument_type="kwargs",
    )

    conversion_paths = [
        path for paths in conversion_paths_nested for path in paths
    ]
    conversion_df = pd.DataFrame(
        conversion_paths, columns=["raw_path", "derived_path"]
    )
    conversion_df["raw_path"] = conversion_df["raw_path"].apply(
        lambda x: x.relative_to(dicom_dir)
    )
    conversion_df["derived_path"] = conversion_df["derived_path"].apply(
        lambda x: x.relative_to(output_dir)
    )
    return conversion_df


def convert_rt(
    dcm_img, dcm_rt_file, output_dir, prefix="seg_", output_img="CT"
):
    convert_rtstruct(
        dcm_img=dcm_img,
        dcm_rt_file=dcm_rt_file,
        output_dir=output_dir,
        prefix=prefix,
        output_img=output_img,
    )
    converted_paths = []
    out_img_path = output_dir / f"{output_img}.nii.gz"
    if out_img_path.exists():
        converted_paths.append((dcm_img, out_img_path))
    derived_seg_paths = list(output_dir.glob(f"{prefix}*.nii.gz"))
    converted_paths.extend(
        (dcm_rt_file, derived_seg_path)
        for derived_seg_path in derived_seg_paths
    )
    return converted_paths
