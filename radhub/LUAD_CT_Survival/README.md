## LIDC-IDRI dataset

## Requirements

- [dcm2niix](https://github.com/rordenlab/dcm2niix) (version 20-July-2022 or newer, don't use an old version from `apt`)

- for download from TCIA, you may use CLI tool https://wiki.cancerimagingarchive.net/display/NBIA/NBIA+Data+Retriever+Command-Line+Interface+Guide or the GUI program.

## Steps

1. Download images (as DICOMs) and tumor segmentations (as NIfTIs) from [TCIA](https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=24284406#24284406036220c66a5a436f90e4a0b54367bfae) \\
   Save the images in the folder `<your_base_dir>/raw/img`
   Save the segmentations in the folder `<your_base_dir>/raw/seg`

2. Using the same link, download the table [Image Features and Patient Survival (CSV)](https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=24284406#24284406036220c66a5a436f90e4a0b54367bfae). Save it as `<your_base_dir>/raw/tables/FeaturesWithLabels.csv`.

3. Edit the base_path in [config.py](config.py)

4. Run the preprocessing and feature extraction:

```bash
   cd radiomics-features/radhub/LUAD_CT_Survival
   python .
```

## Notes

## Citation

**Data citation**:
`Goldgof D., Hall L., Hawkins S.H., Schabath M.B., Stringfield O., Garcia A., Balagurunathan Y., Kim J., Eschrich S., Berglund A.E., Gatenby R., Gillies R.J. (2017) Long and Short Survival in Adenocarcinoma Lung CTs. The Cancer Imaging Archive. https://doi.org/10.7937/K9/TCIA.2017.0tv7b9x1`

**Publication citations**:

1. `Paul, R., Hawkins, S., Balagurunathan, Y., Schabath, M., Gillies, R., Hall, L., & Goldgof, D. (2016). Deep Feature Transfer Learning in Combination with Traditional Features Predicts Survival among Patients with Lung Adenocarcinoma. Tomography, 2(4), 388–395. https://doi.org/10.18383/j.tom.2016.00211`
2. `Hawkins, S. H., Korecki, J. N., Balagurunathan, Y., Yuhua Gu, Kumar, V., Basu, S., Hall, L. O., Goldgof, D. B., Gatenby, R. A., & Gillies, R. J. (2014). Predicting Outcomes of Nonsmall Cell Lung Cancer Using CT Image Features. IEEE Access, 2, 1418–1426. https://doi.org/10.1109/access.2014.2373335`

**TCIA citation**:
`Clark, K., Vendt, B., Smith, K., Freymann, J., Kirby, J., Koppel, P., Moore, S., Phillips, S., Maffitt, D., Pringle, M., Tarbox, L., & Prior, F. (2013). The Cancer Imaging Archive (TCIA): Maintaining and Operating a Public Information Repository. Journal of Digital Imaging, 26(6), 1045–1057. https://doi.org/10.1007/s10278-013-9622-7`
