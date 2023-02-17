### LIDC-IDRI dataset

## Requirements

- [dcm2niix](https://github.com/rordenlab/dcm2niix) (version 20-July-2022, don't use an old version from `apt`)

- [segimage2itkimage](https://qiicr.gitbook.io/dcmqi-guide/opening/cmd_tools/seg/segimage2itkimage)

- for download from TCIA, you may use CLI tool https://wiki.cancerimagingarchive.net/display/NBIA/NBIA+Data+Retriever+Command-Line+Interface+Guide or the GUI program.

## Steps

1. Download images (DICOM) and segmentations (Gross Tumor Volume Segmentation, DICOM SEG) from [TCIA](https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=46334165) \\
   Move downloaded images to folder `<root_dir>/raw/dicom/img` and segmentations to folder `<root_dir>/raw/dicom/seg`.

3. Run processing:

```bash
   cd radhub/RIDER_LungCT
   python .
```

## Notes

It seems there are some discrepancies between RTStruct and DICOM SEG labels (man vs. automatic labels), e.g. look at RIDER-1129164940 TEST. In here we assume label 1 from DICOM SEG is for human annotator and label 2 is for automatic annotator.

## Citation

**Data citation**:
`Wee, L., Aerts, H., Kalendralis, P., & Dekker, A. (2020). RIDER Lung CT Segmentation Labels from: Decoding tumour phenotype by noninvasive imaging using a quantitative radiomics approach [Data set]. The Cancer Imaging Archive. https://doi.org/10.7937/tcia.2020.jit9grk8`

**Publication citation**:
`Aerts, H. J. W. L., Velazquez, E. R., Leijenaar, R. T. H., Parmar, C., Grossmann, P., Carvalho, S., Bussink, J., Monshouwer, R., Haibe-Kains, B., Rietveld, D., Hoebers, F., Rietbergen, M. M., Leemans, C. R., Dekker, A., Quackenbush, J., Gillies, R. J., & Lambin, P. (2014). Decoding tumour phenotype by noninvasive imaging using a quantitative radiomics approach. Nature Communications, 5(1). https://doi.org/10.1038/ncomms5006`

**TCIA citation**:
`Clark, K., Vendt, B., Smith, K., Freymann, J., Kirby, J., Koppel, P., Moore, S., Phillips, S., Maffitt, D., Pringle, M., Tarbox, L., & Prior, F. (2013). The Cancer Imaging Archive (TCIA): Maintaining and Operating a Public Information Repository. Journal of Digital Imaging, 26(6), 1045–1057. https://doi.org/10.1007/s10278-013-9622-7`
