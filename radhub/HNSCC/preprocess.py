from radhub import utils
import logging


log = logging.getLogger(__name__)


def convert_dataset(dicom_dir, output_dir):
    rt_paths = list(dicom_dir.rglob("*1-1.dcm"))
    data_paths = []
    for rt_path in rt_paths:
        dcm_paths = list(rt_path.parents[1].rglob("*1-001.dcm"))
        if not dcm_paths:
            log.warning(f"No CT images found for {rt_path}")
            continue
        dcm_dir = dcm_paths[0].parent
        data_paths.append((dcm_dir, rt_path))
    assert len(data_paths) == 627
