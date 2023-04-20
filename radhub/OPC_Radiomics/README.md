## OPC-Radiomics dataset

## Requirements

- for download from TCIA, you may use CLI tool https://wiki.cancerimagingarchive.net/display/NBIA/NBIA+Data+Retriever+Command-Line+Interface+Guide or the GUI program.

## Steps

1. Download DICOM images and radiation therapy structures from https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=33948764 \\
   Save them in the folder `<your_base_dir>/raw/dicom`.

2. Using the same link, download the table with *Clinical data*. Save it as`<your_base_dir>/raw/tables/clinical_data.xlsx`.

3. Edit the base_path in [config.py](config.py)

5. Run the preprocessing and feature extraction:

```bash
   cd radiomics-features/radhub/OPC_Radiomics
   python .
```

## Notes

Currently we use only GTV masks, as in the original publication. There are, however, plenty of other segmented ROIs available: brain stem, spinal cord, eyes, optic nerves, optic chiasm, parotid glands, mandible, larynx, postcricoid region, esophagus, and others.

## Citation

**Data citation**:
`Kwan JYY, Su J, Huang SH, Ghoraie LS, Xu W, Chan B, Yip KW, Giuliani M, Bayley A, Kim J, Hope AJ, Ringash J, Cho J, McNiven A, Hansen A, Goldstein D, de Almeida JR, Aerts HJ, Waldron JN, Haibe-Kains B, O'Sullivan B, Bratman SV, Liu FF. (2019). Data from Radiomic Biomarkers to Refine Risk Models for Distant Metastasis in Oropharyngeal Carcinoma. The Cancer Imaging Archive. DOI:  10.7937/tcia.2019.8dho2gls`

**Publication citation**:
`Kwan JYY, Su J, Huang SH, Ghoraie LS, Xu W, Chan B, Yip KW, Giuliani M, Bayley A, Kim J, Hope AJ, Ringash J, Cho J, McNiven A, Hansen A, Goldstein D, de Almeida JR, Aerts HJ, Waldron JN, Haibe-Kains B, O'Sullivan B, Bratman SV, Liu FF.  (2018)  Radiomic Biomarkers to Refine Risk Models for Distant Metastasis in HPV-related Oropharyngeal Carcinoma . International Journal of Radiation Oncology*Biology*Physics, 1-10. DOI: https://doi.org/10.1016/j.ijrobp.2018.01.057`

**TCIA citation**:
`Clark, K., Vendt, B., Smith, K., Freymann, J., Kirby, J., Koppel, P., Moore, S., Phillips, S., Maffitt, D., Pringle, M., Tarbox, L., & Prior, F. (2013). The Cancer Imaging Archive (TCIA): Maintaining and Operating a Public Information Repository. Journal of Digital Imaging, 26(6), 1045–1057. https://doi.org/10.1007/s10278-013-9622-7`
