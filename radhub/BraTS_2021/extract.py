import logging

import pandas as pd

from radhub import utils

log = logging.getLogger(__name__)


def extract_features(paths_df: pd.DataFrame) -> pd.DataFrame:
    ROIs = [
        ("necrotic_core", 1),
        ("enhancing_tumor", 2),
        ("peritumoral_edema", 4),
    ]
    feature_df = pd.DataFrame()
    for roi, mask_label in ROIs:
        log.info(f"Extracting features for {roi}...")
        roi_feature_df = utils.extract_features(
            paths_df=paths_df,
            ID_colname="series_ID",
            extraction_params="MR_default.yaml",
            mask_label=mask_label,
        )
        roi_feature_df.insert(3, "ROI", roi)
        feature_df = pd.concat([feature_df, roi_feature_df], axis=0)
    feature_df.sort_values(by=["patient_ID", "sequence", "ROI"], inplace=True)

    return feature_df
