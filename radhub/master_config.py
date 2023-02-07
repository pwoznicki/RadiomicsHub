import logging
import logging.config
import sys
from dataclasses import dataclass
from pathlib import Path

from rich.logging import RichHandler

root_dir = Path("/mnt/volume_fra1_01/radiomics-features")

log = logging.getLogger(__name__)


@dataclass
class Config:
    base_dir: Path
    raw_data_dir: Path
    raw_img_dir: Path | None = None
    raw_seg_dir: Path | None = None

    def __post_init__(self):
        self.raw_table_dir = self.base_dir / "raw" / "tables"
        self.log_dir = self.base_dir / "logs"
        self.derived_table_dir = self.base_dir / "derived" / "tables"
        self.derived_nifti_dir = self.base_dir / "derived" / "nifti"
        self.raw_table_dir.mkdir(exist_ok=True, parents=True)
        self.derived_table_dir.mkdir(exist_ok=True, parents=True)
        self.derived_nifti_dir.mkdir(exist_ok=True)
        self.log_dir.mkdir(exist_ok=True)


def configure_logging(log_dir: Path):
    if not log_dir.exists():
        log_dir.mkdir(exist_ok=True, parents=True)
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "minimal": {"format": "%(message)s"},
            "detailed": {
                "format": "%(levelname)s %(asctime)s [%(name)s:%(filename)s:%(funcName)s:%(lineno)d]\n%(message)s\n"
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
                "formatter": "minimal",
                "level": logging.DEBUG,
            },
            "info": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": Path(log_dir) / "info.log",
                "maxBytes": 10485760,  # 1 MB
                "backupCount": 10,
                "formatter": "detailed",
                "level": logging.INFO,
            },
            "error": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": Path(log_dir) / "error.log",
                "maxBytes": 10485760,  # 1 MB
                "backupCount": 10,
                "formatter": "detailed",
                "level": logging.ERROR,
            },
        },
        "root": {
            "handlers": ["console", "info", "error"],
            "level": logging.INFO,
            "propagate": True,
        },
    }

    logging.config.dictConfig(logging_config)
    logger = logging.getLogger()
    logger.handlers[0] = RichHandler(markup=True)
