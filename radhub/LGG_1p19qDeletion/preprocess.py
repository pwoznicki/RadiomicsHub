import pandas as pd
from pqdm.threads import pqdm

from radhub import utils


def convert_dataset(raw_dicom_dir, output_dir, n_jobs=8):
    raw_seg_paths = list(
        raw_dicom_dir.rglob("**/*Tumor segmentation*/**/*.dcm")
    )
    assert len(raw_seg_paths) == 159, "Expected 169 segmentation files"
    out_seg_dirs = [
        output_dir / raw_seg_path.parents[2].name
        for raw_seg_path in raw_seg_paths
    ]
    raw_img_dirs = [
        d for d in raw_dicom_dir.glob("*/*/*") if not "segmentation" in d.name
    ]
    # assert len(raw_img_dirs) == 318, "Expected 2*169=318 image directories"
    img_conversion_paths = utils.convert_dicom_sitk(
        dicom_data=raw_img_dirs,
        output_dir=output_dir,
        n_jobs=n_jobs,
    )

    args = zip(raw_seg_paths, out_seg_dirs)
    seg_conversion_paths_nested = pqdm(
        args, utils.convert_seg, n_jobs=n_jobs, argument_type="args"
    )
    seg_conversion_paths = [
        path for paths in seg_conversion_paths_nested for path in paths
    ]

    conversion_paths = img_conversion_paths + seg_conversion_paths
    conversion_df = utils.create_conversion_df(conversion_paths)

    return conversion_df


def create_paths_df(derived_nifti_dir):
    T2_names = ["FSE", "T2", "t2", "K2"]
    T1_names = ["T1", "t1", "SPGR", "BRAVO", "Bravo"]

    # df = pd.DataFrame(
    #     {"patient_ID": [p.name for p in derived_nifti_dir.iterdir()]}
    # )
    # df["seg_path"] = df["patient_ID"].apply(
    #     lambda x: conversion_df["derived_path"]
    # df["mod"] = df["derived_path"].apply(lambda x: i)
    results = []
    for case_dir in derived_nifti_dir.iterdir():
        if not case_dir.is_dir():
            continue
        for file in case_dir.glob("*.nii.gz"):
            case_info = {
                "patient_ID": case_dir.name,
                "seg_path": case_dir / "seg_Neoplasm.nii.gz",
            }
            if "seg" in file.name:
                continue
            case_info["img_path"] = file
            if [name for name in T2_names if name in file.name]:
                case_info["sequence"] = "T2"
            elif [name for name in T1_names if name in file.name]:
                case_info["sequence"] = "T1"
            else:
                raise ValueError(f"Unknown sequence for {str(file)}")
            results.append(case_info)
    result_df = pd.DataFrame(results)
    result_df["unique_ID"] = result_df.apply(
        lambda x: f"{x.patient_ID}_{x.sequence}", axis=1
    )
    result_df = result_df.reindex(
        columns=["patient_ID", "sequence", "unique_ID", "img_path", "seg_path"]
    )
    result_df = result_df.sort_values(by="unique_ID")
    return result_df
