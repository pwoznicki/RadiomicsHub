import config
import pandas as pd

from autorad.data.dataset import ImageDataset
from autorad.feature_extraction.extractor import FeatureExtractor

def extract_features(paths_df):
    image_dset = ImageDataset(
        paths_df,
        ID_colname="seg_ID",
        image_colname="img_path",
        mask_colname="seg_path",
    )
    extractor = FeatureExtractor(
        image_dset, extraction_params="CT_default.yaml",
    )
    feature_df = extractor.run()
    return feature_df

if __name__ == "__main__":

    paths_df = pd.read_csv(config.table_dir / "paths.csv")
    feature_df = extract_features(paths_df)
    feature_df.to_csv(config.table_dir / "features.csv", index=False)
