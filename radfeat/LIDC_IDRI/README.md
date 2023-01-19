## LIDC-IDRI dataset

## Requirements

- [dcm2niix](https://github.com/rordenlab/dcm2niix) (version 20-July-2022 or newer, don't use an old version from `apt`)

- for download from TCIA, you may use CLI tool https://wiki.cancerimagingarchive.net/display/NBIA/NBIA+Data+Retriever+Command-Line+Interface+Guide or the GUI program.

## Steps

1. Download DICOM images from https://wiki.cancerimagingarchive.net/display/Public/LIDC-IDRI#1966254194132fe653e4a7db00715f6f775c012 (takes a while...) \\
   Save them in a folder `<your_base_dir>/raw/dicom/img`.

2. Download segmentations (DICOM SEG) from https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=44499647
   Save them in `<your_base_dir>/raw/dicom/seg`.

3. Run the preprocessing and feature extraction:

```bash
   cd radiomics-features/radfeat/LIDC_IDRI
   python .
```

## Notes

8 cases have two CT series instead of one:
LIDC-IDRI-0132, LIDC-IDRI-0151, LIDC-IDRI-0315, LIDC-IDRI-0332, LIDC-IDRI-0355, LIDC-IDRI-0365, LIDC-IDRI-0442, LIDC-IDRI-0484
They were excluded from the analysis.

For 364 masks out of 5708 (6%), the extraction failed (most common due to ROI dimensionality too small for pyradiomics).

## Citation

### Images

**Data citation**:
`Armato III, S. G., McLennan, G., Bidaut, L., McNitt-Gray, M. F., Meyer, C. R., Reeves, A. P., Zhao, B., Aberle, D. R., Henschke, C. I., Hoffman, E. A., Kazerooni, E. A., MacMahon, H., Van Beek, E. J. R., Yankelevitz, D., Biancardi, A. M., Bland, P. H., Brown, M. S., Engelmann, R. M., Laderach, G. E., Max, D., Pais, R. C. , Qing, D. P. Y. , Roberts, R. Y., Smith, A. R., Starkey, A., Batra, P., Caligiuri, P., Farooqi, A., Gladish, G. W., Jude, C. M., Munden, R. F., Petkovska, I., Quint, L. E., Schwartz, L. H., Sundaram, B., Dodd, L. E., Fenimore, C., Gur, D., Petrick, N., Freymann, J., Kirby, J., Hughes, B., Casteele, A. V., Gupte, S., Sallam, M., Heath, M. D., Kuhn, M. H., Dharaiya, E., Burns, R., Fryd, D. S., Salganicoff, M., Anand, V., Shreter, U., Vastagh, S., Croft, B. Y., Clarke, L. P. (2015). Data From LIDC-IDRI [Data set]. The Cancer Imaging Archive. https://doi.org/10.7937/K9/TCIA.2015.LO9QL9SX`

**Publication citation**:
`Armato SG 3rd, McLennan G, Bidaut L, McNitt-Gray MF, Meyer CR, Reeves AP, Zhao B, Aberle DR, Henschke CI, Hoffman EA, Kazerooni EA, MacMahon H, Van Beeke EJ, Yankelevitz D, Biancardi AM, Bland PH, Brown MS, Engelmann RM, Laderach GE, Max D, Pais RC, Qing DP, Roberts RY, Smith AR, Starkey A, Batrah P, Caligiuri P, Farooqi A, Gladish GW, Jude CM, Munden RF, Petkovska I, Quint LE, Schwartz LH, Sundaram B, Dodd LE, Fenimore C, Gur D, Petrick N, Freymann J, Kirby J, Hughes B, Casteele AV, Gupte S, Sallamm M, Heath MD, Kuhn MH, Dharaiya E, Burns R, Fryd DS, Salganicoff M, Anand V, Shreter U, Vastagh S, Croft BY.  The Lung Image Database Consortium (LIDC) and Image Database Resource Initiative (IDRI): A completed reference database of lung nodules on CT scans. Medical Physics, 38: 915--931, 2011. DOI: https://doi.org/10.1118/1.3528204`

### Segmentations

**Data citation**:
`Fedorov, A., Hancock, M., Clunie, D., Brockhhausen, M., Bona, J., Kirby, J., Freymann, J., Aerts, H.J.W.L., Kikinis, R., Prior, F. (2018). Standardized representation of the TCIA LIDC-IDRI annotations using DICOM. The Cancer Imaging Archive. https://doi.org/10.7937/TCIA.2018.h7umfurq`

**Publication citation**:
`Fedorov, A., Hancock, M., Clunie,  D., Brochhausen, M., Bona, J., Kirby, J., Freymann, J, Pieper S, Aerts H.J.W.L., Kikinis, R., Prior, F. (2020) DICOM re‐encoding of volumetrically annotated Lung Imaging Database Consortium (LIDC) nodules. Medical Physics Dataset Article. https://doi.org/10.1002/mp.14445`

**TCIA citation**:
`Clark, K., Vendt, B., Smith, K., Freymann, J., Kirby, J., Koppel, P., Moore, S., Phillips, S., Maffitt, D., Pringle, M., Tarbox, L., & Prior, F. (2013). The Cancer Imaging Archive (TCIA): Maintaining and Operating a Public Information Repository. Journal of Digital Imaging, 26(6), 1045–1057. https://doi.org/10.1007/s10278-013-9622-7`
