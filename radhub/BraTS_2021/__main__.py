import logging

import pandas as pd

from radhub import master_config
from radhub.BraTS_2021 import extract, preprocess
from radhub.BraTS_2021.config import config

log = logging.getLogger(__name__)


def run_pipeline():

    master_config.configure_logging(config.log_dir)

    text = " Creating reference table (1/2) "
    log.info(f"{text:#^80}")

    raw_label_df = pd.read_csv(config.raw_table_dir / "train_labels.csv")
    label_df = preprocess.process_label_df(raw_label_df)
    label_df.to_csv(config.derived_table_dir / "labels.csv", index=False)

    path_df = preprocess.create_path_df(config.raw_data_dir, label_df)
    path_df.to_csv(config.derived_table_dir / "paths.csv", index=False)

    text = " Extracting features (2/2) "
    log.info(f"{text:#^80}")

    feature_df = extract.extract_features(path_df)
    feature_df.to_csv(config.derived_table_dir / f"features.csv", index=False)


if __name__ == "__main__":
    run_pipeline()
