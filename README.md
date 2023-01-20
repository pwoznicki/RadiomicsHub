## Radiomics Features from Public Medical Imaging Datasets

This repo gathers together the available open-source datasets suitable for radiomics research.

More information about each dataset and the extracted radiomics features as well as the labels can be accessed at **https://radiomics.uk**.

## Datasets

| Dataset Name | Website                                                                                 | Status |
| ------------ | --------------------------------------------------------------------------------------- | ------ |
| BraTS 2021   | [Kagglej](https://www.kaggle.com/datasets/dschettler8845/brats-2021-task1)              | ✔️     |
| LIDC-IDRI    | [TCIA](https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=1966254)      | ✔️     |
| LNDb         | [Zenodo](https://zenodo.org/record/6613714#.Y8rTA9LMJkh)                                | ✔️     |
| PI-CAI       | [GrandChallenge](https://pi-cai.grand-challenge.org/)                                   | ✔️     |
| QIN-PROSTATE | [TCIA](https://wiki.cancerimagingarchive.net/display/Public/QIN-PROSTATE-Repeatability) | ✔️     |

## Folder structure

Each dataset adheres to the following structure:

```
<dataset_name>
├── raw
│   ├── dicom       # depending on the format of the original dataset
|   |   ├── img     # raw images
|   |   └── seg     # raw segmentations
│   └── tables
└── derived
    ├── nifti
    │   ├── img    # converted .nii.gz images
    │   └── seg    # converted .nii.gz segmentations
    └── tables
```
