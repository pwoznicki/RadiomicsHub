from pathlib import Path

datasets = ["CRLM", "Desmoid", "GIST", "Lipo", "Liver", "Melanoma"]
modality_map = {
    "CRLM": "CT",
    "Desmoid": "MR",
    "GIST": "CT",
    "Lipo": "MR",
    "Liver": "MR",
    "Melanoma": "CT",
}
excluded_subjects = [
    "Melanoma-037",
    "Melanoma-039",
    "Melanoma-064",
    "Melanoma-071",
    "Melanoma-089",
    "Melanoma-094",
    "Melanoma-096",
    "Melanoma-100",
    "GIST-244",
]
