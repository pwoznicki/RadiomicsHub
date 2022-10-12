### LIDC-IDRI dataset

#### Requirements

- [dcm2niix](https://github.com/rordenlab/dcm2niix) (version 20-July-2022, don't use an old version from `apt`)

- for download from TCIA, you may use CLI tool https://wiki.cancerimagingarchive.net/display/NBIA/NBIA+Data+Retriever+Command-Line+Interface+Guide or the GUI program.

1. Download images (DICOM) and segmentations (DICOM SEG) from https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=46334165 \\
   Move downloaded images to folder `<root_dir>/dicom_img` and segmentations to folder `<root_dir>/dicom_seg`.

3. Convert DICOM images to NIfTI using dcm2niix:

```bash
   mkdir nifti_img
   cd dicom_img
   ls -1 | xargs -L 1 dcm2niix -z y -f %i_%s -o ../nifti_img
```

4. Convert DICOM segmentations to NIfTI:

```bash
   mkdir nifti_seg
   cd dicom_seg
   ls -1 | xargs -L 1 dcm2niix -z y -f %d -o ../nifti_seg
```

5. Create a table with paths:

   ```bash
      python preprocess.py
   ```

6. Extract features:

   ```bash
      python extract_features.py
   ```
