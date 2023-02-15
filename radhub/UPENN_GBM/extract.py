import config
import pandas as pd
from autorad.data.dataset import ImageDataset
from autorad.feature_extraction.extractor import FeatureExtractor


def extract_features(paths_df, save_dir):
    image_dset = ImageDataset(
        paths_df,
        ID_colname="series_ID",
        image_colname="img_path",
        mask_colname="seg_path",
    )
    ROIs = ["necrotic_core", "enhancing_tumor", "peritumoral_edema"]
    for ROI in ROIs:
        extractor = FeatureExtractor(
            dataset=image_dset,
            extraction_params=f"./extraction_params/{ROI}.yaml",
            n_jobs=12,
        )
        roi_feature_df = extractor.run()
        roi_feature_df.to_csv(save_dir / f"features_{ROI}.csv", index=False)
