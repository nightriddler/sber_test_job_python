import pathlib
import unittest

from convert_markup import ConvertMarkup, get_files


class TestPath(unittest.TestCase):
    def test_get_files(self):
        catalog = "test"
        recursive = False
        suff_conv = "_bio"
        init_extension = ".ann"
        result = ["test\\data_one.ann", "test\\data_two.ann"]
        self.assertEqual(
            get_files(catalog, recursive, suff_conv, init_extension), result
        )

        recursive = True
        result = [
            "test\\data_one.ann",
            "test\\data_two.ann",
            "test\\folder\\data_in_folder.ann",
        ]
        self.assertEqual(
            get_files(catalog, recursive, suff_conv, init_extension), result
        )

        catalog = "test/folder"
        result = ["test\\folder\\data_in_folder.ann"]
        self.assertEqual(
            get_files(catalog, recursive, suff_conv, init_extension), result
        )

    def test_convert_markup(self):
        suff_conv = "_bio"
        final_extension = ".ann"
        start = ["test\\data_one.ann", "test\\data_two.ann"]

        converter = ConvertMarkup(start, suff_conv, final_extension)
        converter.convert_all()

        result = ["test\\data_one_bio.ann", "test\\data_two_bio.ann"]
        for file in result:
            self.assertTrue(pathlib.Path(file).exists())
            pathlib.Path(file).unlink()


if __name__ == "__main__":
    unittest.main()
