## MGMT methylation status prediction for brain tumor (BraTS-2021)

1. Register and download the data from [Synapse.org](https://www.synapse.org/#!Synapse:syn25829067/wiki/610865).
   Put the downloaded folder `training_data` in `<your_base_dir>/raw`

2. Download `train_labels.csv` from [BraTS Kaggle Competition](https://www.kaggle.com/competitions/rsna-miccai-brain-tumor-radiogenomic-classification/data?select=train_labels.csv).
   Put it in `<your_base_dir>/raw/tables`.

3. Your data directory should look like this:

```
<your_base_folder>
└── raw
    ├── training_data
    │   ├── BraTS2021_00001
    │   │   ├── BraTS2021_00001_flair.nii.gz
    │   │   ├── BraTS2021_00001_t1.nii.gz
    │   │   ...
    └── train_labels.csv
```

Update `base_dir` in [config.py](radfeat/BraTS-2021/config.py).

3. Run processing script:

```bash
   cd radiomics-features/radfeat/BraTS_2021
   python .
```

## Notes

## References

[1] U.Baid, et al., The RSNA-ASNR-MICCAI BraTS 2021 Benchmark on Brain Tumor Segmentation and Radiogenomic Classification, arXiv:2107.02314, 2021.

[2] B. H. Menze, A. Jakab, S. Bauer, J. Kalpathy-Cramer, K. Farahani, J. Kirby, et al. "The Multimodal Brain Tumor Image Segmentation Benchmark (BRATS)", IEEE Transactions on Medical Imaging 34(10), 1993-2024 (2015) DOI: 10.1109/TMI.2014.2377694

[3] S. Bakas, H. Akbari, A. Sotiras, M. Bilello, M. Rozycki, J.S. Kirby, et al., "Advancing The Cancer Genome Atlas glioma MRI collections with expert segmentation labels and radiomic features", Nature Scientific Data, 4:170117 (2017) DOI: 10.1038/sdata.2017.117
