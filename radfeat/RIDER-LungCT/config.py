from radfeat import master_config


base_dir = master_config.root_dir / "RIDER-LungCT"

dicom_img_dir = base_dir / "dicom_img"
dicom_seg_dir = base_dir / "dicom_seg"

nifti_img_dir = base_dir / "nifti_img"
nifti_seg_dir = base_dir / "nifti_seg"


excluded = [
        "RIDER-2283289298" # only 1 timepoint
        "RIDER-5195703382" # only 1 timepoint
        "RIDER-8509201188" # only 1 timepoint
        ]
