import logging
from pathlib import Path
from typing import Iterable

import pandas as pd
import pydicom
from pqdm.threads import pqdm
from tqdm import tqdm

from radhub import utils
from radhub.Meningioma_SEG_CLASS import config

log = logging.getLogger(__name__)


def find_data(raw_dicom_dir: Path):
    rtstruct_paths = list(raw_dicom_dir.rglob("1-1.dcm"))
    results = []
    for rtstruct_path in tqdm(rtstruct_paths):
        if config.EXCLUDED_ID in str(rtstruct_path):
            continue
        study_dir = rtstruct_path.parents[1]
        img_path = utils.find_matching_img(rtstruct_path, study_dir)
        if img_path is not None:
            results.append((str(img_path), str(rtstruct_path)))
    result_df = pd.DataFrame(results, columns=["img_path", "seg_path"])
    return result_df


def convert_dataset(raw_path_df, derived_nifti_dir, n_jobs=4):
    raw_img_paths = raw_path_df["img_path"].tolist()
    raw_seg_paths = raw_path_df["seg_path"].tolist()
    out_fnames = [
        Path(p).name.split("-")[1].replace(" ", "-") for p in raw_img_paths
    ]
    conversion_df = utils.convert_rt_dataset(
        raw_img_paths=raw_img_paths,
        raw_rt_paths=raw_seg_paths,
        derived_nifti_dir=derived_nifti_dir,
        out_fnames=out_fnames,
        n_jobs=n_jobs,
    )
    return conversion_df


def create_paths_df(raw_path_df, conversion_df):
    result_df = (
        raw_path_df.rename(
            columns={"img_path": "raw_img_path", "seg_path": "raw_seg_path"}
        )
        .merge(
            conversion_df,
            left_on="raw_img_path",
            right_on="raw_path",
            how="left",
        )
        .rename(columns={"derived_path": "img_path"})
        .merge(
            conversion_df,
            left_on="raw_seg_path",
            right_on="raw_path",
            how="left",
        )
        .rename(columns={"derived_path": "seg_path"})
        .drop(columns=["raw_path_x", "raw_path_y"])
        .astype(str)
        .assign(
            patient_ID=lambda x: x.img_path.str.split("/").str[-2],
            sequence=lambda x: x.img_path.str.split("/")
            .str[-1]
            .str.removesuffix(".nii.gz"),
        )
        .assign(
            unique_ID=lambda x: x.apply(
                lambda y: f"{y.patient_ID}_{y.sequence}", axis=1
            )
        )
        .reindex(
            columns=[
                "patient_ID",
                "sequence",
                "unique_ID",
                "img_path",
                "seg_path",
                "raw_img_path",
                "raw_seg_path",
            ]
        )
    )

    return result_df
