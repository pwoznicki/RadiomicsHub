## Meningioma-SEG-CLASS dataset

## Requirements

- for download from TCIA, you may use CLI tool https://wiki.cancerimagingarchive.net/display/NBIA/NBIA+Data+Retriever+Command-Line+Interface+Guide or the GUI program.


## Steps

1. Download images (DICOM) and segmentations (DICOM RT) from [TCIA](https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=133071972#13307197205162a1cd631405587dec16c83836772) (takes a while...) \\
   Save them to `<your_base_dir>/raw/dicom`.

2. In the same link, download the table with **Clinical Data** (Meningioma-SEG-Class Clinical Data.xlsx). Save it as`<your_base_dir>/raw/tables/Clinical_data.xlsx`.

3. Edit the base_path in [config.py](config.py)

4. Run the preprocessing and feature extraction:

```bash
   cd radiomics-features/radhub/Meningioma_SEG_CLASS
   python .
```

## Notes

For each case, there are two RTSTRUCT tumor masks, performed for two sequences. Typically these sequences are axial T1 CD (T3D Stealth ?) and T2 FLAIR. However, sometimes other sequences were used, e.g. T2 TIRM, T2 FLAIR FS instead of T2 FLAIR.

Meningioma-SEG-CLASS-094 has segmentations for two tumors (all the other cases have only one tumor). It was excluded from the analysis.

## Citation

**Data citation**:
`Vassantachart, A., Cao, Y., Shen, Z., Cheng, K., Gribble, M., Ye, J. C., Zada, G., Hurth, K., Mathew, A., Guzman, S., & Yang, W. (2023). Segmentation and Classification of Grade I and II Meningiomas from Magnetic Resonance Imaging: An Open Annotated Dataset (Meningioma-SEG-CLASS) (Version 1) [Data set]. The Cancer Imaging Archive. https://doi.org/10.7937/0TKV-1A36`

**Publication citation**:
`Vassantachart, A., Cao, Y., Gribble, M., Guzman, S., Ye, J. C., Hurth, K., Mathew, A., Zada, G., Fan, Z., Chang, E. L., & Yang, W. (2022). Automatic differentiation of Grade I and II meningiomas on magnetic resonance image using an asymmetric convolutional neural network. In Scientific Reports (Vol. 12, Issue 1). Springer Science and Business Media LLC. https://doi.org/10.1038/s41598-022-07859-0`

**TCIA citation**:
`Clark, K., Vendt, B., Smith, K., Freymann, J., Kirby, J., Koppel, P., Moore, S., Phillips, S., Maffitt, D., Pringle, M., Tarbox, L., & Prior, F. (2013). The Cancer Imaging Archive (TCIA): Maintaining and Operating a Public Information Repository. Journal of Digital Imaging, 26(6), 1045–1057. https://doi.org/10.1007/s10278-013-9622-7`
