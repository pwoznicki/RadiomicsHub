## PI-CAI: Detecting clinically significant prostate cancer

## Steps

1. Download the images from [zenodo](https://zenodo.org/record/6517398#.YzRKVdJBxhE) (1476 cases) and unpack them to the folder <your_base_dir>/raw/mha/img.
2. Clone the repo with the segmentations:

```
cd <your_base_dir>/raw/mha
git clone https://github.com/DIAGNijmegen/picai_labels
```

### Important facts

- The PI-CAI dataset includes cases from ProstateX.
- Only the segmentations from human experts are included here (available for 86% cases). The segmentations from AI model are available as well.

### Problems

- Only csPCa are segmented, so only 220 / 1476 have manual lesion segmentations. Either whole gland or automatic segmentation could be used here.
