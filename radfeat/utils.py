import logging

import SimpleITK as sitk
from autorad.data.dataset import ImageDataset
from autorad.feature_extraction.extractor import FeatureExtractor

logging.getLogger().setLevel(logging.CRITICAL)


def extract_features(
    paths_df, ID_colname, extraction_params="CT_default.yaml", n_jobs=-1
):
    image_dset = ImageDataset(
        paths_df,
        ID_colname=ID_colname,
        image_colname="img_path",
        mask_colname="seg_path",
    )
    extractor = FeatureExtractor(
        image_dset,
        extraction_params=extraction_params,
        n_jobs=n_jobs,
    )
    feature_df = extractor.run()
    return feature_df


def convert_sitk(in_path, out_path):
    if not in_path.exists():
        raise FileNotFoundError
    data = sitk.ReadImage(in_path)
    out_path.parent.mkdir(exist_ok=True, parents=True)
    sitk.WriteImage(data, out_path)


def sitk_array_to_image(arr, ref_img):
    """
    Convert a NumPy array to a SimpleITK image, using the reference image's
    metadata.
    """
    img = sitk.GetImageFromArray(arr)
    img.CopyInformation(ref_img)
    return img
