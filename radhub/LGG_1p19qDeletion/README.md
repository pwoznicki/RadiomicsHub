## LGG-1p19qDeletion dataset

## Requirements

- for download from TCIA, you may use CLI tool https://wiki.cancerimagingarchive.net/display/NBIA/NBIA+Data+Retriever+Command-Line+Interface+Guide or the GUI program.

## Steps

1. Download DICOM images and segmentations from https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=1966254 (takes a while...) \\
   Save them in a folder `<your_base_dir>/raw/dicom/img`.

2. In the same link, scroll down and download 1p19q Status and Histologic Type (XLS). Save it as`<your_base_dir>/raw/tables/TCIA_LGG_cases_159.xlsx`.

3. Edit the base_path in [config.py](config.py)

4. Run the preprocessing and feature extraction:

```bash
   cd radiomics-features/radhub/LGG-1p19qDeletion
   python .
```

## Notes

Every case has T2-weighted and post-contrast T1-weighted, registered to T2w, and a tumor segmentation.

## Citation

**Data citation**:
`Erickson, Bradley; Akkus, Zeynettin; Sedlar, Jiri; Korfiatis, Panagiotis. (2017). Data From LGG-1p19qDeletion. The Cancer Imaging Archive. DOI: https://doi.org/10.7937/K9/TCIA.2017.dwehtz9v`

**Publication citation**:
`Zeynettin Akkus, Issa Ali, Jiří Sedlář, Jay P. Agrawal, Ian F. Parney, Caterina Giannini, and Bradley J. Erickson.Predicting Deletion of Chromosomal Arms 1p/19q in Low-Grade Gliomas from MR Images Using Machine Intelligence. J Digit Imaging. 2017 Aug; 30(4): 469–476. Published online 2017 Jun 9.  DOI:  https://doi.org/10.1007/s10278-017-9984-3. PMCID: PMC5537096`

**TCIA citation**:
`Clark, K., Vendt, B., Smith, K., Freymann, J., Kirby, J., Koppel, P., Moore, S., Phillips, S., Maffitt, D., Pringle, M., Tarbox, L., & Prior, F. (2013). The Cancer Imaging Archive (TCIA): Maintaining and Operating a Public Information Repository. Journal of Digital Imaging, 26(6), 1045–1057. https://doi.org/10.1007/s10278-013-9622-7`
