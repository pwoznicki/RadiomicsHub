import logging

import SimpleITK as sitk
from autorad.data.dataset import ImageDataset
from autorad.feature_extraction.extractor import FeatureExtractor

logging.getLogger().setLevel(logging.CRITICAL)


def extract_features(paths_df):
    image_dset = ImageDataset(
        paths_df,
        ID_colname="seg_ID",
        mask_colname="seg_path",
    )
    extractor = FeatureExtractor(
        image_dset, extraction_params="CT_default.yaml"
    )
    feature_df = extractor.run()
    return feature_df


def convert_sitk(in_path, out_path):
    if not in_path.exists():
        raise FileNotFoundError
    data = sitk.ReadImage(in_path)
    out_path.parent.mkdir(exist_ok=True)
    sitk.WriteImage(data, out_path)
