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


def find_matching_img(
    rtstruct_path: Path, dcm_img_data: Path | Iterable[Path]
):
    dicom_dirs = utils.get_dicom_dirs(dcm_img_data)
    for dicom_dir in dicom_dirs:
        dcm_img_path = next(dicom_dir.glob("*.dcm"))
        dcm_img = pydicom.dcmread(dcm_img_path)
        dcm_seg = pydicom.dcmread(rtstruct_path)
        if not dcm_img.Modality == "MR":
            pass
        assert dcm_seg.Modality == "RTSTRUCT"
        if utils.is_dicom_a_match(dcm_img, dcm_seg):
            return dcm_img_path.parent
    log.error(f"No matching image found for {rtstruct_path}")


def find_data(raw_dicom_dir: Path):
    rtstruct_paths = list(raw_dicom_dir.rglob("1-1.dcm"))
    results = []
    for rtstruct_path in tqdm(rtstruct_paths):
        if config.EXCLUDED_ID in str(rtstruct_path):
            continue
        study_dir = rtstruct_path.parents[1]
        img_path = find_matching_img(rtstruct_path, study_dir)
        if img_path is not None:
            results.append((str(img_path), str(rtstruct_path)))
    result_df = pd.DataFrame(results, columns=["img_path", "seg_path"])
    return result_df


def convert_dataset(raw_path_df, derived_nifti_dir, n_jobs=4):
    raw_img_paths = raw_path_df["img_path"].tolist()
    raw_seg_paths = raw_path_df["seg_path"].tolist()
    output_dirs = [
        derived_nifti_dir / Path(p).parents[1].name for p in raw_img_paths
    ]
    out_fnames = [
        Path(p).name.split("-")[1].replace(" ", "-") for p in raw_img_paths
    ]
    prefixes = [f"seg_{out_fname}_" for out_fname in out_fnames]
    arg_dict = dict(
        dcm_img=raw_img_paths,
        dcm_rt_path=raw_seg_paths,
        output_dir=output_dirs,
        prefix=prefixes,
        out_img_stem=out_fnames,
    )
    args = pd.DataFrame(arg_dict).to_dict(orient="records")
    conversion_paths_nested = pqdm(
        args, utils.convert_rt, n_jobs=n_jobs, argument_type="kwargs"
    )
    conversion_paths = [
        item for sublist in conversion_paths_nested for item in sublist
    ]
    conversion_df = utils.create_conversion_df(conversion_paths)

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
