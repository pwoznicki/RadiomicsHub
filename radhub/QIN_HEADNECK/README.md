## QIN-HEADNECK dataset

## Requirements

- for download from TCIA, you may use CLI tool https://wiki.cancerimagingarchive.net/display/NBIA/NBIA+Data+Retriever+Command-Line+Interface+Guide or the GUI program.


## Steps

1. Download DICOM images from https://wiki.cancerimagingarchive.net/display/Public/QIN-HEADNECK (takes a while...) \\
   Save them in a folder `<your_base_dir>/raw/dicom`.

2. Using the same link, download _Clinical data_ . Save it as`<your_base_dir>/raw/tables/clinical_data.xlsx`.

3. Edit the base_path in [config.py](config.py)

4. Run the preprocessing and feature extraction:

```bash
   cd radiomics-features/radhub/QIN-HEADNECK
   python .
```

## Notes

Second PET/CT approx. 3 months after the first (but available in very few cases).
Dates were shifted by the same fixed offset across all the datasets to maintain temporal relationships of the datasets.

Only one case (0047) has two studies annotated. The rest have annotation for one study only.

reader is saved in ContentCreatorName
imaging time point is saved in ClinicalTrialTimePointID
segmentation session in ClinicalTrialSeriesID
algorithm for segmentation (manual/semi-/automatic) in SegmentAlgorithmType
SegmentedPropertyType = (M-80003, SRT, "Neoplasm, Primary")
AnatomicRegion = (T-53131, SRT, "base of tongue")


## Citation

**Data citation**:
`Beichel R R, Ulrich E J, Bauer C, Wahle A, Brown B, Chang T, Plichta K A, Smith B J, Sunderland J J, Braun T, Fedorov A, Clunie D, Onken M, Magnotta VA, Menda Y, Riesmeier J, Pieper S, Kikinis R, Graham M M, Casavant T L, Sonka M, Buatti J M. (2015). Data From QIN-HEADNECK. The Cancer Imaging Archive. DOI:  10.7937/K9/TCIA.2015.K0F5CGLI`

**Publication citation**:
`Fedorov A, Clunie D, Ulrich E, Bauer C, Wahle A, Brown B, Onken M, Riesmeier J, Pieper S, Kikinis R, Buatti J, Beichel RR. (2016) DICOM for quantitative imaging biomarker development: a standards based approach to sharing clinical data and structured PET/CT analysis results in head and neck cancer research. PeerJ 4:e2057  DOI: https://doi.org/10.7717/peerj.2057`

**TCIA citation**:
`Clark, K., Vendt, B., Smith, K., Freymann, J., Kirby, J., Koppel, P., Moore, S., Phillips, S., Maffitt, D., Pringle, M., Tarbox, L., & Prior, F. (2013). The Cancer Imaging Archive (TCIA): Maintaining and Operating a Public Information Repository. Journal of Digital Imaging, 26(6), 1045–1057. https://doi.org/10.1007/s10278-013-9622-7`
