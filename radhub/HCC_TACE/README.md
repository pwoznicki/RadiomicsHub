## HCC-TACE-Seg dataset

## Requirements

- for download from TCIA, you may use the [CLI tool](https://wiki.cancerimagingarchive.net/display/NBIA/NBIA+Data+Retriever+Command-Line+Interface+Guide) or the GUI program.

## Steps

1. Download DICOM images and segmentations from [TCIA](https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=70230229) \\
   Save the patient directories in the folder `<your_base_dir>/raw/dicom`.

2. In the same link, download "Clinical data with description (XLSX)". Save it as `<your_base_dir>/raw/tables/HCC-TACE-Seg_clinical_data-V2.xlsx`.

4. Edit the base_path in [config.py](config.py)

5. Run the preprocessing and feature extraction:

```bash
   cd radiomics-features/radhub/
   python .
```

## Notes

For each segmented case, 4 masks available: 
- Liver (without the tumor and the portal vein)
- Abdominal aorta (part) 
- Portal vein with branches
- Liver tumor (Mass)

The images which have the segmentations, are saved as multiphase series. 
That's why the conversion included separation of each phase (using AcquisitionNumber) and then conversion to NIfTI. \\
The phases are saved in the following order:
- 1: late arterial phase
- 2: portal venous (pv) phase
- 3: delayed phase

85/104 cases have pv phase in the series where segmentation was done.
23/104 cases have late arterial phase, and 23/104 have delayed phase.
For consistency, we only extract features from pv phase.

## Citation

**Data citation**:
`Moawad, A. W., Fuentes, D., Morshid, A., Khalaf, A. M., Elmohr, M. M., Abusaif, A., Hazle, J. D., Kaseb, A. O., Hassan, M., Mahvash, A., Szklaruk, J., Qayyom, A., & Elsayes, K. (2021). Multimodality annotated HCC cases with and without advanced imaging segmentation [Data set]. The Cancer Imaging Archive. https://doi.org/10.7937/TCIA.5FNA-0924`

**Publication citation**:
`Morshid, A., Elsayes, K. M., Khalaf, A. M., Elmohr, M. M., Yu, J., Kaseb, A. O., Hassan, M., Mahvash, A., Wang, Z., Hazle, J. D., & Fuentes, D. (2019). A Machine Learning Model to Predict Hepatocellular Carcinoma Response to Transcatheter Arterial Chemoembolization. Radiology: Artificial Intelligence, 1(5), e180021. https://doi.org/10.1148/ryai.2019180021`

**TCIA citation**:
`Clark, K., Vendt, B., Smith, K., Freymann, J., Kirby, J., Koppel, P., Moore, S., Phillips, S., Maffitt, D., Pringle, M., Tarbox, L., & Prior, F. (2013). The Cancer Imaging Archive (TCIA): Maintaining and Operating a Public Information Repository. Journal of Digital Imaging, 26(6), 1045–1057. https://doi.org/10.1007/s10278-013-9622-7`
