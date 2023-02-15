import logging

import pandas as pd

from radhub import master_config
from radhub.UPENN_GBM import config, preprocess, extract

log = logging.getLogger(__name__)


def run_pipeline():

    master_config.configure_logging(config.log_dir)

    text = " Creating tables with paths and labels (1/2)"
    log.info(f"{text:#^80}")

    paths_df = preprocess.create_ref_table(
        config.raw_data_dir, config.raw_seg_dir
    )
    paths_df.to_csv(config.derived_table_dir / "paths.csv", index=False)

    label_df = pd.read_csv(
        config.raw_table_dir / "UPENN-GBM_clinical_info_v1.0.csv"
    )
    label_df.to_csv(config.derived_table_dir / "labels.csv", index=False)

    text = " Extracting features (2/2)"
    log.info(f"{text:#^80}")

    paths_df = pd.read_csv(config.derived_table_dir / "paths.csv")
    extract.extract_features(paths_df, save_dir=config.derived_table_dir)


if __name__ == "__main__":
    run_pipeline()
