from pathlib import Path

from radfeat import master_config

base_dir = Path("/mnt/hard/radiomics-features/LNDb")
raw_data_dir = base_dir / "raw" / "mhd"

config = master_config.Config(
    base_dir=base_dir,
    raw_data_dir=raw_data_dir,
)

# according to https://arxiv.org/pdf/1911.08434.pdf
label_interpretation = {
    0: "No routine follow-up required or optional CT at 12 months according to patient risk",
    1: "CT at 6-12 months required",
    2: "CT at 3-6 months required",
    3: "CT, PET/CT or tissue sampling at 3 months required",
}

texture_interpretation = {
    1: "GGO",
    2: "intermediate",
    3: "part solid",
    4: "intermediate",
    5: "solid",
}
