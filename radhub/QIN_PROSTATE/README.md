## Repeatability of radiomics features in prostate mpMRI (QIN-PROSTATE)

1. Download images and segmentations from [TCIA](https://wiki.cancerimagingarchive.net/display/Public/QIN+PROSTATE#18022465db2186bfb9d24789803d784c7a3c1041).

2. Rename the downloaded `QIN-PROSTATE-Repeatability` folder to `<your_base_dir>/raw/dicom`.
   Set the `base_dir` variable in [config.py](radhub/QIN_PROSTATE/config.py).

3. Run the processing script

```bash
cd radiomics-features/radhub/QIN_PROSTATE
python .
```

## Notes

For PCAMPMRI-00004 study 09-12-1994, the tumor segmentation is too small for the extraction with pyradiomics, for ADC and T2. Therefore features were not extracted for this ROI and sequences.

## Citation

The dataset was downloaded from [TCIA](https://wiki.cancerimagingarchive.net/display/Public/QIN-PROSTATE-Repeatability)

If you use it for your research, cite the original dataset and publication, and TCIA:

**Data Citation**
`Fedorov, A; Schwier, M; Clunie, D; Herz, C; Pieper, S; Kikinis, R; Tempany, C; Fennessy, F. (2018). Data From QIN-PROSTATE-Repeatability. The Cancer Imaging Archive. DOI: https://doi.org/10.7937/K9/TCIA.2018.MR1CKGND`

**Publication Citation**
`Fedorov A, Vangel MG, Tempany CM, Fennessy FM. Multiparametric Magnetic Resonance Imaging of the Prostate: Repeatability of Volume and Apparent Diffusion Coefficient Quantification. Investigative Radiology. 52, 538–546 (2017). DOI: https://doi.org/10.1097/RLI.0000000000000382`

**Publication Citation**
`Fedorov, A., Schwier, M., Clunie, D., Herz, C., Pieper, S., Kikinis,R., Tempany, C. & Fennessy, F. An annotated test-retest collection of prostate multiparametric MRI. Scientific Data 5, 180281 (2018). DOI: https://doi.org/10.1038/sdata.2018.281`

**TCIA Citation**
`Clark K, Vendt B, Smith K, Freymann J, Kirby J, Koppel P, Moore S, Phillips S, Maffitt D, Pringle M, Tarbox L, Prior F. The Cancer Imaging Archive (TCIA): Maintaining and Operating a Public Information Repository, Journal of Digital Imaging, Volume 26, Number 6, December, 2013, pp 1045-1057. DOI: 10.1007/s10278-013-9622-7`

```

```
