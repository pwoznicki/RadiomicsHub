## Radiomics Features from Public Medical Imaging Datasets

This repo gathers together the available open-source datasets suitable for radiomics research.

More information about each dataset and the extracted radiomics features as well as the labels can be accessed at **https://radiomics.uk**.

## Datasets

| Dataset Name           | Website                                                                                 | Task | Status |
| ---------------------- | --------------------------------------------------------------------------------------- | ------ | ---- |
| LIDC-IDRI              | [TCIA](https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=1966254)      | binary classification | ✔️     |
| LNDb                   | [Zenodo](https://zenodo.org/record/6613714#.Y8rTA9LMJkh)                                | multiclass classification | ✔️     |
| NSCLC-Radiogenomics | [TCIA](https://wiki.cancerimagingarchive.net/display/Public/NSCLC+Radiogenomics#286723474bf3bc54d8c14b93ba3b3b874b5b1a0b)     | survival analysis | ✔️     |
| NSCLC-Radiomics | [TCIA](https://wiki.cancerimagingarchive.net/display/Public/NSCLC-Radiomics)     | survival analysis | ✔️     |
| LUAD-CT-Survival | [TCIA](https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=24284406#24284406036220c66a5a436f90e4a0b54367bfae)     | binary classification | ✔️     |
| RIDER-Lung-CT | [TCIA](https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=46334165) | repeatability | ✔️     |
| BraTS-2021             | [Kaggle](https://www.kaggle.com/datasets/dschettler8845/brats-2021-task1)               | binary classification | ✔️     |
| UCSF-PDGM | [TCIA](https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=119705830#1197058307e324bc732ef415a86e5ac4b072a65f2)                                | binary classification, survival analysis| ✔️     |
| UPENN-GBM                   | [TCIA](https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=70225642#70225642c94d520b7b5f42e7925602d723412459)                                | survival analysis | ✔️     |
| Meningioma-SEG-CLASS | [TCIA](https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=133071972#13307197205162a1cd631405587dec16c83836772)                                | binary classification | ✔️     |
| LGG-1p19qDeletion | [TCIA](https://wiki.cancerimagingarchive.net/display/Public/LGG-1p19qDeletion#25789042f10ce39add5847a4914c1e541428cf8b)                               | binary classification | ✔️     |
| PI-CAI                 | [Grand Challenge](https://pi-cai.grand-challenge.org/)                                 | multiclass classification | ✔️     |
| Prostate-MRI-US-Biopsy | [TCIA](https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=68550661)    | multiclass classification | ✔️     |
| QIN-PROSTATE           | [TCIA](https://wiki.cancerimagingarchive.net/display/Public/QIN-PROSTATE-Repeatability) | repeatability | ✔️     |
| Head-Neck-Radiomics-HN1 | [TCIA](https://wiki.cancerimagingarchive.net/display/Public/Head-Neck-Radiomics-HN1) | survival analysis | ✔️     |
| HNSCC | [TCIA](https://wiki.cancerimagingarchive.net/display/Public/HNSCC) | survival analysis | ✔️     |
| Head-Neck-PET-CT | [TCIA](https://wiki.cancerimagingarchive.net/display/Public/Head-Neck-PET-CT) | survival analysis | ✔️     |
| OPC-Radiomics | [TCIA](https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=33948764) | survival analysis | ✔️     |
| QIN-HEADNECK | [TCIA](https://wiki.cancerimagingarchive.net/display/Public/QIN-HEADNECK)                                         | repeatability | ✔️     |
| Colorectal-Liver-Metastases | [TCIA](https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=89096268#890962686311a10d4c514199bbe0273c4d8d7abe)                                          | survival analysis | ✔️     |
| HCC-TACE-Seg | [TCIA](https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=70230229)                                        | survival analysis  | ✔️     |
| C4KC-KiTS | [TCIA](https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=61081171)                                          | survival analysis | ✔️     |
| Soft-Tissue-Sarcoma | [TCIA](https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=21266533)                                          | binary classification | ✔️     |
| WORC                   | [GitHub](https://github.com/MStarmans91/WORCDatabase)                                   | binary classification | ✔️     |
## Folder structure

Each dataset adheres to the following structure, with minor variations:

```
<dataset_name>
├── raw
│   ├── dicom       # depending on the format of the original dataset
│   └── tables
└── derived
    ├── nifti       # converted to NIfTI format
    └── tables
```
