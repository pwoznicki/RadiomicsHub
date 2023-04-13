## KiTS 2019 dataset

## Requirements

- for download from TCIA, you may use CLI tool https://wiki.cancerimagingarchive.net/display/NBIA/NBIA+Data+Retriever+Command-Line+Interface+Guide or the GUI program.

## Steps

1. Download _Images and Segmentations_ (DICOM) from [TCIA C4KC-KiTs](https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=61081171) \\
   Put the dicom directories in the folder:`<your_base_dir>/raw/dicom`.

2. In the same link, download [Clinical Data](https://wiki.cancerimagingarchive.net/download/attachments/61081171/C4KC%20KiTS_Clinical%20Data_Version%201.csv?api=v2). Save it as `<your_base_dir>/raw/tables/clinical_data.csv`.

4. Edit the base_path in [config.py](config.py)

5. Run the preprocessing and feature extraction:

```bash
   cd radiomics-features/radhub/C4KC_KiTS
   python .
```

## Notes

## Citation

**Data citation**:
`Heller, N., Sathianathen, N., Kalapara, A., Walczak, E., Moore, K., Kaluzniak, H., Rosenberg, J., Blake, P., Rengel, Z., Oestreich, M., Dean, J., Tradewell, M., Shah, A., Tejpaul, R., Edgerton, Z., Peterson, M., Raza, S., Regmi, S., Papanikolopoulos, N., Weight, C.  (2019) Data from C4KC-KiTS  [Data set]. The Cancer Imaging Archive. DOI: 10.7937/TCIA.2019.IX49E8NX`

**Publication citation**:
`Heller, N., Isensee, F., Maier-Hein, K. H., Hou, X., Xie, C., Li, F., Nan, Y., Mu, G., Lin, Z., Han, M., Yao, G., Gao, Y., Zhang, Y., Wang, Y., Hou, F., Yang, J., Xiong, G., Tian, J., Zhong, C., … Weight, C. (2021). The state of the art in kidney and kidney tumor segmentation in contrast-enhanced CT imaging: Results of the KiTS19 challenge. Medical Image Analysis, 67, 101821. https://doi.org/10.1016/j.media.2020.101821`

**TCIA citation**:
`Clark, K., Vendt, B., Smith, K., Freymann, J., Kirby, J., Koppel, P., Moore, S., Phillips, S., Maffitt, D., Pringle, M., Tarbox, L., & Prior, F. (2013). The Cancer Imaging Archive (TCIA): Maintaining and Operating a Public Information Repository. Journal of Digital Imaging, 26(6), 1045–1057. https://doi.org/10.1007/s10278-013-9622-7`
