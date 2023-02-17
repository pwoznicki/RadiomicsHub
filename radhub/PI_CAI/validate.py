import logging
from autorad.utils import testing
from radhub.PI_CAI import config
import pandas as pd

log = logging.getLogger(__name__)

if __name__ == "__main__":
    utils.pretty_log("Validating data (2/2)")

    path_df = pd.read_csv(config.derived_table_dir / "paths.csv")
    testing.check_assertion_dataset(
        testing.assert_is_binary,
        path_df["seg_path"].values,
        raise_error=False,
    )
