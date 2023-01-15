import config
import pandas as pd
from autorad.data.dataset import ImageDataset
from autorad.feature_extraction.extractor import FeatureExtractor


def extract_features(paths_df):
    image_dset = ImageDataset(
        paths_df,
        ID_colname="img_ID",
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
        roi_feature_df.to_csv(
            config.table_dir / f"features_{ROI}.csv", index=False
        )


if __name__ == "__main__":

    paths_df = pd.read_csv(config.table_dir / "paths.csv")
    extract_features(paths_df)
