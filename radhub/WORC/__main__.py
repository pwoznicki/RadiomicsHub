import argparse
import logging
from pathlib import Path

import pandas as pd

from radhub import master_config, utils
from radhub.WORC import config, extract, preprocess

log = logging.getLogger(__name__)


def run_pipeline(dataset_name: str, dataset_dir: Path, extraction_params=None):
    if not dataset_name in config.datasets:
        raise ValueError(f"Dataset {dataset_name} not in {config.datasets}")

    master_config.configure_logging(dataset_dir / "logs")

    utils.pretty_log("Creating table with paths (1/2)")
    raw_label_df = pd.read_csv(dataset_dir / "raw" / "tables" / "labels.csv")
    raw_label_df = raw_label_df[
        ~raw_label_df["Subject"].isin(config.excluded_subjects)
    ]

    path_df, label_df = preprocess.create_path_df_for_single_dataset(
        dataset_name=dataset_name,
        raw_label_df=raw_label_df,
        dataset_dir=dataset_dir,
    )

    derived_table_dir = dataset_dir / "derived" / "tables"
    derived_table_dir.mkdir(parents=True, exist_ok=True)
    path_df.to_csv(
        derived_table_dir / "paths.csv",
        index=False,
    )
    label_df.to_csv(
        derived_table_dir / "labels.csv",
        index=False,
    )

    utils.pretty_log("Extracting features (2/2)")
    if not extraction_params:
        extraction_params = extract.get_pyradiomics_param_file(dataset_name)
    feature_df = utils.extract_features(
        path_df,
        ID_colname="subject_ID",
        extraction_params=extraction_params,
    )
    feature_df.to_csv(derived_table_dir / f"features.csv", index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset",
        type=str,
        help="Name of the dataset to run the pipeline on",
        choices=config.datasets,
    )
    parser.add_argument(
        "--dataset-path",
        type=Path,
        help="Path to the dataset directory",
    )
    args = parser.parse_args()
    run_pipeline(args.dataset, Path(args.dataset_path))
