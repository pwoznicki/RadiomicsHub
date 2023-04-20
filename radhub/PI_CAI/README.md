## PI-CAI: Detecting clinically significant prostate cancer

## Steps

1. Download the images from [zenodo](https://zenodo.org/record/6517398#.YzRKVdJBxhE) (1476 cases) and unpack them to the folder <your_base_dir>/raw/mha/img.
2. Clone the repo with the whole prostate & lesion segmentations as well as the labels:

```
cd <your_base_dir>/raw
git clone https://github.com/DIAGNijmegen/picai_labels
```

### Important facts

- The PI-CAI dataset includes cases from ProstateX.
- Only the segmentations from human experts are included here (available for 86% cases). The segmentations from AI model are available as well.

### Notes

- Many of lesion masks are empty.
- Only csPCa were segmented in the dataset, so only 220 / 1476 have manual lesion segmentations. Either whole gland or automatic segmentation could be used here.

## Citation
**Dataset/challenge citation**:
`A. Saha, J. J. Twilt, J. S. Bosma, B. van Ginneken, D. Yakar, M. Elschot, J. Veltman, J. J. Fütterer, M. de Rooij, H. Huisman, "Artificial Intelligence and Radiologists at Prostate Cancer Detection in MRI: The PI-CAI Challenge (Study Protocol)", DOI: https://doi.org/10.5281/zenodo.6522364`

**Publication citation**:
<not yet available>