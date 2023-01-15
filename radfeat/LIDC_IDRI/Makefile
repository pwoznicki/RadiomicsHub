.ONESHELL
venv:
	virtualenv .venv -p python3.8
	source .venv/bin/activate
	pip install -r requirements.txt

.ONESHELL
dcm2nii:
	segimage2itkimage --inputDICOM /mnt/hard/radiomics-features/LIDC-IDRI/mask_nifti/manifest-1585232716547/LIDC-IDRI/LIDC-IDRI-0001/01-01-2000-NA-NA-30178/3000567.000000-Segmentation\ of\ Nodule\ 1\ -\ Annotation\ Nodule\ 001-90548/1-1.dcm --outputDirectory . -t nifti
