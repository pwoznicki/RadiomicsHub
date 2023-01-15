### Detecting clinically significant prostate cancer

1. Download the images from [zenodo](https://zenodo.org/record/6517398#.YzRKVdJBxhE) (1476 cases) and unpack them to selected folder.
2. clone the repo with the segmentations:
```
git clone https://github.com/DIAGNijmegen/picai_labels
```


### Important facts
- The PI-CAI dataset includes cases from ProstateX.
- Only the segmentations from human experts are included here (available for 86% cases). The segmentations from AI model are available.


### Problems
- Only csPCa are segmented, so only 220 / 1476 have manual lesion segmentations. Either whole gland or automatic segmentation could be used here.
