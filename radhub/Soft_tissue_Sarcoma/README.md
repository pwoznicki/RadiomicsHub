## Soft-tissue-Sarcoma dataset

## Requirements

- for download from TCIA, you may use CLI tool https://wiki.cancerimagingarchive.net/display/NBIA/NBIA+Data+Retriever+Command-Line+Interface+Guide or the GUI program.

## Steps

1. Download DICOM images and Radiation Therapy Structures from [TCIA](https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=21266533) \\
   Save them in a folder `<your_base_dir>/raw/dicom`.

2. Using the same link, download [Clinical Data Table](https://wiki.cancerimagingarchive.net/download/attachments/21266533/INFOclinical_STS.xlsx?version=1&modificationDate=1452628070860&api=v2). Save it as `<your_base_dir>/raw/tables/INFOclinical_STS.xlsx`.

3. Edit the base_path in [config.py](config.py)

4. Run the preprocessing and feature extraction:

```bash
   cd RadiomicsHub/radhub/Soft_tissue_Sarcoma
   python .
```

## Notes

## Citation

**Data citation**:

`Vallières, Martin, Freeman, Carolyn R., Skamene, Sonia R., & El Naqa, Issam. (2015). A radiomics model from joint FDG-PET and MRI texture features for the prediction of lung metastases in soft-tissue sarcomas of the extremities (Soft-tissue-Sarcoma) [Dataset]. The Cancer Imaging Archive. http://doi.org/10.7937/K9/TCIA.2015.7GO2GSKS`

**Publication citation**:

`Vallières, M., Freeman, C. R., Skamene, S. R., & Naqa, I. El. (2015, June 29). A radiomics model from joint FDG-PET and MRI texture features for the prediction of lung metastases in soft-tissue sarcomas of the extremities. Physics in Medicine and Biology. IOP Publishing. http://doi.org/10.1088/0031-9155/60/14/5471`

**TCIA citation**:
`Clark, K., Vendt, B., Smith, K., Freymann, J., Kirby, J., Koppel, P., Moore, S., Phillips, S., Maffitt, D., Pringle, M., Tarbox, L., & Prior, F. (2013). The Cancer Imaging Archive (TCIA): Maintaining and Operating a Public Information Repository. Journal of Digital Imaging, 26(6), 1045–1057. https://doi.org/10.1007/s10278-013-9622-7`
