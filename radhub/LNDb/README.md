## LIDC-IDRI dataset

## Steps

1. Download dataset (`data0-data5.rar] from https://zenodo.org/record/6613714#.Y8rTA9LMJkh \\
Unpack them to a folder `<your_base_dir>/raw/mhd/img`.

2. Download segmentations `masks.rar` from the same link. Unpack them to the folder `<your_base_dir>/raw/mhd/seg`.

3. Download `trainset_csv.zip` from zenodo and unpack the csv tables inside to `<your_base_dir>/raw/tables/`.

4. Edit the base_path in [config.py](config.py)

5. Run the preprocessing and feature extraction:

```bash
   cd radiomics-features/radhub/
   python .
```

### Labels

Fleischner scores are used as labels. They are converted to numerical values as follows:

- 0: No routine follow-up required or optional CT at 12 months according to patient risk
- 1: CT at 6-12 months required
- 2: CT at 3-6 months required
- 3: CT, PET/CT or tissue sampling at 3 months required

## Notes

Only nodules >3mm were segmented, smaller nodules and non-nodules were only annotated with centroids and had to be thus excluded from feature extraction.

## Citation

`Pedrosa, João, et al. "LNDb: a lung nodule database on computed tomography." arXiv preprint arXiv:1911.08434 (2019).`
`Pedrosa, João, et al. "LNDb challenge on automatic lung cancer patient management." Medical image analysis 70 (2021): 102027.`
