## Prostate-MRI-US-Biopsy dataset

## Requirements

- [dcm2niix](https://github.com/rordenlab/dcm2niix) (version 20-July-2022 or newer, don't use an old version from `apt`)

- [slicer](https://pypi.org/project/slicer/) (install with `pip install slicer`)
- for download from TCIA, you may use CLI tool https://wiki.cancerimagingarchive.net/display/NBIA/NBIA+Data+Retriever+Command-Line+Interface+Guide or the GUI program.

## Steps

1. Download DICOM images from https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=68550661 (takes a while...) \\
   Save them in a folder `<your_base_dir>/raw/dicom`.

2. Using the same link, download *STL Files (ZIP)*. Unzip and put all the .STL files in the folder `<your_base_dir>/raw/stl/`.

3. From the same link, download *Biopsy data* (Excel file). Save it as `<your_base_dir>/raw/tables/biopsy.xlsx`.

4. Edit the base_path in [config.py](config.py)

5. Convert segmentations from STL into nifti. For that, run a docker container with 3D Slicer Notebook environment from this directory. In there, run the notebook `work/stl_to_nifti.ipynb` (set the paths accordingly) with *Slicer* kernel.
```bash
docker run -p 8888:8888 -p 49053:49053 -v /mnt/hard/radiomics-features/Prostate-MRI-US-Biopsy/raw/stl:/stl -v /mnt/hard/radiomics-features/Prostate-MRI-US-Biopsy/derived/nifti:/nifti -v "$PWD":/home/sliceruser/work --rm -ti lassoan/slicer-notebook:latest

```
5. Convert DICOM images to nifti, run preprocessing and feature extraction:

```bash
   cd radiomics-features/radhub/
   python .
```



## Notes

## Citation

**Data citation**:
`Natarajan, S., Priester, A., Margolis, D., Huang, J., & Marks, L. (2020). Prostate MRI and Ultrasound With Pathology and Coordinates of Tracked Biopsy (Prostate-MRI-US-Biopsy) [Data set]. The Cancer Imaging Archive. DOI: https://doi.org/10.7937/TCIA.2020.A61IOC1A`

**Publication citation**:
`Sonn GA, Natarajan S, Margolis DJ, MacAiran M, Lieu P, Huang J, Dorey FJ, Marks LS. Targeted biopsy in the detection of prostate  cancer using an office based magnetic resonance ultrasound fusion device.  Journal of Urology 189, no. 1 (2013): 86-91. DOI: https://doi.org/10.1016/j.juro.2012.08.095`

**TCIA citation**:
`Clark, K., Vendt, B., Smith, K., Freymann, J., Kirby, J., Koppel, P., Moore, S., Phillips, S., Maffitt, D., Pringle, M., Tarbox, L., & Prior, F. (2013). The Cancer Imaging Archive (TCIA): Maintaining and Operating a Public Information Repository. Journal of Digital Imaging, 26(6), 1045–1057. https://doi.org/10.1007/s10278-013-9622-7`
