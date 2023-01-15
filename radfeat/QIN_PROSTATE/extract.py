import logging

import pandas as pd
from autorad.data.dataset import ImageDataset
from autorad.feature_extraction.extractor import FeatureExtractor


def extract_features(paths_df: pd.DataFrame) -> pd.DataFrame:

    image_dset = ImageDataset(
        paths_df,
        ID_colname="series_ROI_ID",
        image_colname="img_path",
        mask_colname="seg_path",
    )
    extractor = FeatureExtractor(
        dataset=image_dset,
        extraction_params="MR_default.yaml",
        n_jobs=12,
    )
    feature_df = extractor.run()

    return feature_df
