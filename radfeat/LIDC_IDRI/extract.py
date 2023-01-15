import config
import pandas as pd
from rad-db import utils

if __name__ == "__main__":

    paths_df = pd.read_csv(config.base_dir / "paths.csv")
    feature_df = utils.extract_features(paths_df)
    feature_df.to_csv("features.csv", index=False)
