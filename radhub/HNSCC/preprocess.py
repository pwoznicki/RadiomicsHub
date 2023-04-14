from radhub import utils
import logging
from pqdm.processes import pqdm
from tqdm import tqdm
import pandas as pd


log = logging.getLogger(__name__)


def get_dcm_series_modality(dcm_dir):
    dcm_path = list(dcm_dir.rglob("*.dcm"))[0]
    return utils.get_modality(dcm_path)


def convert_dataset(raw_dicom_dir, derived_nifti_dir, n_jobs=8):
    candidate_seg_paths = list(raw_dicom_dir.rglob("*1-1.dcm"))
    is_rtstruct_list = pqdm(
        candidate_seg_paths, utils.is_rtstruct, n_jobs=n_jobs
    )
    rtstruct_paths = [
        p
        for p, is_rtstruct in zip(candidate_seg_paths, is_rtstruct_list)
        if is_rtstruct
    ]
    kwargs_list = [
        {"rtstruct_path": rt_path, "dcm_img_data": rt_path.parents[2]}
        for rt_path in rtstruct_paths
    ]

    img_paths = pqdm(
        kwargs_list,
        utils.find_matching_img,
        argument_type="kwargs",
        n_jobs=n_jobs,
    )
    args_list = [(p,) for p in img_paths]
    modalities = pqdm(
        args_list, get_dcm_series_modality, argument_type="args", n_jobs=n_jobs
    )

    conversion_df = utils.convert_rt_dataset(
        raw_img_paths=img_paths,
        raw_rt_paths=rtstruct_paths,
        derived_nifti_dir=derived_nifti_dir,
        out_fname=modalities,
        n_jobs=n_jobs,
    )

    return conversion_df


def create_paths_df(derived_nifti_dir):
    gtv_seg_paths = list(derived_nifti_dir.rglob("seg_CT_GTV*.nii.gz"))
    rois = [
        p.name.removesuffix(".nii.gz").removeprefix("seg_CT_")
        for p in gtv_seg_paths
    ]
    print(f"Found {len(gtv_seg_paths)} GTV segmentations")
    img_paths = [p.parent / "CT.nii.gz" for p in gtv_seg_paths]
    patient_IDs = [p.parent.name for p in gtv_seg_paths]
    result_df = pd.DataFrame(
        {
            "patient_ID": patient_IDs,
            "ROI": rois,
            "unique_ID": [f"{p}_{r}" for p, r in zip(patient_IDs, rois)],
            "img_path": img_paths,
            "seg_path": gtv_seg_paths,
        }
    ).sort_values("patient_ID")

    return result_df
