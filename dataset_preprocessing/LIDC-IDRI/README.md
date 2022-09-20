### LIDC-IDRI dataset

#### Requirements

- [dcm2niix](https://github.com/rordenlab/dcm2niix) (version 20-July-2022)

1. Download DICOM images from https://wiki.cancerimagingarchive.net/display/Public/LIDC-IDRI#1966254194132fe653e4a7db00715f6f775c012 (takes a while...) \\
   Save them in a folder called `dicom`.

2. Download segmentations (DICOM SEG) from https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=44499647
   Save them in a folder called `dicom_seg`.

3. Convert DICOM images to NIfTI using dcm2niix:

```bash
   mkdir nifti_img
   cd dicom
   ls -1 | xargs -L 1 dcm2niix -z y -f %i -o ../nifti_img -i y
```

4. Convert DICOM segmentations to NIfTI:

```bash
   mkdir nifti_seg
   cd dicom_seg
   ls -1 | xargs -L 1 dcm2niix -z y -f %i_%d -o ../nifti_seg
```

5. Create a table with paths: