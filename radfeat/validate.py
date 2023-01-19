from autorad.utils import testing


def run_tests(path_df):
    img_paths = path_df["img_path"].values
    seg_paths = path_df["seg_path"].values

    single_assertions = [
        testing.assert_dimensionality,
        testing.assert_has_nonzero,
    ]
    img_mask_assertions = [
        testing.assert_equal_shape,
        testing.assert_has_nonzero_within_roi,
    ]
    for assert_fn in single_assertions:
        testing.check_assertion_dataset(assert_fn, img_paths)
        testing.check_assertion_dataset(assert_fn, seg_paths)
    for assert_fn in img_mask_assertions:
        testing.check_assertion_dataset(assert_fn, (img_paths, seg_paths))
