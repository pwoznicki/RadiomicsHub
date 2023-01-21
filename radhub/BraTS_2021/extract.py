import logging
from pathlib import Path

import pandas as pd
from autorad.data.dataset import ImageDataset
from autorad.feature_extraction.extractor import FeatureExtractor

log = logging.getLogger(__name__)


def extract_features(paths_df: pd.DataFrame) -> pd.DataFrame:
    image_dset = ImageDataset(
        paths_df,
        ID_colname="series_ID",
        image_colname="img_path",
        mask_colname="seg_path",
    )
    ROIs = ["necrotic_core", "enhancing_tumor", "peritumoral_edema"]
    feature_df = pd.DataFrame()
    for i, roi in enumerate(ROIs):
        log.info(f"Extracting features for {roi}... ({i+1}/{len(ROIs)}")
        param_path = Path(__file__).parent / f"extraction_params/{roi}.yaml"
        extractor = FeatureExtractor(
            dataset=image_dset,
            extraction_params=param_path,
            n_jobs=8,
        )
        roi_feature_df = extractor.run()
        roi_feature_df.insert(3, "ROI", roi)
        feature_df = pd.concat([feature_df, roi_feature_df], axis=0)
    feature_df.sort_values(by=["patient_ID", "sequence", "ROI"], inplace=True)

    return feature_df
