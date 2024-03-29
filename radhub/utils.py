import logging
import subprocess
from pathlib import Path
from typing import Iterable, Sequence

import nibabel as nib
import numpy as np
import pandas as pd
import pydicom
import pydicom_seg
import SimpleITK as sitk
from autorad.data import ImageDataset
from autorad.feature_extraction.extractor import FeatureExtractor
from autorad.utils import io
from platipy.dicom.io.rtstruct_to_nifti import convert_rtstruct
from pqdm.threads import pqdm
from tqdm import tqdm

logging.getLogger().setLevel(logging.CRITICAL)

log = logging.getLogger(__name__)


def pretty_log(text):
    text = f" {text} "
    log.info(f"{text:#^80}")


def binarize_segmentations(nifti_data: Path | Sequence[Path], n_jobs=4):
    if isinstance(nifti_data, Path):
        seg_paths = list(nifti_data.rglob("*.nii.gz"))
    else:
        seg_paths = nifti_data
    for seg_path in tqdm(seg_paths):
        binarize_segmentation(seg_path)


def binarize_segmentation(nifti_path: Path):
    with nib.load(nifti_path) as img:
        arr = img.get_fdata()
        arr = (arr > 0).astype(np.uint8)
        new_img = nib.Nifti1Image(arr, img.affine, img.header)
    nib.save(new_img, nifti_path)


def read_dicom_sitk(input_dir: Path) -> sitk.Image:
    reader = sitk.ImageSeriesReader()

    dicom_names = reader.GetGDCMSeriesFileNames(str(input_dir))
    reader.SetFileNames(dicom_names)

    image = reader.Execute()

    return image


def convert_dicom_seg_dataset(
    dicom_data: Path | Sequence[Path],
    nifti_seg_dir: Path,
    suffix="",
):
    dicom_dirs = get_dicom_dirs(dicom_data)
    for dicom_dir in dicom_dirs:
        seg_sitk = io.read_dicom_seg_sitk(dicom_dir)
        id_ = dicom_dir.parents[2].name
        output_dir = nifti_seg_dir / id_
        output_dir.mkdir(parents=True, exist_ok=True)
        sitk.WriteImage(seg_sitk, str(output_dir / f"seg_{suffix}.nii.gz"))


def get_dicom_dirs(dicom_data: Path | Iterable[Path]):
    if isinstance(dicom_data, Path):
        if not dicom_data.exists():
            raise FileNotFoundError(f"Directory not found: {dicom_data}")
        dicom_dirs = list(
            set(dicom_dir.parent for dicom_dir in dicom_data.rglob("*.dcm"))
        )
    else:
        dicom_dirs = dicom_data
    return dicom_dirs


def convert_dicom_to_nifti(
    dicom_data: Path | Iterable[Path],
    nifti_img_dir,
    filename_pattern="%i",
    *dcm2niix_args,
    ignore_derived=True,
    n_jobs=4,
):
    dicom_dirs = get_dicom_dirs(dicom_data)
    nifti_img_dir.mkdir(parents=True, exist_ok=True)
    if ignore_derived:
        dcm2niix_args = list(dcm2niix_args) + ["-i", "y"]
    img_cmds = (
        [
            "dcm2niix",
            "-z",
            "y",
            "-f",
            filename_pattern,
            "-o",
            str(nifti_img_dir),
            *dcm2niix_args,
            str(dicom_dir),
        ]
        for dicom_dir in dicom_dirs
    )
    pqdm(img_cmds, convert_series, n_jobs=n_jobs)


def convert_dicom_to_nifti_imported(
    dicom_dir: Path, output_path: Path, converter: str = "dcm2niix"
):
    """
    Convert directory containing one dicom series into compressed nifti
    Args:
        dicom_dir (Path): Path to the dicom directory
        output_path (Path): Path to the output nifti file
        converter (str): Converter to use. Either "plastimatch" or "dcm2niix"
    """
    dicom_dir = Path(dicom_dir)
    output_path = Path(output_path)
    if converter == "plastimatch":
        cmd = (
            f"plastimatch convert --input {dicom_dir.absolute()} "
            f"--output-img {output_path.absolute()}"
        )
    elif converter == "dcm2niix":
        do_compression = "y" if output_path.name.endswith(".nii.gz") else "n"
        cmd = (
            f"dcm2niix -z {do_compression} -f {output_path.name.split('.')[0]} -o"
            f" {output_path.parent.absolute()} -i y {dicom_dir.absolute()}"
        )
    else:
        raise ValueError(f"Converter {converter} not found!")

    log.info(f"Converting {dicom_dir} to {output_path} with {converter}")
    log.info(f"Command: {cmd}")

    try:
        output = subprocess.check_output(cmd.split())
    except RuntimeError:
        log.error(f"Conversion to nifti with dcm2niix failed for {dicom_dir}")


def convert_series(cmd: list[str]):
    try:
        subprocess.check_output(cmd)
        log.info(f"Conversion successful! (command: {cmd}")
    except subprocess.CalledProcessError as e:
        log.error(f"Conversion failed! (command: {cmd}")
        log.error(f"Error: {e.output}")


def convert_dataset_sitk(
    dicom_data: Path | Iterable[Path],
    output_dir: Path,
    ext_to: str = ".nii.gz",
    out_fname=None,
    prefix="",
    n_jobs=4,
) -> pd.DataFrame:
    def get_fname(img_path, fname):
        if not fname:
            return (
                prefix.join(Path(img_path).name.split("-")[1:-1])
                .replace(" ", "_")
                .replace(".", "")
                + ext_to
            )
        else:
            return prefix + fname + ext_to

    dicom_dirs = get_dicom_dirs(dicom_data)
    args = [
        (
            img_path,
            Path(output_dir)
            / Path(img_path).parents[1].name
            / get_fname(img_path, out_fname),
        )
        for img_path in dicom_dirs
    ]
    conversion_paths = pqdm(
        args, convert_sitk, n_jobs=n_jobs, argument_type="args"
    )

    conversion_df = create_conversion_df(conversion_paths)

    return conversion_df


def convert_dir_sitk(
    input_dir: str,
    output_dir: str,
    ext_from: str = ".mhd",
    ext_to: str = ".nii.gz",
    n_jobs=4,
):
    args = (
        (img_path, Path(output_dir) / (img_path.name.split(".")[0] + ext_to))
        for img_path in Path(input_dir).glob("*" + ext_from)
    )
    pqdm(args, convert_sitk, n_jobs=n_jobs)
    # for img_path in tqdm(list(Path(input_dir).glob("*" + ext_from))):
    #     out_img_path = Path(output_dir) / (
    #         img_path.name.split(".")[0] + ext_to
    #     )
    #     convert_sitk(img_path, out_img_path)


def extract_features(
    paths_df,
    ID_colname,
    extraction_params="CT_default.yaml",
    image_colname="img_path",
    mask_colname="seg_path",
    root_dir=None,
    n_jobs=-1,
    mask_label=None,
):
    image_dset = ImageDataset(
        paths_df,
        ID_colname=ID_colname,
        image_colname=image_colname,
        mask_colname=mask_colname,
        root_dir=root_dir,
    )
    extractor = FeatureExtractor(
        image_dset,
        extraction_params=extraction_params,
        n_jobs=n_jobs,
    )
    feature_df = extractor.run(mask_label=mask_label)
    return feature_df


def convert_sitk(in_path, out_path):
    if not Path(in_path).exists():
        raise FileNotFoundError(f"File {str(in_path)} does not exist")
    try:
        # data = io.read_image_sitk(Path(in_path))
        Path(out_path).parent.mkdir(exist_ok=True, parents=True)
        # if Path(out_path).exists():
        #     log.warning(f"File {str(out_path)} already exists, overwriting")
        # sitk.WriteImage(data, str(out_path))
    except RuntimeError:
        log.error(f"Conversion to nifti with SimpleITK failed for {in_path}")
        return None

    return in_path, out_path


def sitk_array_to_image(arr, ref_img):
    """
    Convert a NumPy array to a SimpleITK image, using the reference image's
    metadata.
    """
    img = sitk.GetImageFromArray(arr)
    img.CopyInformation(ref_img)
    return img


def convert_seg(
    raw_seg_path: Path, output_dir: Path
) -> list[tuple[Path, Path]]:
    dcm = pydicom.dcmread(raw_seg_path)

    reader = pydicom_seg.SegmentReader()
    try:
        dcm_seg = reader.read(dcm)
    except ValueError as e:
        log.error(f"Error reading segmentation ({raw_seg_path})")
        return []        
    paths = []
    for segment_ID in dcm_seg.available_segments:
        try:
            segment_meta = dcm_seg.segment_infos[segment_ID]
        except Exception as e:
            log.error("Error reading segment {segment_ID} in {raw_seg_path}")
            continue
        roi = segment_meta.SegmentLabel.replace(" ", "_")
        output_path = output_dir / f"seg_{roi}.nii.gz"
        if output_path.exists():
            log.warn("Output path already exists: %s", output_path)
        output_path.parent.mkdir(exist_ok=True, parents=True)
        try:
            image = dcm_seg.segment_image(segment_ID)
        except ValueError:
            log.error(
                "Segment %s not found in %s", segment_ID, raw_seg_path
            )
            continue
        sitk.WriteImage(image, str(output_path))
        paths.append((raw_seg_path, output_path))
    return paths


def convert_seg_dataset(
    raw_seg_paths: Iterable[Path], output_dir: Path, n_jobs=4
) -> pd.DataFrame:
    kwargs = (
        dict(
            raw_seg_path=raw_seg_path,
            output_dir=output_dir / raw_seg_path.parents[2].name,
        )
        for raw_seg_path in raw_seg_paths
    )
    conversion_paths_nested = pqdm(
        kwargs,
        convert_seg,
        n_jobs=n_jobs,
        argument_type="kwargs",
    )
    conversion_paths = [
        path for paths in conversion_paths_nested for path in paths
    ]
    conversion_df = create_conversion_df(conversion_paths)

    return conversion_df


def convert_rt(
    dcm_img,
    dcm_rt_path,
    output_dir,
    prefix="seg_",
    out_img_stem=None,
):
    Path(output_dir).mkdir(exist_ok=True, parents=True)
    convert_rtstruct(
        dcm_img=dcm_img,
        dcm_rt_file=dcm_rt_path,
        output_dir=output_dir,
        prefix=prefix,
        output_img=out_img_stem,
    )
    converted_paths = []
    if out_img_stem:
        derived_img_path = output_dir / f"{out_img_stem}.nii.gz"
        if not derived_img_path.exists():
            log.warning("Converted image does not exist: %s", derived_img_path)
        else:
            converted_paths.append((dcm_img, derived_img_path))
    derived_seg_paths = list(output_dir.glob(f"{prefix}*.nii.gz"))
    converted_paths.extend(
        [
            (dcm_rt_path, str(derived_seg_path))
            for derived_seg_path in derived_seg_paths
        ]
    )
    return converted_paths


def create_conversion_df(conversion_paths, dicom_dir=None, output_dir=None):
    conversion_df = pd.DataFrame(
        conversion_paths, columns=["raw_path", "derived_path"]
    )
    if dicom_dir is not None and output_dir is not None:
        conversion_df["raw_path"] = conversion_df["raw_path"].apply(
            lambda x: x.relative_to(dicom_dir)
        )
        conversion_df["derived_path"] = conversion_df["derived_path"].apply(
            lambda x: x.relative_to(output_dir)
        )
    conversion_df = conversion_df.astype("str")
    return conversion_df


def is_dicom_a_match(dcm_img: pydicom.Dataset, dcm_seg: pydicom.Dataset):
    img_id = dcm_img.SeriesInstanceUID
    if dcm_seg.Modality == "SEG":
        try:
            referenced_id = dcm_seg.ReferencedSeriesSequence[
                0
            ].SeriesInstanceUID
        except AttributeError:
            log.warning(
                f"Could not find ReferencedSeriesSequence for DICOM SEG: {dcm_seg.PatientID}"
            )
            return False
    elif dcm_seg.Modality == "RTSTRUCT":
        try:
            referenced_id = (
                dcm_seg.ReferencedFrameOfReferenceSequence[0]
                .RTReferencedStudySequence[0]
                .RTReferencedSeriesSequence[0]
                .SeriesInstanceUID
            )
        except AttributeError:
            log.warning(
                f"Could not find info about referenced series for RTSTRUCT: {dcm_seg.PatientID}"
            )
            return False
    else:
        log.error(
            f"Unknown Modality {dcm_seg.Modality} for DICOM file {dcm_seg.PatientID}"
        )
        return False
    return img_id == referenced_id


def find_matching_img(
    rtstruct_path: Path, dcm_img_data: Path | Iterable[Path]
):
    dicom_dirs = get_dicom_dirs(dcm_img_data)
    for dicom_dir in dicom_dirs:
        dcm_img_path = next(dicom_dir.glob("*.dcm"))
        dcm_img = pydicom.dcmread(dcm_img_path)
        dcm_seg = pydicom.dcmread(rtstruct_path)
        if not dcm_img.Modality == "MR" and not dcm_img.Modality == "CT":
            pass
        assert dcm_seg.Modality == "RTSTRUCT"
        if is_dicom_a_match(dcm_img, dcm_seg):
            return dcm_img_path.parent
    log.error(f"No matching image found for {rtstruct_path}")


def convert_rt_dataset(
    raw_img_paths, raw_rt_paths, derived_nifti_dir, out_fname=None, n_jobs=8
):
    output_dirs = [
        derived_nifti_dir / Path(p).parents[1].name for p in raw_img_paths
    ]
    if not isinstance(out_fname, list):
        out_fnames = [out_fname for _ in output_dirs]
    else:
        out_fnames = out_fname
    prefixes = [f"seg_{out_fname}_" for out_fname in out_fnames]
    arg_dict = dict(
        dcm_img=raw_img_paths,
        dcm_rt_path=raw_rt_paths,
        output_dir=output_dirs,
        prefix=prefixes,
        out_img_stem=out_fnames,
    )
    args = pd.DataFrame(arg_dict).to_dict(orient="records")
    conversion_paths_nested = pqdm(
        args, convert_rt, n_jobs=n_jobs, argument_type="kwargs"
    )
    conversion_paths = [
        item for sublist in conversion_paths_nested for item in sublist if item
    ]
    conversion_df = create_conversion_df(conversion_paths)

    return conversion_df


def is_rtstruct(dcm_path):
    dcm_img = pydicom.dcmread(dcm_path)
    return dcm_img.Modality == "RTSTRUCT"


def get_modality(dcm_path):
    dcm_img = pydicom.dcmread(dcm_path)
    return dcm_img.Modality

def get_dcm_tag(tag, dcm_dir):
    dcm_path = next(dcm_dir.glob("*.dcm"))
    dcm_img = pydicom.dcmread(dcm_path)
    return dcm_img[tag].value