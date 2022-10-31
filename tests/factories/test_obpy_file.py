from ob.factories import ObpyFileFactory
from ob.models import ObpyFile


def test_obpy_file_factory():
    fs_path = "/obpy-files/binance/BTCUSDT/2022-10-31/1667214131792_1667214134109.obpy"
    obpy_file = ObpyFileFactory(fs_root="/obpy-files", extension=".obpy").from_path(
        fs_path
    )

    assert isinstance(obpy_file, ObpyFile)
    assert obpy_file.fs_path == fs_path
