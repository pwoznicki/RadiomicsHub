## WORC database

The database contains 6 separate datasets:
- CRLM
- Desmoid
- GIST
- Lipo
- Liver
- Melanoma

Each dataset has binary labels.

## Requirements

## Steps

1. Download images from WORC [XNAT repository](https://xnat.bmia.nl/data/projects/worc) (`Actions -> Download Images`).
   By default, you will download all 6 datasets.

   The downloaded data will look like:
   ```
   ├── Melanoma-001_CT
   ├── Melanoma-002_CT
   ...
   ├── Liver-001_MR
   ├── Liver-002_MR
   ...
   ├── Lipo-001_MR
   ├── Lipo-002_MR
   ...
   ```

To process one dataset (e.g. Melanoma):

a. move its all cases to a folder `<your_dataset_dir>/raw/nifti`.

b. Download table from [XNAT repository](https://xnat.bmia.nl/data/projects/worc) (`Scroll down to Subjects -> Options -> Spreadsheet`). Save it as `<your_dataset_dir/raw/tables/labels.csv`.

c. Run the preprocessing and feature extraction:

```bash
   cd radiomics-features/radhub/
   python . --dataset <selected_dataset> --dataset-path <your_dataset_dir>
   # e.g. python . --dataset Melanoma --dataset-path /home/user/data/WORC-Melanoma
```

## Notes


## Citation

Starmans, M. P. A. et al. (2021). The WORC\* database: MRI and CT scans, segmentations, and clinical labels for 932 patients from six radiomics studies. Submitted, preprint available from https://doi.org/10.1101/2021.08.19.21262238

The experiments are described in the following paper: Starmans, M. P. A. et al. (2021). Reproducible radiomics through automated machine learning validated on twelve clinical applications. Submitted, preprint available from https://arxiv.org/abs/2108.08618.
