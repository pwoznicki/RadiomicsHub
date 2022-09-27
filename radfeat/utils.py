import logging


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
