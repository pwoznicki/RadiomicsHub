## LIDC-IDRI dataset

## Requirements

- [dcm2niix](https://github.com/rordenlab/dcm2niix) (version 20-July-2022 or newer, don't use an old version from `apt`)

- for download from TCIA, you may use CLI tool https://wiki.cancerimagingarchive.net/display/NBIA/NBIA+Data+Retriever+Command-Line+Interface+Guide or the GUI program.

## Steps

1. Download DICOM images from https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=1966254 (takes a while...) \\
   Save them in a folder `<your_base_dir>/raw/dicom/img`.

2. In the same link, go to _Detailed Description_, scroll down to _Diagnosis Data_ and download [tcia-diagnosis-data-2012-04-20.xls](https://wiki.cancerimagingarchive.net/download/attachments/3539039/tcia-diagnosis-data-2012-04-20.xls?version=1&modificationDate=1334930231098&api=v2). Save it in the folder `<your_base_dir>/raw/tables/`.

3. Download segmentations (DICOM SEG) from https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=44499647
   Save them in `<your_base_dir>/raw/dicom/seg`.

4. Edit the base_path in [config.py](config.py)

5. Run the preprocessing and feature extraction:

```bash
   cd radiomics-features/radfeat/
   python .
```

## Notes

## Citation

**Data citation**:

**Publication citation**:

**TCIA citation**:
`Clark, K., Vendt, B., Smith, K., Freymann, J., Kirby, J., Koppel, P., Moore, S., Phillips, S., Maffitt, D., Pringle, M., Tarbox, L., & Prior, F. (2013). The Cancer Imaging Archive (TCIA): Maintaining and Operating a Public Information Repository. Journal of Digital Imaging, 26(6), 1045–1057. https://doi.org/10.1007/s10278-013-9622-7`
