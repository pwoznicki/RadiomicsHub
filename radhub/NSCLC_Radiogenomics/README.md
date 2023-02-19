## NSCLC-Radiogenomics

## Requirements

- [dcm2niix](https://github.com/rordenlab/dcm2niix) (version 20-July-2022 or newer, don't use an old version from `apt`)
- for download from TCIA, you may use CLI tool https://wiki.cancerimagingarchive.net/display/NBIA/NBIA+Data+Retriever+Command-Line+Interface+Guide or the GUI program.

## Steps

1. Download DICOM images and segmentations from [TCIA](https://wiki.cancerimagingarchive.net/display/Public/NSCLC+Radiogenomics#286723474bf3bc54d8c14b93ba3b3b874b5b1a0b) (takes a while...) \\
   Save the patient folders in: `<your_base_dir>/raw/dicom`.

2. In the same link, download [Clinical Data](https://wiki.cancerimagingarchive.net/download/attachments/28672347/NSCLCR01Radiogenomic_DATA_LABELS_2018-05-22_1500-shifted.csv?version=1&modificationDate=1531967714295&api=v2). Save it as `<your_base_dir>/raw/tables/clinical_data.csv`.

3. Edit the base_path in [config.py](config.py)

4. Run the preprocessing and feature extraction:

```bash
   cd radiomics-features/radhub/
   python .
```

## Notes

For cases AMC001 - AMC049, no segmentations are present (ref. table 2 from https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6190740/).
Similarly, cases R01-147 - R01-163 have no segmentations.
For cases R01-001 - R01-146, all but two (R01-009 and R01-143) have segmentations for the CT study.
Cases with segmentations are included in the analysis.

The PET/CT studies are not used here (no segmentations).

## Citation

**Data citation**:
`Bakr, Shaimaa; Gevaert, Olivier; Echegaray, Sebastian; Ayers, Kelsey; Zhou, Mu; Shafiq, Majid; Zheng, Hong; Zhang, Weiruo; Leung, Ann; Kadoch, Michael; Shrager, Joseph; Quon, Andrew; Rubin, Daniel; Plevritis, Sylvia; Napel, Sandy.(2017). Data for NSCLC Radiogenomics Collection. The Cancer Imaging Archive. http://doi.org/10.7937/K9/TCIA.2017.7hs46erv`

**Publication citations**:
`Bakr, S., Gevaert, O., Echegaray, S., Ayers, K., Zhou, M., Shafiq, M., Zheng, H., Benson, J. A., Zhang, W., Leung, A., Kadoch, M., Hoang, C. D., Shrager, J., Quon, A., Rubin, D. L., Plevritis, S. K., & Napel, S. (2018). A radiogenomic dataset of non-small cell lung cancer. Scientific data, 5, 180202. https://doi.org/10.1038/sdata.2018.202`

`Gevaert, O., Xu, J., Hoang, C. D., Leung, A. N., Xu, Y., Quon, A., … Plevritis, S. K. (2012, August). Non–Small Cell Lung Cancer: Identifying Prognostic Imaging Biomarkers by Leveraging Public Gene Expression Microarray Data—Methods and Preliminary Results. Radiology. Radiological Society of North America (RSNA). http://doi.org/10.1148/radiol.12111607`


**TCIA citation**:
`Clark, K., Vendt, B., Smith, K., Freymann, J., Kirby, J., Koppel, P., Moore, S., Phillips, S., Maffitt, D., Pringle, M., Tarbox, L., & Prior, F. (2013). The Cancer Imaging Archive (TCIA): Maintaining and Operating a Public Information Repository. Journal of Digital Imaging, 26(6), 1045–1057. https://doi.org/10.1007/s10278-013-9622-7`
