## Head-Neck-Radiomics-HN1 dataset

## Requirements

- for download from TCIA, you may use CLI tool https://wiki.cancerimagingarchive.net/display/NBIA/NBIA+Data+Retriever+Command-Line+Interface+Guide or the GUI program.

## Steps

1. Download DICOM images and segmentations from https://wiki.cancerimagingarchive.net/display/Public/Head-Neck-Radiomics-HN1 (takes a while...) \\
   Save them in a folder `<your_base_dir>/raw/dicom`.

2. In the same link, download *Clinical Data*. Unpack the ZIP and save the CSV as `<your_base_dir>/raw/tables/clinical_data.csv`.

4. Edit the `base_path` in [config.py](config.py)

5. Run the preprocessing and feature extraction:

```bash
   cd radiomics-features/radhub/Head_Neck_Radiomics_HN1
   python .
```

## Notes
Only CT images are used here, PET images are not available for all subjects.

## Citation

**Data citation**:
`Wee, L., & Dekker, A. (2019). Data from HEAD-NECK-RADIOMICS-HN1 [Data set]. The Cancer Imaging Archive. https://doi.org/10.7937/tcia.2019.8kap372n`

**Publication citation**:
`Aerts HJWL, Velazquez ER, Leijenaar RTH, Parmar C, Grossmann P, Carvalho S, Bussink J, Monshouwer R, Haibe-Kains B, Rietveld D, Hoebers F, Rietbergen MM, Leemans CR, Dekker A, Quackenbush J, Gillies RJ, Lambin P. Decoding Tumour Phenotype by Noninvasive Imaging Using a Quantitative Radiomics Approach, Nature Communications, Volume 5, Article Number 4006, June 03, 2014. DOI: http://doi.org/10.1038/ncomms5006`

**TCIA citation**:
`Clark, K., Vendt, B., Smith, K., Freymann, J., Kirby, J., Koppel, P., Moore, S., Phillips, S., Maffitt, D., Pringle, M., Tarbox, L., & Prior, F. (2013). The Cancer Imaging Archive (TCIA): Maintaining and Operating a Public Information Repository. Journal of Digital Imaging, 26(6), 1045–1057. https://doi.org/10.1007/s10278-013-9622-7`
