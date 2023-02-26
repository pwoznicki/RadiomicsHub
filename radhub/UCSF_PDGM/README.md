## LIDC-IDRI dataset

## Requirements

## Steps

1. Download the images and segmentations in Nifti format from [TCIA](https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=119705830#1197058307e324bc732ef415a86e5ac4b072a65f2) \\
   Save them in a folder `<your_base_dir>/raw/nifti`.

2. Using the same link, download [Clinical data (CSV)](https://wiki.cancerimagingarchive.net/download/attachments/119705830/UCSF-PDGM-metadata_v2.csv?api=v2). Save it as`<your_base_dir>/raw/tables/UCSF-PDGM-metadata_v2.csv`.

3. Edit the base_path in [config.py](config.py)

4. Run the preprocessing and feature extraction:

```bash
   cd radiomics-features/radhub/UCSF_PDGM
   python .
```

## Notes

The dataset has additional masks for brain and brain parenchyma that were not used here.

## Citation

**Data citation**
`Calabrese, E., Villanueva-Meyer, J., Rudie, J., Rauschecker, A., Baid, U., Bakas, S., Cha, S., Mongan, J., & Hess, C. (2022). The University of California San Francisco Preoperative Diffuse Glioma MRI (UCSF-PDGM) (Version 3) [Dataset].  The Cancer Imaging Archive.  DOI: 10.7937/tcia.bdgf-8v37`

**Publication citation**:
`Evan Calabrese, Javier E. Villanueva-Meyer, Jeffrey D. Rudie, Andreas M. Rauschecker, Ujjwal Baid, Spyridon Bakas, Soonmee Cha, John T. Mongan, Christopher P. Hess. The UCSF Preoperative Diffuse Glioma MRI (UCSF-PDGM) Dataset. Radiology: Artificial Intelligence. DOI: https://doi.org/10.1148/ryai.220058`

**TCIA citation**:
`Clark, K., Vendt, B., Smith, K., Freymann, J., Kirby, J., Koppel, P., Moore, S., Phillips, S., Maffitt, D., Pringle, M., Tarbox, L., & Prior, F. (2013). The Cancer Imaging Archive (TCIA): Maintaining and Operating a Public Information Repository. Journal of Digital Imaging, 26(6), 1045–1057. https://doi.org/10.1007/s10278-013-9622-7`
