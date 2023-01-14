import config
from pathlib import Path
import pandas as pd
from autorad.data.dataset import ImageDataset
from autorad.feature_extraction.extractor import FeatureExtractor

# get path of this file with pathlib

def extract_features(paths_df):
    image_dset = ImageDataset(
        paths_df,
        ID_colname="series_ID",
        image_colname="img_path",
        mask_colname="seg_path",
    )
    ROIs = ["necrotic_core", "enhancing_tumor", "peritumoral_edema"]
    feature_df = pd.DataFrame()
    for ROI in ROIs:
        extractor = FeatureExtractor(
            dataset=image_dset,
            extraction_params=f"{Path(__file__).parent}/extraction_params/{ROI}.yaml",
            n_jobs=12,
        )
        roi_feature_df = extractor.run()
        roi_feature_df.to_csv(
            config.table_dir / f"features_{ROI}.csv", index=False
        )
        roi_feature_df.insert(3, "ROI", ROI)
        feature_df = pd.concat([feature_df, roi_feature_df], axis=0)
    feature_df.sort_values(by=["patient_ID", "sequence", "ROI"], inplace=True)
    feature_df.to_csv(
        config.table_dir / f"features.csv", index=False
    )


if __name__ == "__main__":

    paths_df = pd.read_csv(config.table_dir / "paths.csv")
    extract_features(paths_df)
