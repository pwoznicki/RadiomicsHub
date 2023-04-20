## HNSCC dataset

## Requirements

- for download from TCIA, you may use CLI tool https://wiki.cancerimagingarchive.net/display/NBIA/NBIA+Data+Retriever+Command-Line+Interface+Guide or the GUI program.

## Steps

1. Download DICOM images and segmentations(RT structures) from https://wiki.cancerimagingarchive.net/display/Public/HNSCC#415180001cbf1fde71ae4a448039d61437d1076b (takes a while...) \\
   Save them in a folder `<your_base_dir>/raw/dicom`.

2. In the same link, download the 3 tables with clinical data. Save them as:
- `<your_base_dir>/raw/tables/Patient and Treatment Characteristics.xls`
- `<your_base_dir>/raw/tables/Field Descriptions for Patient and Treatment Characteristics.xlsx`
- `<your_base_dir>/raw/tables/Radiomics_Outcome_Prediction_in_OPC_ASRM_corrected.csv`

3. Edit the base_path in [config.py](config.py)

4. Run the preprocessing and feature extraction:

```bash
   cd radiomics-features/radhub/HNSCC
   python .
```

## Notes
CT and PET images are available. For each case, there is 1 CT image with corresponding RT segmentations. There are multiple PET images. We only used CT in the analysis.
All the segmentations starting with GTV were used here. That means, there may be multiple GTV segmentations for each case, which can be filtered if needed using *ROI* column.

There are two tables with clinical data and labels for subsets of data: one with 492 cases ("HN_Cancer_Atlas") and the other with 215 cases ("OPC").

## Citation

**Data citation**:
`Grossberg A, Elhalawani H, Mohamed A, Mulder S, Williams B, White AL, Zafereo J, Wong AJ, Berends JE, AboHashem S, Aymard JM, Kanwar A, Perni S, Rock CD, Chamchod S, Kantor M, Browne T, Hutcheson K, Gunn GB, Frank SJ, Rosenthal DI, Garden AS, Fuller CD, M.D. Anderson Cancer Center Head and Neck Quantitative Imaging Working Group. (2020) HNSCC [ Dataset ]. The Cancer Imaging Archive. DOI: https://doi.org/10.7937/k9/tcia.2020.a8sh-7363`
**Publication citations**:
`Grossberg  A, Mohamed A, Elhalawani H, Bennett W, Smith K, Nolan T,  Williams B, Chamchod S, Heukelom J, Kantor M, Browne T, Hutcheson K, Gunn G, Garden A, Morrison W, Frank S, Rosenthal D, Freymann J, Fuller C. (2018) Imaging and Clinical Data Archive for Head and Neck Squamous Cell Carcinoma Patients Treated with Radiotherapy. Scientific Data 5:180173 (2018) DOI: https://doi.org/10.1038/sdata.2018.173`

`Elhalawani, H., Mohamed, A., White, A. et al. Matched computed tomography segmentation and demographic data for oropharyngeal cancer radiomics challenges. Sci Data 4, 170077 (2017). DOI: https://doi.org/10.1038/sdata.2017.77`

**TCIA citation**:
`Clark, K., Vendt, B., Smith, K., Freymann, J., Kirby, J., Koppel, P., Moore, S., Phillips, S., Maffitt, D., Pringle, M., Tarbox, L., & Prior, F. (2013). The Cancer Imaging Archive (TCIA): Maintaining and Operating a Public Information Repository. Journal of Digital Imaging, 26(6), 1045–1057. https://doi.org/10.1007/s10278-013-9622-7`
