## Radiomics Features from Public Medical Imaging Datasets

This repo gathers together the available open-source datasets suitable for radiomics research.

More information about each dataset and the extracted radiomics features as well as the labels can be accessed at **https://radiomics.uk**.

## Datasets

| Dataset Name           | Website                                                                                 | Status |
| ---------------------- | --------------------------------------------------------------------------------------- | ------ |
| BraTS 2021             | [Kaggle](https://www.kaggle.com/datasets/dschettler8845/brats-2021-task1)               | ✔️     |
| LIDC-IDRI              | [TCIA](https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=1966254)      | ✔️     |
| LNDb                   | [Zenodo](https://zenodo.org/record/6613714#.Y8rTA9LMJkh)                                | ✔️     |
| UPENN-GBM                   | [TCIA](https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=70225642#70225642c94d520b7b5f42e7925602d723412459)                                | ✔️     |
| LUAD-CT-Survival | [TCIA](https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=24284406#24284406036220c66a5a436f90e4a0b54367bfae)     | ✔️     |
| RIDER-Lung-CT | [TCIA](https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=46334165) | ✔️     |
| PI-CAI                 | [Grand Challenge](https://pi-cai.grand-challenge.org/)                                  | ✔️     |
| QIN-PROSTATE           | [TCIA](https://wiki.cancerimagingarchive.net/display/Public/QIN-PROSTATE-Repeatability) | ✔️     |
| Prostate-MRI-US-Biopsy | [TCIA](https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=68550661)     | ✔️     |
| Soft-tissue-Sarcoma    | [TCIA](https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=21266533)                                          | ✔️     |
| WORC                   | [GitHub](https://github.com/MStarmans91/WORCDatabase)                                   | ✔️     |
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
