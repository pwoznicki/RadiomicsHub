import SimpleITK as sitk
from pathlib import Path
import config

def convert_sitk(in_path, out_path):
    if not in_path.exists():
        raise FileNotFoundError
    data = sitk.ReadImage(in_path)
    out_path.parent.mkdir(exist_ok=True)
    sitk.WriteImage(data, out_path)

def convert_dir(input_dir, output_dir)
    for img_path in input_dir.glob(".mhd"):
        out_img_path = output_dir / (img_path.name.split(".")[0] + ".nii.gz")
        convert_sitk(img_path, output_path)

def convert_mhd_to_nifti(data_dir):
    img_dir = data_dir / "raw_img"
    out_img_dir = data_dir / "nifti_img"
    convert_dir(img_dir, out_img_dir)

    seg_dir = data_dir / "raw_seg"
    out_seg_dir = data_dir / "nifti_seg"
    convert_dir(seg_dir, out_seg_dir)

if __name__ == "__main__":
    convert_mhd_to_nifti(config.base_dir)
        

        
