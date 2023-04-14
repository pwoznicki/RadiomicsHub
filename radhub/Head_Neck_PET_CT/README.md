## Head-Neck-PET-CT dataset

## Requirements

- for download from TCIA, you may use CLI tool https://wiki.cancerimagingarchive.net/display/NBIA/NBIA+Data+Retriever+Command-Line+Interface+Guide or the GUI program.

## Steps

1. Download DICOM images and segmentations (Radiation Therapy Structures) from https://wiki.cancerimagingarchive.net/display/Public/Head-Neck-PET-CT (takes a while...) \\
   Save them in a folder `<your_base_dir>/raw/dicom/img`.

2. In the same link, download *Clinical Data (XLS)*. Save it as`<your_base_dir>/raw/tables/INFOclinical_HN_Version2_30may2018.xlsx`.

3. Download *Names of GTV contours (XLS)*. Save it as `<your_base_dir>/raw/tables/INFO_GTVcontours_HN.xlsx`.

4. Edit the base_path in [config.py](config.py)

5. Run the preprocessing and feature extraction:

```bash
   cd radiomics-features/radhub/Head_Neck_PET_CT
   python .
```

## Notes

We used only the mask for GTV here. There are many more masks available, including for GTV lymph nodes (available only for some) and many head and neck organs.

For 3 patients, two GTV ROIs are available. We only used the first one.

## Citation

**Data citation**:
`Martin Vallières, Emily Kay-Rivest, Léo Jean Perrin, Xavier Liem, Christophe Furstoss, Nader Khaouam, Phuc Félix Nguyen-Tan, Chang-Shu Wang, Khalil Sultanem. (2017). Data from Head-Neck-PET-CT. The Cancer Imaging Archive. doi: 10.7937/K9/TCIA.2017.8oje5q00`

**Publication citation**:
`Vallières, M., Kay-Rivest, E., Perrin, L. J., Liem, X., Furstoss, C., Aerts, H. J. W. L., Khaouam, N., Nguyen-Tan, P. F., Wang, C.-S., Sultanem, K., Seuntjens, J., & El Naqa, I. (2017). Radiomics strategies for risk assessment of tumour failure in head-and-neck cancer. In Scientific Reports (Vol. 7, Issue 1).  DOI: https://doi.org/10.1038/s41598-017-10371-5`

**TCIA citation**:
`Clark, K., Vendt, B., Smith, K., Freymann, J., Kirby, J., Koppel, P., Moore, S., Phillips, S., Maffitt, D., Pringle, M., Tarbox, L., & Prior, F. (2013). The Cancer Imaging Archive (TCIA): Maintaining and Operating a Public Information Repository. Journal of Digital Imaging, 26(6), 1045–1057. https://doi.org/10.1007/s10278-013-9622-7`
