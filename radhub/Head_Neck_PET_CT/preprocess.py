from radhub import utils
from pathlib import Path
from tqdm import tqdm
import pydicom
import pandas as pd
from pqdm.processes import pqdm
import logging

log = logging.getLogger(__name__)


def is_rtstruct(dcm_path):
    dcm_img = pydicom.dcmread(dcm_path)
    return dcm_img.Modality == "RTSTRUCT"


def get_series_description(dcm_path):
    dcm_img = pydicom.dcmread(dcm_path)
    try:
        desc = dcm_img.SeriesDescription
    except AttributeError:
        desc = ""
    return desc


def get_modality(series_description):
    if isinstance(series_description, float):
        return "CT"
    if "->PET" in series_description:
        return "PET"
    return "CT"


def find_data(raw_dicom_dir):
    candidate_seg_paths = list(raw_dicom_dir.rglob("1-1.dcm"))
    is_rtstruct_list = pqdm(candidate_seg_paths, is_rtstruct, n_jobs=16)
    rtstruct_paths = [
        p
        for p, is_rtstruct in zip(candidate_seg_paths, is_rtstruct_list)
        if is_rtstruct
    ]
    ids = [p.parents[2].name for p in rtstruct_paths]
    path_dict = {id_: [] for id_ in ids}
    series_description_map = {}
    for id_, path in zip(ids, rtstruct_paths):
        path_dict[id_].append(path)
    for id_, paths in tqdm(path_dict.items()):
        if len(paths) > 2:
            series_descriptions = [get_series_description(p) for p in paths]
            resampled_paths = [
                p
                for p, desc in zip(paths, series_descriptions)
                if "->" in desc
            ]
            nonresampled_paths = [
                p
                for p, desc in zip(paths, series_descriptions)
                if "->" not in desc
            ]
            paths = resampled_paths
            if len(resampled_paths) == 1:
                paths.append(nonresampled_paths[0])
        if len(paths) != 2:
            raise ValueError(
                f"Found {len(paths)} RTSTRUCT files for patient {id_}. "
                "Expected 2."
            )
        for p in paths:
            series_description_map[p] = get_series_description(p)
        path_dict[id_] = paths
    final_rt_paths = list(series_description_map.keys())
    final_img_paths = [
        utils.find_matching_img(
            rtstruct_path=rt_path,
            dcm_img_data=rt_path.parents[2],
        )
        for rt_path in tqdm(final_rt_paths)
    ]
    final_series_descriptions = series_description_map.values()

    raw_path_df = pd.DataFrame(
        {
            "img_path": final_img_paths,
            "rt_path": final_rt_paths,
            "series_description": final_series_descriptions,
        }
    )
    raw_path_df.append(
        pd.DataFrame(
            {
                "img_path": ["/mnt/hard/radiomics-features/Head-Neck-PET-CT/raw/dicom/HN-HGJ-030/08-27-1885-NA-PET HEAD NECK-94646/1.000000-PET AC 21-49095"],
                "rt_path": ["/mnt/hard/radiomics-features/Head-Neck-PET-CT/raw/dicom/HN-HGJ-030/08-27-1885-NA-PET HEAD NECK-94646/1.000000-RTstructCTsim-PETPET-CT-89245/1-1.dcm"],
                "series_description": ["RTstruct_CTsim->PET(PET-CT)"],
            },
        )
    )

    return raw_path_df


def convert_dataset(raw_path_df, output_dir):
    output_dir.mkdir(exist_ok=True)
    raw_path_df = raw_path_df.copy().dropna(subset=["img_path", "rt_path"])
    patient_IDs = [Path(p).parents[1].name for p in raw_path_df.img_path]
    out_case_dirs = [output_dir / id_ for id_ in patient_IDs]
    kwargs = [
        dict(
            dcm_img=dcm_img,
            dcm_rt_path=dcm_rt_path,
            out_img_stem=modality,
            prefix=f"seg_{modality}_",
            output_dir=out_case_dir,
        )
        for dcm_img, dcm_rt_path, modality, out_case_dir in zip(
            raw_path_df.img_path,
            raw_path_df.rt_path,
            raw_path_df.series_description.apply(get_modality),
            out_case_dirs,
        )
    ]
    conversion_paths_nested = pqdm(
        kwargs, utils.convert_rt, n_jobs=12, argument_type="kwargs"
    )
    conversion_paths = [
        path for paths in conversion_paths_nested for path in paths
    ]
    conversion_df = utils.create_conversion_df(
        conversion_paths=conversion_paths,
    )
    return conversion_df


def load_contours_df(path):
    dfs = pd.read_excel(path, sheet_name=None, engine="openpyxl")
    merged_df = pd.concat(dfs, ignore_index=True)
    merged_df.rename({"Patient": "patient_ID"}, axis=1, inplace=True)

    return merged_df


def create_path_df(conversion_df, contours_df):
    results = []
    for _, row in tqdm(list(contours_df.iterrows())):
        patient_ID = row.patient_ID
        seg_name = (
            row["Name GTV Primary"]
            .replace(" ", "_")
            .replace("__", "_")
            .split(",")[0]
        )  # use only first seg (3 cases in dataset have multiple)
        for modality in ["CT", "PET"]:
            try:
                derived_case_dir = Path(
                    conversion_df.derived_path[
                        conversion_df.derived_path.str.contains(patient_ID)
                    ].iloc[0]
                ).parent
            except IndexError:
                log.error(f"Could not find {patient_ID} in conversion_df")
                continue
            img_path = derived_case_dir / f"{modality}.nii.gz"
            if not img_path.exists():
                log.error(f"Could not find {img_path}")
                continue
            try:
                seg_path = [
                    path
                    for path in derived_case_dir.iterdir()
                    if f"seg_{modality}_{seg_name}".lower()
                    in path.name.lower()
                ][0]
            except IndexError:
                log.error(
                    f"Could not find {seg_name} in {patient_ID} (dir: {derived_case_dir}))"
                )
                continue
            if not seg_path.exists():
                log.error(f"Could not find {seg_path}")
                continue

            results.append(
                dict(
                    patient_ID=patient_ID,
                    modality=modality,
                    unique_ID=f"{patient_ID}_{modality}",
                    img_path=img_path,
                    seg_path=seg_path,
                )
            )
    result_df = pd.DataFrame(results).sort_values("patient_ID")

    return result_df
