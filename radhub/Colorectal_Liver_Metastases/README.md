## Colorectal-Liver-Metastases dataset

## Requirements

- for download from TCIA, you may use CLI tool https://wiki.cancerimagingarchive.net/display/NBIA/NBIA+Data+Retriever+Command-Line+Interface+Guide or the GUI program.

## Steps

1. Download DICOM images & segmentations from https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=1966254 (takes a while...) \\
   Save them in the folder `<your_base_dir>/raw/dicom`.

2. In the same link, download *Clinical data* table. Save it as`<your_base_dir>/raw/tables/Colorectal Liver Metastases Clinical data October 2022.xlsx`.

3. Edit the base_path in [config.py](config.py)

4. Run the preprocessing and feature extraction:

```bash
   cd radiomics-features/radhub/Colorectal_Liver_Metastases
   python .
```

## Notes
All the segmentation ROIs were used for feature extraction.

## Citation

**Data citation**:
`Simpson, A. L., Peoples, J., Creasy, J. M., Fichtinger, G., Gangai, N., Lasso, A., Keshava Murthy, K. N., Shia, J., D’Angelica, M. I., & Do, R. K. G. (2023). Preoperative CT and Recurrence for Patients Undergoing Resection of Colorectal Liver Metastases (Colorectal Liver Metastases) (Version 1) [Data set]. The Cancer Imaging Archive. https://doi.org/10.7937/QXK2-QG03`

**Publication citation**:
`Simpson, A. L., Doussot, A., Creasy, J. M., Adams, L. B., Allen, P. J., DeMatteo, R. P., Gönen, M., Kemeny, N. E., Kingham, T. P., Shia, J., Jarnagin, W. R., Do, R. K. G., & D’Angelica, M. I. (2017). Computed Tomography Image Texture: A Noninvasive Prognostic Marker of Hepatic Recurrence After Hepatectomy for Metastatic Colorectal Cancer. In Annals of Surgical Oncology (Vol. 24, Issue 9, pp. 2482–2490). Springer Science and Business Media LLC. https://doi.org/10.1245/s10434-017-5896-1`

**TCIA citation**:
`Clark, K., Vendt, B., Smith, K., Freymann, J., Kirby, J., Koppel, P., Moore, S., Phillips, S., Maffitt, D., Pringle, M., Tarbox, L., & Prior, F. (2013). The Cancer Imaging Archive (TCIA): Maintaining and Operating a Public Information Repository. Journal of Digital Imaging, 26(6), 1045–1057. https://doi.org/10.1007/s10278-013-9622-7`
